import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time
from pathlib import Path

import customtkinter
import random

from src.custom_nodes.model import classifier
from sgnlp_workflow import SmartCorrect, SA, ABSA

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Root:

    def position_button_event(self):
        self.capture_direction.set("Left" if self.capture_direction.get() == "Right" else "Right")

    def __init__(self):

        # Configs for testing and debugging
        self.cv_enabled = False
        self.sc_enabled = True
        self.sa_enabled = True

        self.window = customtkinter.CTk()

        # Create the GUI window
        self.window.geometry("1024x576")

        self.curr_string = tkinter.StringVar()
        self.input_string = tkinter.StringVar()
        self.latest_char = tkinter.StringVar()

        self.curr_pred_label = tkinter.StringVar()
        self.curr_pred_score = tkinter.StringVar()

        self.curr_sentiment = tkinter.StringVar()
        self.curr_sentiment_score = tkinter.DoubleVar()
        self.sentiment_str = tkinter.StringVar()

        # Create a label to display the webcam feed
        self.webcam_label = customtkinter.CTkLabel(self.window, text="")
        self.webcam_label.pack(padx=25,pady=(25,10),side="top", anchor="nw")

        if not self.cv_enabled:
            self.test_string = "_HI_HOW_ARE_YOU"
            self.test_string_pos = -1

        self.SC = SmartCorrect.SmartCorrect(self.sc_enabled)
        self.SA = SA.SA(self.sa_enabled)

        # Initialize the webcam
        self.webcam = cv2.VideoCapture(0)
        if not self.webcam.isOpened():
            raise Exception("Could not open video device")
        # Set properties. Each returns === True on success (i.e. correct resolution)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.model_node = classifier.Node(self.cv_enabled, pkd_base_dir=Path.cwd() / "src" / "custom_nodes")


        # Initialize the time of the last saved frame
        self.last_updated_at = 0

        # Initialize the time of the last captured frame
        self.last_captured_at = 0

        self.capture_direction = tkinter.StringVar(value="Right") #Default: right side of the screen
        
        self.is_captured = False

        self.position_button = customtkinter.CTkButton(master=self.window, textvariable=self.capture_direction, command=self.position_button_event)
        self.position_button.pack(padx=25,pady=(0,25),side="left",anchor='nw')
        self.sentiment_button = customtkinter.CTkButton(master=self.window, text="Sentiment: " ,textvariable=self.sentiment_str, width=200)
        self.sentiment_button.pack(padx=(0,25),pady=(0,25),side="left",anchor='nw')

        

        self.textbox_entry = customtkinter.CTkEntry(self.window,
                 textvariable = self.input_string, height=40, width=480, fg_color="white", border_width=2, border_color="gray50")
        self.textbox_entry.place(x=25, y=460)

        self.gc_button = customtkinter.CTkButton(master=self.window, text="Smart Correct", command=self.process_string)
        self.send_button = customtkinter.CTkButton(master=self.window, text="Send", command=self.send_message)

        self.gc_button.place(x=25, y=526)
        self.send_button.place(x=175, y=526)


        # Trace curr_string
        self.input_string.trace_add("write",self.update_curr_from_input)

        # Chat Interface

        self.user = tkinter.StringVar(value='User 1')
        self.user_option = customtkinter.StringVar(value="Select User")  # set initial value

        self.chat_frame = customtkinter.CTkFrame(master=self.window, width=440, height=576)
        self.chat_frame.pack_propagate(0)
        self.chat_frame.place(x=584, y=0)

        combobox = customtkinter.CTkOptionMenu(master=self.chat_frame,
                                            width = 100,
                                            height = 40,
                                            font = ("Helvetica", 16),
                                            values=["User 1", "User 2"],
                                            command=self.user_option_callback,
                                            variable=self.user_option)
        combobox.pack(padx=20, pady=10, side="top", anchor="ne")

        #Defining the frame on the left and the right to hold the messagess.
        self.msg_frame = customtkinter.CTkFrame(master=self.chat_frame, fg_color= "transparent", height=500)
        self.msg_frame.pack_propagate(0)
        self.msg_frame.pack(padx = 25, pady = (10,0), side="top", anchor="nw")

        # Start updating the GUI
        self.update_frame()

    def user_option_callback(self,choice):
        self.user.set(choice)

    def send_message(self,event = None):
        message = self.user.get() + ": " + self.curr_string.get()
        if self.user.get() == "User 1":
            user1_bubble = customtkinter.CTkLabel(self.msg_frame, text= message, width=100,fg_color=("lightgreen", "gray75"),font=("Helvetica", 12), corner_radius=10)
            user1_bubble.pack(side="top", pady=(0,10), anchor="w")
        else:
            user2_bubble = customtkinter.CTkLabel(self.msg_frame, text= message, fg_color=("lightblue", "gray75"), font=("Helvetica", 12), width=100,corner_radius=10)
            user2_bubble.pack(side="top", pady=(0,10), anchor="w")

    def update_input_from_curr(self, *args):
        print(args)
        s = self.curr_string.get()
        print(s)
        self.input_string.set(s)
        print(self.input_string.get())

    def update_curr_from_input(self, *args):
        print(args)
        s = self.input_string.get()
        print(s)
        self.curr_string.set(s)
        self.update_sentiment()

        print(self.curr_string.get())

    def get_capture_zone_border_color(self):
        # BGR format
        return (60,20,220) if not self.is_captured else (51,163,90)


    @staticmethod
    def get_capture_zone_position(parent_height, direction):
        # returns x1, y1, x2,y2
        if direction=="Right":
            return int(0.6 * parent_height), 10, parent_height - 10, int(0.4 * parent_height)
        
        elif direction=="Left":
            return 10, 10, int(0.4 * parent_height), int(0.4 * parent_height)
        else:
            return 0,0,0,0

    def predict(self, img):
        input_dict = {'img':img}

        res = self.model_node.run(input_dict)
        self.update_prediction(res['pred_label'], res['pred_score'])

    def update_prediction(self, label, score):
        
        if label == '_':
            self.curr_pred_label.set(' ')
        else:
            self.curr_pred_label.set(label)
        
        self.curr_pred_score.set('%.2f' % score)

    def update_sentiment(self):
        label, score = self.SA.run(self.curr_string.get())
        self.curr_sentiment.set(label)
        self.curr_sentiment_score.set(str(score))
        self.sentiment_str.set(f"{self.curr_sentiment.get()} ({str(self.curr_sentiment_score.get())}%)")

        self.sentiment_button.configure(fg_color="green" if label=='POSITIVE' else "red")

    def sc(self, raw):
        res = self.SC.run([raw.lower()])
        if res:
            return res[0]
        return raw
        
    def process_string(self):

        # Grammar correction
        processed = self.sc(self.curr_string.get())
        self.curr_string.set(processed)
        self.update_input_from_curr()
        self.update_sentiment()

    def capture_result(self):
        label = self.curr_pred_label.get()

        if not self.cv_enabled:
            self.test_string_pos += 1
            if self.test_string_pos >= len(self.test_string):
                label = "_"
            else:
                label = self.test_string[self.test_string_pos]
            

        if label and label != '_':
            self.latest_char = label
            self.curr_string.set(self.curr_string.get() + self.latest_char)
            self.update_input_from_curr()
            self.update_sentiment()

            self.is_captured = True
            self.last_captured_at = time.time()
        elif label:
            if self.latest_char == ' ':
                return
            self.latest_char = ' '
            self.curr_string.set(self.curr_string.get() + self.latest_char)
            self.update_input_from_curr()
            self.update_sentiment()

            self.is_captured = True
            self.last_captured_at = time.time()
        else:
            return


    def update_frame(self):
        _, frame = self.webcam.read()
        frame = cv2.flip(frame, 1)
        x1, y1, x2, y2 = self.get_capture_zone_position(frame.shape[1], self.capture_direction.get())
        cv2.rectangle(frame, (x1-1,y1-1), (x2+1,y2+1), self.get_capture_zone_border_color() ,2)
        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        print(cv2image.shape)

        img = PIL.Image.fromarray(cv2image)
        imgtk = PIL.ImageTk.PhotoImage(image=img)
        self.webcam_label.imgtk = imgtk
        self.webcam_label.configure(image=imgtk)


        cap_img = cv2image[y1:y2,x1:x2]
        
        self.predict(cap_img)


        current_time = time.time()
        if current_time - self.last_updated_at >= 1.5:
            self.capture_result()
            self.last_updated_at = current_time

        if current_time - self.last_captured_at >= 0.3:
            self.is_captured = False
            
        self.window.after(100, self.update_frame)



# Run the GUI loop
(Root()).window.mainloop()
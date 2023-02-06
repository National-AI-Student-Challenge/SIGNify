import tkinter as tk
import customtkinter as ctk
import datetime

font_tuple = ("Helvetica", 18)

#Defining the send message function
def send_message(event = None):
    message = user_var.get() + ": " + message_entry.get()
    if user_var.get() == "User 1":
        user1_bubble = ctk.CTkLabel(user_frame, text= message, width=100,fg_color=("lightgreen", "gray75"),font=("Helvetica", 12), corner_radius=10)
        user1_bubble.pack(side="top", pady=(0,10), anchor="w")
    else:
        user2_bubble = ctk.CTkLabel(user_frame, text= message, fg_color=("lightblue", "gray75"), font=("Helvetica", 12), width=100,corner_radius=10)
        user2_bubble.pack(side="top", pady=(0,10), anchor="w")
    message_entry.delete(0, ctk.END)
    print(user_var.get())




#Defining the main frame
root = ctk.CTk()
root.title("Chatbox")
ctk.set_appearance_mode("blue")

#Defining the frame on the left and the right to hold the messagess.
user_frame = ctk.CTkFrame(root, fg_color= "transparent", height=450)
user_frame.pack_propagate(0)
user_frame.pack(padx = 25, pady = (10,0), side="left", anchor="nw")



user_var = ctk.StringVar()
user_var.set("User 1")





#Allowing user to choose the initial user speaking
optionmenu_var = ctk.StringVar(value="Select User")  # set initial value

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)
    user_var.set(choice)

combobox = ctk.CTkOptionMenu(master=root,
                                    width = 100,
                                    height = 40,
                                    font = ("Helvetica", 16),
                                    values=["User 1", "User 2"],
                                    command=optionmenu_callback,
                                    variable=optionmenu_var)
combobox.pack(padx=20, pady=10)



#Change the dimension of the middle portion
messages = ctk.CTkFrame(root, width=300, height=500, fg_color= "transparent")
messages.pack()



##Defining the message enter box
message_entry= ctk.CTkEntry(master = root, font = font_tuple, width= 150,placeholder_text="Enter Text")
message_entry.pack()


font_tuple_2 = ("Helvetica", 12, "bold")
send_button = ctk.CTkButton(master = root, font = font_tuple_2, text="Send", command=send_message)
send_button.pack()

#Allow for easy toggle between User 1 and 2
def toggle_user():
    if user_var.get() == "User 1":
        user_var.set("User 2")
        ctk.StringVar(value="User 2")
    else:
        user_var.set("User 1")
        ctk.StringVar(value="User 1")

toggle_user_button = ctk.CTkButton(master = root,  font = font_tuple_2, text="Toggle User", command=toggle_user)
toggle_user_button.pack()


#Bind the enter button to send a message
root.bind('<Return>', send_message)
root.mainloop()
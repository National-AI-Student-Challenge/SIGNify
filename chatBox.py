import tkinter as tk
import customtkinter as ctk
import datetime

font_tuple = ("Helvetica", 18)
current_time = datetime.datetime.now().strftime("%H:%M")

#Defining the send message function
def send_message(event = None):
    message = user_var.get() + ": " + message_entry.get()
    if user_var.get() == "User 1":
        user1_bubble = ctk.CTkLabel(user1_frame, text= current_time + "  " + message, anchor="w", width=100,fg_color=("lightgreen", "gray75"),font=("Helvetica", 12), corner_radius=10)
        user1_bubble.pack(side="top", pady=10, anchor="w")
    else:
        user2_bubble = ctk.CTkLabel(user2_frame, text=current_time + "  " + message, fg_color=("lightblue", "gray75"), font=("Helvetica", 12),anchor="e", width=100,corner_radius=10)
        user2_bubble.pack(side="top", pady=10, anchor="e")
    message_entry.delete(0, ctk.END)
    print(user_var.get())




#Defining the main frame
root = ctk.CTk()
root.title("Chatbox")
ctk.set_appearance_mode("blue")

#Defining the frame on the left and the right to hold the messagess.
user1_frame = ctk.CTkFrame(root,corner_radius=30, fg_color= "transparent")
user1_frame.pack(side="left", pady=100, anchor="w")

user2_frame = ctk.CTkFrame(root, corner_radius=30, fg_color= "transparent")
user2_frame.pack(side="right", pady=100, anchor="e")


user_var = ctk.StringVar()
user_var.set("User 1")





#Allowing user to choose the initial user speaking
optionmenu_var = ctk.StringVar(value="Select User")  # set initial value

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)
    user_var.set(choice)

combobox = ctk.CTkOptionMenu(master=root,
                                    width = 200,
                                    height = 50,
                                    font = font_tuple,
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
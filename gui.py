from main import bot_response  
import time
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledText

root = tb.Window(themename="solar")
root.title("Simple Virtual Assistant")
root.geometry("690x635")


def send_message(event=None):
   msg = my_message.get()
   if msg.strip() != "":
       chat_window.insert(tb.END, "You: " + msg + "\n")
       my_message.set("")


       response = bot_response(msg)
       chat_window.insert(tb.END, "Agent: ", "agent")
       chat_window.update()
       for ch in buffer(response):
           chat_window.insert(tb.END,ch)
           chat_window.update()
       chat_window.insert(tb.END, "\n")
       print(response)



chat_window = ScrolledText(
    root,
    width=60,
    height=30,
    wrap=WORD,
    autohide=True,
    bootstyle="info",
    font=('Verdana', 15)
)
chat_window.grid(row=0, column=0, columnspan=2, padx=15, pady=15)
chat_window.tag_config("agent", foreground="dark grey")
chat_window.tag_config("user", foreground="white")

my_message = tb.StringVar()

#--------------------- BUFFER RESPONSE------------------
def buffer(response):
   delay = .025
   for ch in response:
       yield ch
       time.sleep(delay)
entry_field = tb.Entry(
    root,
    textvariable=my_message,
    width=48,
    bootstyle="info",
    font=('Verdana', 15)
)
entry_field.grid(row=1, column=0)
entry_field.bind("<Return>", send_message)

send_button = tb.Button(
    root,
    text="Send",
    command=send_message,
    width=6,
    bootstyle="outline"
)
send_button.grid(row=1, column=1)

topic = 'Catch Me If You Can'
initial_response = "Hi, I am your virtual assistant, ask me anything about " + topic

root.after(500, lambda: chat_window.insert(tb.END, "Agent: " + initial_response + "\n"))

root.mainloop()
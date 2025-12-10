from main import bot_response  
import time
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.constants import *

# ==================== WINDOW SETUP ====================
root = tb.Window(themename="darkly")
root.title("Catch Me If You Can - AI Assistant")

# Set window size
window_width = 900
window_height = 750

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position to center window
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)

# Set window geometry with center position
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)

# Configure root background
root.configure(bg="#343541")

# ==================== SIDEBAR FRAME (ChatGPT-style) ====================
sidebar_frame = tb.Frame(root, bootstyle="dark", width=260)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="ns", padx=0, pady=0)
sidebar_frame.grid_propagate(False)

# New Chat Button
new_chat_button = tb.Button(
    sidebar_frame,
    text="+ New Chat",
    bootstyle="light-outline",
    width=30,
    command=lambda: clear_chat()
)
new_chat_button.pack(padx=15, pady=20)

# Sidebar title
sidebar_title = tb.Label(
    sidebar_frame,
    text="Movie Database",
    font=('Helvetica', 12, 'bold'),
    bootstyle="inverse-dark"
)
sidebar_title.pack(padx=15, pady=(20, 10), anchor="w")

# Movie info
movie_info = tb.Label(
    sidebar_frame,
    text="Catch Me If You Can\n2002 • Steven Spielberg",
    font=('Helvetica', 9),
    bootstyle="secondary",
    justify=LEFT
)
movie_info.pack(padx=15, pady=5, anchor="w")

# Separator
separator = tb.Separator(sidebar_frame, bootstyle="secondary")
separator.pack(fill=X, padx=15, pady=20)

# Example questions section
examples_label = tb.Label(
    sidebar_frame,
    text="Example Questions",
    font=('Helvetica', 12, 'bold'),
    bootstyle="inverse-dark"
)
examples_label.pack(padx=15, pady=(10, 10), anchor="w")

example_questions = [
    "Who directed the movie?",
    "What jobs did Frank pretend to have?",
    "How much money did Frank steal?",
    "Who composed the music?"
]

def insert_example(question):
    my_message.set(question)
    entry_field.focus()

for question in example_questions:
    example_btn = tb.Button(
        sidebar_frame,
        text=f"→ {question[:35]}{'...' if len(question) > 35 else ''}",
        bootstyle="primary-link",
        command=lambda q=question: insert_example(q),
        width=28
    )
    example_btn.pack(padx=15, pady=2, anchor="w")

# ==================== MAIN CHAT AREA ====================
main_frame = tb.Frame(root, bootstyle="dark")
main_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=0, pady=0)

# Header (minimal like ChatGPT)
header_frame = tb.Frame(main_frame, bootstyle="dark")
header_frame.pack(fill=X, padx=0, pady=0)

title_label = tb.Label(
    header_frame,
    text="Catch Me If You Can Assistant",
    font=('Helvetica', 14, 'bold'),
    bootstyle="inverse-dark",
    padding=20,
    anchor=CENTER
)
title_label.pack(fill=X)

# Thin separator line
header_separator = tb.Separator(main_frame, bootstyle="secondary")
header_separator.pack(fill=X)

# ==================== CHAT WINDOW ====================
chat_container = tb.Frame(main_frame, bootstyle="dark")
chat_container.pack(fill=BOTH, expand=True, padx=0, pady=0)

# Chat window - centered content like ChatGPT
chat_window = ScrolledText(
    chat_container,
    wrap=WORD,
    autohide=True,
    bootstyle="dark",
    font=('Segoe UI', 12),
    padding=30
)
chat_window.pack(fill=BOTH, expand=True)

# Configure text tags (ChatGPT-style)
chat_window.tag_config(
    "user", 
    foreground="#ECECF1",
    font=('Segoe UI', 12),
    spacing1=8,
    spacing3=8,
    lmargin1=20,
    lmargin2=20
)
chat_window.tag_config(
    "agent", 
    foreground="#D1D5DB",
    font=('Segoe UI', 12),
    spacing1=8,
    spacing3=8,
    lmargin1=20,
    lmargin2=20
)
chat_window.tag_config(
    "user_label", 
    foreground="#FFFFFF",
    font=('Segoe UI', 12, 'bold'),
    spacing1=15,
    lmargin1=20
)
chat_window.tag_config(
    "agent_label", 
    foreground="#10A37F",
    font=('Segoe UI', 12, 'bold'),
    spacing1=15,
    lmargin1=20
)
chat_window.tag_config(
    "timestamp", 
    foreground="#6B7280",
    font=('Segoe UI', 8),
    lmargin1=20
)

# ==================== INPUT AREA (Bottom) ====================
input_container = tb.Frame(main_frame, bootstyle="dark")
input_container.pack(fill=X, padx=40, pady=20)

# Create frame for input with border (ChatGPT-style rounded input)
input_frame = tb.Frame(input_container, bootstyle="secondary", relief="solid", borderwidth=1)
input_frame.pack(fill=X)

my_message = tb.StringVar()

# Entry field
entry_field = tb.Entry(
    input_frame,
    textvariable=my_message,
    font=('Segoe UI', 13),
    bootstyle="dark",
    foreground="#ECECF1"
)
entry_field.pack(side=LEFT, fill=BOTH, expand=True, padx=15, pady=12)

# Send button (minimal icon-style)
send_button = tb.Button(
    input_frame,
    text="↑",
    bootstyle="success",
    width=3,
    command=lambda: send_message()
)
send_button.pack(side=RIGHT, padx=10, pady=8)

# Character count below input
char_count_label = tb.Label(
    input_container,
    text="",
    font=('Segoe UI', 8),
    bootstyle="secondary"
)
char_count_label.pack(pady=(5, 0))

def update_char_count(*args):
    count = len(my_message.get())
    if count > 0:
        char_count_label.config(text=f"{count}/500 characters")
        if count > 500:
            char_count_label.config(bootstyle="danger")
        else:
            char_count_label.config(bootstyle="secondary")
    else:
        char_count_label.config(text="")

my_message.trace('w', update_char_count)

# Configure grid weights for responsive layout
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

# ==================== SEND MESSAGE FUNCTION ====================
def send_message(event=None):
    msg = my_message.get().strip()
    if msg != "" and len(msg) <= 500:
        current_time = time.strftime("%H:%M")
        
        # Display user message
        chat_window.insert(END, "You\n", "user_label")
        chat_window.insert(END, f"{msg}\n\n", "user")
        my_message.set("")
        
        # Scroll to bottom
        chat_window.see(END)
        chat_window.update()
        
        # Get response
        response = bot_response(msg)
        
        # Display agent response with label
        chat_window.insert(END, "Assistant\n", "agent_label")
        
        # Animate response
        for ch in buffer(response):
            chat_window.insert(END, ch, "agent")
            chat_window.see(END)
            chat_window.update()
        
        chat_window.insert(END, "\n\n")
        chat_window.see(END)
        
        print(f"[{current_time}] User: {msg}")
        print(f"[{current_time}] Agent: {response}\n")

# Bind enter key
entry_field.bind("<Return>", send_message)

# ==================== CLEAR CHAT FUNCTION ====================
def clear_chat():

    chat_window.delete(1.0, END)
    show_initial_message()

# ==================== BUFFER RESPONSE ====================
def buffer(response):
    delay = 0.015
    for ch in response:
        yield ch
        time.sleep(delay)

# ==================== INITIAL MESSAGE ====================
initial_response = (
    "Hello! I'm your AI assistant specialized in the movie 'Catch Me If You Can' (2002). "
    "I can answer questions about the plot, cast, production, and interesting facts about the film.\n\n"
    "Feel free to ask me anything, or try one of the example questions from the sidebar!"
)

def show_initial_message():
    chat_window.insert(END, "Assistant\n", "agent_label")
    chat_window.insert(END, initial_response + "\n\n", "agent")

root.after(200, show_initial_message)

# Focus on entry field when window loads
root.after(300, lambda: entry_field.focus())

# Bind keyboard shortcuts
root.bind("<Control-l>", lambda e: clear_chat())
root.bind("<Control-q>", lambda e: root.quit())
root.bind("<Escape>", lambda e: entry_field.focus())

# ==================== RUN ====================
root.mainloop()
import tkinter as tk
from time import sleep

def scale_font(event):
    # Calculate the font size based on the window width
    font_size = max(20, int(event.width / 6))
    label.config(font=('Helvetica', font_size, 'bold'))

def toggle_fullscreen(event):
    if root.attributes('-fullscreen'):
        root.attributes('-fullscreen', False)
    else:
        root.attributes('-fullscreen', True)


def adjust_time(value, increment):
    global hours, minutes, seconds
    if value == "hours":
        hours = (hours + increment) % 24
    elif value == "minutes":
        minutes = (minutes + increment) % 60
    elif value == "seconds":
        seconds[0] = (seconds[0] + increment) % 60  # Update seconds using a mutable object
    update_display()

def update_display():
    global selected_value, countdown_running 
    time_format = f"{hours:02d}:{minutes:02d}:{seconds[0]:02d}"
    label.config(text=time_format)
    if countdown_running == False:
        if selected_value == "hours":
            label.config(underline=1)  # Underline the hours part (0-based index)
        elif selected_value == "minutes":
            label.config(underline=4)  # Underline the minutes part
        elif selected_value == "seconds":
            label.config(underline=7)  # Underline the seconds part
        return
    elif countdown_running == True:
        label.config(underline=-1)  # Remove underline from the label
        return

def toggle_countdown():
    global countdown_running
    countdown_running = not countdown_running #switch whether countdown_running is true or false
    if countdown_running:
        # Start countdown when spacebar is pressed
        start_countdown()
    else:
        # Stop countdown when spacebar is pressed again
        stop_countdown()

def start_countdown():
    global countdown_running
    countdown_running = True
    try:
        time_str = label.cget("text")
        hours, minutes, seconds[0] = map(int, time_str.split(":"))  # Update seconds using a mutable object
        total_seconds = hours * 3600 + minutes * 60 + seconds[0]
        countdown(total_seconds)
    except ValueError:
        # Handle invalid input here if needed
        pass

def reset_timer():
    global hours, minutes, countdown_running
    hours, minutes = 0, 0
    seconds[0] = 0  # Update seconds using a mutable object
    countdown_running = False
    label.config(foreground='white')
    reset_button.config(foreground="black")  # Disable the button after resetting
    update_display()

def countdown(total_seconds):
    global countdown_running, hours, minutes, seconds
    while seconds[0] >= 0 and countdown_running:
        if seconds[0] > 0:
            seconds[0] -= 1
        elif seconds[0] == 0:
            if minutes > 0:
                minutes -= 1
                seconds[0] = 59  # Update seconds using a mutable object
            elif minutes == 0:
                if hours > 0:
                    hours -= 1
                    minutes = 59
                    seconds[0] = 59  # Update seconds using a mutable object
                elif hours == 0:
                    label.config(foreground='red')  # Set text color to red
                    countdown_running = False  # Stop countdown when it reaches zero
                    reset_button.config(foreground="white")  # Enable the "Reset" button
        root.update()
        update_display()
        sleep(1)

def stop_countdown():
    global countdown_running
    countdown_running = False

def handle_keypress(event):
    global selected_value, countdown_running
    key = event.keysym
    if key == "Right":
        if selected_value == "hours":
            selected_value = "minutes"
        elif selected_value == "minutes":
            selected_value = "seconds"
        elif selected_value == "seconds":
            selected_value = "hours"
    elif key == "Left":
        if selected_value == "hours":
            selected_value = "seconds"
        elif selected_value == "minutes":
            selected_value = "hours"
        elif selected_value == "seconds":
            selected_value = "minutes"
    elif key == "Up":
        adjust_time(selected_value, 1)
    elif key == "Down":
        adjust_time(selected_value, -1)
    elif key == "space":
        toggle_countdown()
    else:
        return

    # Update the label text and underline the selected_value
    update_display()

def show_instructions():
    popup = tk.Toplevel()
    popup.title("Instructions")
    popup.geometry("400x170")  # Set the size of the popup window

    # Add a label with instructions

    instructions_label = tk.Label(
    popup, 
    text="Instructions:\n"
         "←→ arrow  keys to select place value.\n"
         "↑↓ arrow keys to adjust amount of time.\n"
         "Spacebar to start/stop the countdown.\n"
         "F11 to toggle fullscreen mode.\n"
         "Crtl + Q to close the app.\n",
    font=('Helvetica', 14, 'bold'),
    padx=0,
    pady=0,
    foreground="white",
    background="black"
)

    instructions_label.pack(fill='both', expand=True)
    # Function to close the popup window
    def close_popup():
        popup.destroy()
        root.attributes('-topmost', 1)


    # Bind the close button event (X button) to the close_popup function
    popup.protocol("WM_DELETE_WINDOW", close_popup)

    popup.lift()
    popup.attributes("-topmost", 1)
    popup.after(1, popup.attributes, "-topmost", 0)  # Remove the "always on top" attribute

# Function to close the window
def close_window(event):
    root.destroy()







root = tk.Tk()
root.title("Countdown Timer App")
root.geometry("400x200")  # Set the initial size of the timer window


hours, minutes = 0, 0
seconds = [0]  # Use a list to hold seconds as a mutable object
selected_value = "seconds"
countdown_running = False  # Initialize countdown as paused

label = tk.Label(root, font=('Helvetica', 20, 'bold'))
label.config(background='black', foreground='white') 
label.pack(fill='both', expand=True)
label.bind("<Configure>", scale_font)
update_display()

root.bind("<Left>", handle_keypress)
root.bind("<Right>", handle_keypress)
root.bind("<Up>", handle_keypress)
root.bind("<Down>", handle_keypress)
root.bind("<space>", handle_keypress)  # Bind spacebar to toggle countdown
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", toggle_fullscreen)
root.bind("<Control-q>", close_window)  # Bind Ctrl+Q to close the window


reset_button = tk.Button(
    root, 
    font=('Helvetica', 20, 'bold'), 
    background='black', 
    foreground='black', 
    text="Reset", 
    command=reset_timer, 
    relief="flat",
    padx=0
    )
reset_button.pack(fill='x')  # Set fill='x' to make the button fill the width of its parent


show_instructions() 

root.mainloop()

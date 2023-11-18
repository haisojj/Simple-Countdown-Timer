import tkinter as tk

def move_label(event):
    label.place(x=event.x, y=event.y)  # Move the label to the mouse pointer's position

root = tk.Tk()
root.geometry("400x300")

label = tk.Label(root, text="Move me!", font=("Helvetica", 14))
label.pack()

# Bind the left mouse button click event to the move_label function
root.bind("<Button-1>", move_label)

root.mainloop()

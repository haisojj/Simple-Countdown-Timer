import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

label = tk.Label(root, text="Bottom Right", font=("Helvetica", 14))
label.place(x=root.winfo_screenwidth() - label.winfo_reqwidth(), y=root.winfo_screenheight() - label.winfo_reqheight())

root.mainloop()

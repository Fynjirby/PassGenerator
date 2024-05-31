import tkinter as tk
import string, random
import datetime, webbrowser, os

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Password Generator")
        master.geometry("500x300")
        master.resizable(False, False)  
    
        self.center_window()
        self.file_name = "generated_pass.txt"
        self.save_enabled = tk.BooleanVar()

        self.label = tk.Label(master, text="Enter the number of characters:")
        self.label.pack(pady=20)

        self.entry = tk.Entry(master)
        self.entry.pack(pady=5)

        self.button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.button.pack(pady=20)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack(pady=20)

        self.copy_button = tk.Button(master, text="Copy", command=self.copy_password)
        self.copy_button.pack(pady=0)
        
        self.label = tk.Label(master, text="Ctrl+C or Cmd+C")
        self.label.pack(pady=0)

        self.menu = tk.Menu(master)
        master.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)

        self.save_checkbutton = tk.BooleanVar()
        self.file_menu.add_checkbutton(label="Save generated passwords", variable=self.save_checkbutton, onvalue=True, offvalue=False)
        self.file_menu.add_command(label="Open generated passwords", command=self.open_file)
        self.file_menu.add_command(label="Delete generated passwords", command=self.delete_file)
        
        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.help_menu.add_command(label="Github", command=lambda: webbrowser.open("https://github.com/fynjirby"))

        self.master.bind("<Return>", lambda event: self.generate_password())
        self.master.bind("<Control-g>", lambda event: webbrowser.open("https://github.com/fynjirby"))
        self.master.bind("<Command-g>", lambda event: webbrowser.open("https://github.com/fynjirby"))
        self.master.bind("<Control-c>", lambda event: self.copy_password())
        self.master.bind("<Command-c>", lambda event: self.copy_password())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Command-o>", lambda event: self.open_file())

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width/2) - (500/2)
        y = (screen_height/2) - (300/2)
        self.master.geometry(f'+{int(x)}+{int(y)}')

    def generate_password(self, event=None):
        n = int(self.entry.get())
        symbols = list(string.ascii_letters + string.digits)
        random.shuffle(symbols)
        self.password = ''.join(symbols[:n])
        self.result_label.config(text="Generated password: " + self.password)
        if self.save_checkbutton.get():
            self.save_password()

    def copy_password(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.password)

    def save_password(self):
        with open(self.file_name, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {self.password}\n")
            
    def open_file(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("Generated Passwords")
        new_window.geometry("500x300")
        new_window.resizable(False, False)

        text_widget = tk.Text(new_window, width=500, height=300)
        text_widget.pack()

        with open(self.file_name, "r") as f:
            content = f.read()
            text_widget.insert(tk.END, content)
            
    def delete_file(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
            self.result_label.config(text="File deleted")

            
root = tk.Tk()
my_gui = PasswordGenerator(root)
root.mainloop()
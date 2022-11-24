import customtkinter
import tkinter
from tkinter import filedialog
from tkinter import messagebox
from cryptography.fernet import Fernet


################################ Password Manager ################################

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}
    
    #creates a key given a name or a path with a name
    def create_key(self):
        self.key = Fernet.generate_key()
        path = self.browse_files()
        with open(path, 'wb') as f:
            f.write(self.key)

    #loads a key given a name or a path with name
    def load_key(self):
        path = self.browse_files()
        with open(path, "rb") as f:
            self.key = f.read()

    #creates a key given a name or a path with name
    def create_password_file(self, initial_values = None):
        path = self.browse_files()
        self.password_file = path


        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    #loads a key given a name or a path with name
    def load_password_file(self):
        path = self.browse_files()
        self.password_file = path

        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(':')
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()

    #adds a password to the loaded password file
    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    #outputs a password from the loaded password file given the site corresponding to the password
    def get_password(self, site):
        return self.password_dict[site]
    
    #opens the file explorer
    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = (("Text files","*.txt*"),("all files","*.*")))
        return filename


################################ GUI ################################

class App(customtkinter.CTk):
    

    WIDTH = 780
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        
        self.pm = PasswordManager()

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Andris' Password Manager v1.0")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frame = customtkinter.CTkFrame(master=self)

        self.lable = customtkinter.CTkLabel(master=self, text="Andris' Password Manager v1.0", width=450, height=20)
        self.lable.pack(pady=10, padx=10)

        self.button1 = customtkinter.CTkButton(master=self, text="Create a new key", command=lambda: self.pm.create_key(),width=450, height=60)
        self.button1.pack(pady=10, padx=50)

        self.button2 = customtkinter.CTkButton(master=self, text="Load a key", command=lambda: self.pm.load_key(), width=450, height=60)
        self.button2.pack(pady=10, padx=50)

        self.button3 = customtkinter.CTkButton(master=self, text="Create new password file", command=lambda: self.pm.create_password_file(), width=450, height=60)
        self.button3.pack(pady=10, padx=50)

        self.button4 = customtkinter.CTkButton(master=self, text="Load a password file", command=lambda: self.pm.load_password_file(), width=450, height=60)
        self.button4.pack(pady=10, padx=50)

        self.button5 = customtkinter.CTkButton(master=self, text="Add new password",command=lambda: self.password_event(), width=450, height=60)
        self.button5.pack(pady=10, padx=50)
        
        self.button6 = customtkinter.CTkButton(master=self, text="Get password", command=lambda: self.pass_out(), width=450, height=60)
        self.button6.pack(pady=10, padx=50)

        self.textbox = customtkinter.CTkTextbox(master=self, width=450, height=100)
        self.textbox.pack(pady=10, padx=50)
        self.textbox.insert("0.0", "Your password is: ")

    def password_event(self):
        dialog = tkinter.simpledialog.askstring(title="site", parent=self, prompt="Site")
        if dialog is not None:
            pword = tkinter.simpledialog.askstring(title="Password", parent=self, prompt="Password")
            self.pm.add_password(dialog, pword)
        else:
            return None
    
    def pass_out(self):
        dialog = tkinter.simpledialog.askstring(title="site", parent=self, prompt="Site")
        if dialog is not None:
            password = self.pm.get_password(dialog)
            self.textbox.insert("2.0", password)
        else:
            self.textbox.insert("2.0", "No input")
    
    def on_closing(self, event=0):
        self.bye = tkinter.messagebox.showinfo(master=self, title="BYE!", message="Thanks for using! Bye!")
        self.destroy()



if __name__ == "__main__":
    app = App()
    app.mainloop()

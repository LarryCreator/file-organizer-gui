import customtkinter

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("File organizer GUI")
        self.geometry("800x696")
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        self.mainFrame = MainFrame(self, "File Organizer GUI")

    def button_callback(self):
        print("button pressed")

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=6)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)

        self.grid(row=0, column=0, columnspan=2, sticky="nsew",padx=10, pady=10)
        self.titleWidget = customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6, font=("arial", 24, "bold"))
        self.titleWidget.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.logsFrame = LogsFrame(self)
        self.settingsFrame = SettingsFrame(self)
        self.targetFolderFrame = TargetFolderFrame(self)
        self.button = customtkinter.CTkButton(self, text="Start Organization", font=("arial", 24, "bold"), fg_color="#315CC8")
        self.button.grid(row=4, column=0, columnspan=2, sticky="nsew",padx=10,pady=5)

class LogsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#161616")
        self.title = "Activity Logs"
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.titleWidget = customtkinter.CTkLabel(self, text=self.title, corner_radius=6, font=("arial", 17, "bold"))
        self.titleWidget.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#353535")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.title1="Select categories:"
        self.title2="Operation mode:"
        self.titleWidget1 = customtkinter.CTkLabel(self, text=self.title1, corner_radius=6, font=("arial", 17, "bold"), fg_color="#161616")
        self.titleWidget1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="ew")
        self.titleWidget2 = customtkinter.CTkLabel(self, text=self.title2, corner_radius=6, font=("arial", 17, "bold"), fg_color="#161616")
        self.titleWidget2.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

class TargetFolderFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#353535")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid(row=3, column=0, sticky="nsew",padx=10,pady=10)
        self.title = "Target Folder"
        self.titleWidget = customtkinter.CTkLabel(self, text=self.title, corner_radius=6, font=("arial", 17, "bold"), fg_color="#161616")
        self.titleWidget.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Select Folder", font=("arial", 20), fg_color="#666666")
        self.button.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=10,pady=10)

app = App()
app.mainloop()

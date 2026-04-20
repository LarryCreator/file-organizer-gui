import customtkinter
from organizer import main as organize
from CTkMessagebox import CTkMessagebox
from datetime import datetime

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.folderPath = None
        self.operationMode = "move"
        self.selectedCategories = ['videos', 'documents', 'audios', 'images', 'others']
        self.title("File organizer GUI")
        self.geometry("800x696")
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(False, False)

        self.mainFrame = MainFrame(self, "File Organizer GUI", self)
    
    def updateSelectedCategories(self, checkBox):
        checkBoxName = checkBox.cget("text").lower()
        if checkBox.get() == 'on':
            logMessage = f"Category {checkBoxName.capitalize()} checked"
            if checkBoxName not in self.selectedCategories:
                self.selectedCategories.append(checkBoxName)
        else:
            logMessage = f"Category {checkBoxName.capitalize()} unchecked"
            if checkBoxName in self.selectedCategories:
                self.selectedCategories.remove(checkBoxName)

        self.mainFrame.logsFrame.updateLogs(logMessage)

    def updateSelectedOpMode(self, radioButton):
        if radioButton.cget("value") == 1:
            self.operationMode = 'move'
        else:
            self.operationMode = "copy"

        logMessage = f"Mode: {self.operationMode.capitalize()}"
        self.mainFrame.logsFrame.updateLogs(logMessage)
    
    def updateFolderPath(self, newPath):
        self.folderPath = newPath
        folderName = self.folderPath[self.folderPath.rfind("/")+1:]
        logMessage = f"Folder set: {folderName}"
        self.mainFrame.logsFrame.updateLogs(logMessage, folderLog=True)

    def displayOrganizingLogs(self, result):
        actionWord = "moved" if self.operationMode == "move" else "copied"
        if len(result) > 0:
            self.mainFrame.logsFrame.updateLogs("Starting organization...")
            for key in result.keys():
                if key != "total":
                    self.mainFrame.logsFrame.updateLogs(f"{result[key]} files {actionWord} to {key.capitalize()} folder")
            self.mainFrame.logsFrame.updateLogs(f"{result["total"]} files {actionWord} in total")
        else:
            self.mainFrame.logsFrame.updateLogs("Error: Folder has no files")

    def handleOrganizingErrors(self, result):
        if result == 'category':
            errorMessage = 'You must select at least one category!!!'
            self.mainFrame.logsFrame.updateLogs("Error: No category selected")
            CTkMessagebox(title="Error", message=errorMessage, icon="cancel")
        elif result == 'folder':
            errorMessage = 'You must select a folder to run the application!!!'
            CTkMessagebox(title="Error", message=errorMessage, icon="cancel")
            self.mainFrame.logsFrame.updateLogs("Error: No folder selected")

    def exportLogs(self):
        print("")
        #to do

    def runApplication(self):
        result = organize(self.folderPath, self.selectedCategories, self.operationMode)
        if (result["errors"] != ""):
            self.handleOrganizingErrors(result["errors"])
        else:
            self.displayOrganizingLogs(result["logs"])

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, app):
        super().__init__(master)
        self.app = app
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=6)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew",padx=10, pady=10)
        self.titleWidget = customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6, font=("arial", 24, "bold"))
        self.titleWidget.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.logsFrame = LogsFrame(self, app)
        self.settingsFrame = SettingsFrame(self, app)
        self.targetFolderFrame = TargetFolderFrame(self, app)
        self.runAppButton = customtkinter.CTkButton(self, text="Start Organization", font=("arial", 20, "bold"), fg_color="#315CC8", command=self.organizeButtonCommand)
        self.runAppButton.grid(row=5, column=0, columnspan=2, sticky="nsew",padx=10,pady=5)
        self.exportLogsButton = customtkinter.CTkButton(self, text="Export logs", font=("arial", 15, "bold"), fg_color="gray20")
        self.exportLogsButton.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)

    def organizeButtonCommand(self):
        self.app.runApplication()
    
    def exportLogsButtonCommand(self):
        self.app.exportLogs()

class LogsFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="#161616", orientation="vertical")
        self.app = app
        self.title = "Activity Logs"
        self.defaultLabel = "No activity yet. \nConfigure settings and start organizing!"
        self.logs = []
        self.logColor = "#1AE9D8"
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.titleWidget = customtkinter.CTkLabel(self, text=self.title, corner_radius=6, font=("arial", 17, "bold"))
        self.titleWidget.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")
        self.defaultLabelWidget = customtkinter.CTkLabel(self, text=self.defaultLabel, corner_radius=6, font=("arial", 12, "bold"), text_color="gray")
        self.defaultLabelWidget.grid(row=1, column=0, columnspan=3, padx=10, pady=(1, 0), sticky="ew")

    def updateLogs(self, logMessage, folderLog=False):
        finalLogMessage = f"[{datetime.now().strftime('%H:%M:%S')}] {logMessage}"
        if len(self.logs) == 0:
            self.defaultLabelWidget.configure(text=finalLogMessage, text_color=self.logColor, anchor='w')
        else:
            newLabel = customtkinter.CTkLabel(self, text=finalLogMessage, corner_radius=6, font=("arial", 12, "bold"), text_color=self.logColor, anchor='w')
            newLabel.grid(row=len(self.logs)+1, column=0, columnspan=3, padx=10, pady=(1, 0), sticky='ew')
            
        if folderLog:
            logWithFullFolderPath = f"[{datetime.now().strftime('%H:%M:%S')}] {logMessage[logMessage.rfind(":"):]}{self.app.folderPath}"
            self.logs.append(logWithFullFolderPath)
        else:
            self.logs.append(finalLogMessage)
        self.scrollDown()

    def scrollDown(self):
        self.after(10, self._parent_canvas.yview_moveto, 1.0)

class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="#353535")
        self.app = app
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
        self.checkBoxes = []
        self.radioButtons = []
        self.setUpCheckBoxes()
        self.setUpRadioButtons()
    
    def setUpCheckBoxes(self):
        index = 1
        content = {
            "videos": ".mp4', '.avi', '.mkv', '.wmv', '.mov', '.webm",
            'images': '.png, .jpg, .jpeg, .jfif, .gif, .svg, .webp',
            'documents': '.txt, .docx, .pdf, .csv, .xlsx',
            'audios': '.mp3, .wav, .aiff, .aac',
            'others': "All other extensions"
        }
        for title in content:
            checkVar = customtkinter.StringVar(value="on")
            checkBox = customtkinter.CTkCheckBox(self, text=title.capitalize(), variable=checkVar, onvalue="on", offvalue="off")
            checkBox.grid(row=index, column=0,padx=10,pady=10,sticky="ew")
            checkBox.configure(command=lambda cb=checkBox: self.app.updateSelectedCategories(cb))
            self.checkBoxes.append(checkBox)
            index += 1
    
    def setUpRadioButtons(self):
        index = 1
        content = ["move files", "copy files"]
        radioVar = customtkinter.IntVar(value=index)
        for i in range (len(content)):
            radioButton = customtkinter.CTkRadioButton(self, text=content[i].capitalize(), variable=radioVar, value=index)
            radioButton.configure(command=lambda rb=radioButton:self.app.updateSelectedOpMode(rb))
            radioButton.grid(row=index, column=1, padx=10, pady=10, sticky="ew")
            self.radioButtons.append(radioButton)
            index += 1

class TargetFolderFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="gray20")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid(row=3, rowspan=2, column=0, sticky="nsew",padx=10,pady=10)
        self.title = "Target Folder"
        self.titleWidget = customtkinter.CTkLabel(self, text=self.title, corner_radius=6, font=("arial", 17, "bold"), fg_color="#161616")
        self.titleWidget.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Select Folder", font=("arial", 18), fg_color="gray30", command=self.getFolderPath)
        self.button.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=10,pady=10)
        self.button.grid_propagate(False)


    def getFolderPath(self):
        folderSelected = customtkinter.filedialog.askdirectory(title="Select a folder to be organized")
        self.app.updateFolderPath(folderSelected)
        self.showPathOnUI()

    def showPathOnUI(self):
        if isinstance(self.app.folderPath, str) and self.app.folderPath != '':
            self.button.configure(text=self.app.folderPath, font=('arial', 12, 'bold'), fg_color="#007180")

app = App()
app.mainloop()

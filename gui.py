import customtkinter
from organizer import export_logs, run_organization
from CTkMessagebox import CTkMessagebox
from datetime import datetime

app_font = 'arial'

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 696
        self.folder_path = None
        self.operation_mode = "move"
        self.selected_categories = ['videos', 'documents', 'audios', 'images', 'others']
        self.title("File organizer GUI")
        self.logs = []
        self.geometry("800x696")
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(False, False)
        self.main_frame = MainFrame(self, "File Organizer GUI", self)
        self.center_window()

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.geometry(f'{self.width}x{self.height}+{int(x)}+{int(y)}')
    
    def update_selected_categories(self, checkbox):
        checkbox_name = checkbox.cget("text").lower()
        if checkbox.get() == 'on':
            log_message = f"Category {checkbox_name.capitalize()} checked"
            if checkbox_name not in self.selected_categories:
                self.selected_categories.append(checkbox_name)
        else:
            log_message = f"Category {checkbox_name.capitalize()} unchecked"
            if checkbox_name in self.selected_categories:
                self.selected_categories.remove(checkbox_name)

        self.main_frame.logs_frame.update_logs(log_message)

    def update_operation_mode(self, radio_button):
        if radio_button.cget("value") == 1:
            self.operation_mode = 'move'
        else:
            self.operation_mode = "copy"

        log_message = f"Mode: {self.operation_mode.capitalize()}"
        self.main_frame.logs_frame.update_logs(log_message)
    
    def update_folder_path(self, new_path):
        self.folder_path = new_path
        folder_name = self.folder_path[self.folder_path.rfind("/")+1:]
        log_message = f"Folder set: {folder_name}"
        self.main_frame.logs_frame.update_logs(log_message, folder_log=True)

    def display_organizing_logs(self, result):
        action_word = "moved" if self.operation_mode == "move" else "copied"
        if len(result) > 0:
            self.main_frame.logs_frame.update_logs("Starting organization...")
            for detailed_log in result['details']:
                log_message = f"[{datetime.now().strftime('%H:%M:%S')}] {detailed_log}"
                self.logs.append(log_message)
            for key in result.keys():
                if key != "total" and key != "details":
                    self.main_frame.logs_frame.update_logs(f"{result[key]} files {action_word} to {key.capitalize()}")
            self.main_frame.logs_frame.update_logs(f"{result["total"]} files {action_word} in total")
        else:
            self.main_frame.logs_frame.update_logs("Error: Folder has no files")

    def handle_organizing_errors(self, result):
        if result == 'category':
            error_message = 'You must select at least one category!!!'
            self.main_frame.logs_frame.update_logs("Error: No category selected")
            CTkMessagebox(title="Error", message=error_message, icon="cancel")
        elif result == 'folder':
            error_message = 'You must select a folder to run the application!!!'
            CTkMessagebox(title="Error", message=error_message, icon="cancel")
            self.main_frame.logs_frame.update_logs("Error: No folder selected")

    def enable_export_button(self):
        self.main_frame.export_logs_button.configure(state="normal")

    def run_application(self):
        result = run_organization(self.folder_path, self.selected_categories, self.operation_mode)
        if (result["errors"] != ""):
            self.handle_organizing_errors(result["errors"])
        else:
            self.display_organizing_logs(result["logs"])

class MainFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, app):
        super().__init__(master)
        self.setup_layout()

        self.app = app
        self.logs_frame = LogsFrame(self, app)
        self.settings_frame = SettingsFrame(self, app)
        self.target_folder_frame = TargetFolderFrame(self, app)

        self.title_widget = customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6, font=(app_font, 20, "bold"))
        self.title_widget.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10), sticky="ew")
        self.run_app_button = customtkinter.CTkButton(self, text="Start Organization", font=(app_font, 20, "bold"), fg_color="#315CC8", command=self.app.run_application)
        self.run_app_button.grid(row=5, column=0, columnspan=2, sticky="nsew",padx=10,pady=5)
        self.export_logs_button = customtkinter.CTkButton(self, text="Export logs", font=(app_font, 15, "bold"), fg_color="gray20", command=self.export_logs_button_command, state="disabled")
        self.export_logs_button.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)

    def setup_layout(self):
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=6)
        self.grid_rowconfigure(2, weight=6)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=0)
        self.grid(row=0, column=0, columnspan=2, sticky="nsew",padx=10, pady=10)
    
    def export_logs_button_command(self):
        selected_folder = customtkinter.filedialog.askdirectory(title="Where do you want to save the log file?")
        if(selected_folder != ""):
            file_name = export_logs(selected_folder, self.app.logs)
            self.logs_frame.update_logs("Log export successful")
            message = f'Log file successfully exported: {file_name}'
            CTkMessagebox(title="Info", message=message)
        else:
            error_message = 'You must select a folder to save the log file in!!!'
            CTkMessagebox(title="Error", message=error_message, icon="cancel")
            self.logs_frame.update_logs("Export error: No folder set")

class LogsFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="#161616", orientation="vertical")
        self.app = app

        self.grid_columnconfigure(0, weight=1)
        self.grid(row=1, column=1, rowspan=3, sticky="nsew", padx=10, pady=10)

        self.log_text_color = "#1AE9D8"
        self.title = "Activity Logs"
        self.default_logs_text = "No activity yet. \nConfigure settings and start organizing!"

        self.title_widget = customtkinter.CTkLabel(self, text=self.title, corner_radius=6, font=(app_font, 17, "bold"))
        self.default_logs_label_widget = customtkinter.CTkLabel(self, text=self.default_logs_text, corner_radius=6, font=(app_font, 12, "bold"), text_color="gray")
        self.title_widget.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")
        self.default_logs_label_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=(1, 0), sticky="ew")

    def update_logs(self, log_message, folder_log=False):
        final_log_message = f"[{datetime.now().strftime('%H:%M:%S')}] {log_message}"
        if len(self.app.logs) == 0:
            self.default_logs_label_widget.configure(text=final_log_message, text_color=self.log_text_color, anchor='w')
            self.app.enable_export_button()
        else:
            new_label = customtkinter.CTkLabel(self, text=final_log_message, corner_radius=6, font=(app_font, 12, "bold"), text_color=self.log_text_color, anchor='w')
            new_label.grid(row=len(self.app.logs)+1, column=0, columnspan=3, padx=10, pady=(1, 0), sticky='ew')
            
        if folder_log:
            log_with_full_folder_path = f"[{datetime.now().strftime('%H:%M:%S')}] {log_message[log_message.rfind(":"):]}{self.app.folder_path}"
            self.app.logs.append(log_with_full_folder_path)
        else:
            self.app.logs.append(final_log_message)
        self.scroll_down()

    def scroll_down(self):
        self.after(10, self._parent_canvas.yview_moveto, 1.0)

class SettingsFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="#353535")
        self.app = app
        self.radio_buttons = []
        self.categories_frame = CategoriesFrame(self, self.app)

        self.setup_layout()

        self.first_column_title="Select categories"
        self.second_column_title="Operation mode"
        
        self.first_column_widget = customtkinter.CTkLabel(self, text=self.first_column_title, corner_radius=6, font=(app_font, 17, "bold"), fg_color="#161616")
        self.second_column_widget = customtkinter.CTkLabel(self, text=self.second_column_title, corner_radius=6, font=(app_font, 17, "bold"), fg_color="#161616")
        self.first_column_widget.grid(row=0, column=1, padx=10, pady=10 , sticky="ew")
        self.second_column_widget.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.setup_radio_buttons()
    
    def setup_layout(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=10)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1)

    def setup_radio_buttons(self):
        index = 1
        content = ["move files", "copy files"]
        radio_var = customtkinter.IntVar(value=index)
        for i in range (len(content)):
            radio_button = customtkinter.CTkRadioButton(self, text=content[i].capitalize(), variable=radio_var, value=index)
            radio_button.configure(command=lambda rb=radio_button:self.app.update_operation_mode(rb))
            radio_button.grid(row=index, column=1, sticky="ew", padx=20)
            self.radio_buttons.append(radio_button)
            index += 1

class CategoriesFrame(customtkinter.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="#353535")
        self.app = app
        self.checkboxes = []

        self.setup_layout()
        self.setup_checkboxes()

    def setup_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, rowspan=10, sticky="nsew", padx=5, pady=(60.2, 0))
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_rowconfigure(10, weight=1) 

    def setup_checkboxes(self):
        index = 1
        content = {
            "videos": ".mp4., .avi, .mkv, .wmv, .mov, .webm",
            'images': '.png, .jpg, .jpeg, .jfif, .gif, .svg, .webp',
            'documents': '.txt, .docx, .pdf, .csv, .xlsx',
            'audios': '.mp3, .wav, .aiff, .aac',
            'others': "All other extensions"
        }
        for title in content:
            check_var = customtkinter.StringVar(value="on")
            checkbox = customtkinter.CTkCheckBox(self, text=title.capitalize(), variable=check_var, onvalue="on", offvalue="off")
            checkbox.grid(row=index, column=0,padx=10,pady=0,sticky="w")
            checkbox.configure(command=lambda cb=checkbox: self.app.update_selected_categories(cb))
            self.checkboxes.append(checkbox)

            extensions_label = customtkinter.CTkLabel(self, text=content[title], corner_radius=6, font=(app_font, 12, "bold"), text_color="gray", anchor="w")
            extensions_label.grid(row=index+1, column=0, sticky="w")
            index += 2

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

        self.title_widget = customtkinter.CTkLabel(self, text=self.title, corner_radius=6, font=(app_font, 17, "bold"), fg_color="#161616")
        self.button = customtkinter.CTkButton(self, text="Select Folder", font=(app_font, 18), fg_color="gray30", command=self.get_folder_path)
        self.title_widget.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="ew")
        self.button.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=10,pady=10)
        self.button.grid_propagate(False)

    def get_folder_path(self):
        selected_folder = customtkinter.filedialog.askdirectory(title="Select a folder to be organized")
        if(selected_folder != ""):
            self.app.update_folder_path(selected_folder)
            self.show_path_on_ui()
        else:
            error_message = 'You must select a folder to run the application!!!'
            CTkMessagebox(title="Error", message=error_message, icon="cancel")
            self.master.logs_frame.update_logs("Error: No folder selected")

    def show_path_on_ui(self):
        if isinstance(self.app.folder_path, str) and self.app.folder_path != '':
            self.button.configure(text=self.app.folder_path, font=('arial', 12, 'bold'), fg_color="#007180")

app = App()
app.mainloop()

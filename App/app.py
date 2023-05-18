import sqlite3, configparser, os
import tkinter, tkinter.messagebox
import customtkinter as CTk


class Status(CTk.CTkFrame):
    def __init__(self, *args, header_name="command", **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = "Status for " + header_name

        self.header = CTk.CTkLabel(self, text=self.header_name)
        self.header.grid(row=0, column=0, padx=10, pady=10)

        self.radio_button_var = CTk.StringVar(value="")
        self.radio_button_1 = CTk.CTkRadioButton(self, text="On", value="On",
                                                 variable=self.radio_button_var)
        self.radio_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.radio_button_2 = CTk.CTkRadioButton(self, text="Off", value="Off",
                                                 variable=self.radio_button_var)
        self.radio_button_2.grid(row=2, column=0, padx=10, pady=10)

    def set_value(self, selection):
        """ selects the corresponding radio button, selects nothing if no corresponding radio button """
        self.radio_button_var.set(selection)

    def get_value(self):
        """ returns selected value as a string, returns an empty string if nothing selected """
        return self.radio_button_var.get()


class App(CTk.CTk):
    def __init__(self, title: str, size: str, resizable_: bool = False, mode: str = "System"):
        super().__init__()

        self.config_ = configparser.RawConfigParser()
        if os.path.exists("config.ini") == False:
            with open('config.ini', 'w') as f:
                f.close()
        self.config_.read('config.ini')

        # settings
        self._set_appearance_mode(mode)
        self.geometry(size)
        self.title(title)
        self.resizable(resizable_, resizable_)
        self.on_start()

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.textbox = CTk.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lor\n\n")

        CTk.CTkLabel(master=self, text='').grid(padx=(0, 0))

        self.bot_user = CTk.CTkFrame(master=self, fg_color="transparent")
        self.bot_user.grid(row=1, column=1)

        # self.entry_user = CTk.CTkEntry(master=self.bot_user, width=132).grid(row=1, column=0, padx=(10, 20))

    def on_start(self):
        self.window = CTk.CTkToplevel(self)
        self.window.geometry(f'{630}x{600}')
        self.window.title('команды для работы с D-85:')
        self.window.minsize(height=520, width=372)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # create radio button frames
        self.commands = ['cat', 'dog', 'date', 'report', 'smile', 'vote', 'ctk']
        self.frames = []
        for i in range(len(self.commands)):
            row = 1 if i % 4 == 0 else 2 if i % 4 == 1 else 3 if i % 4 == 2 else 4 if i % 4 == 3 else 5
            self.frames.append(Status(self.window, header_name=self.commands[i]))

            self.frames[i].set_value(self.config_['Status'][self.commands[i]])
            self.frames[i].grid(row=row, column=int(i / 4) + 1, padx=0, pady=0)

        button = CTk.CTkButton(self.window, text='сохранить', command=self.save)
        button.grid(row=1, column=3, padx=0, pady=0)

    def save(self):
        self.config_.read("../config.ini")
        try:
            self.config_.add_section("Status")
        except:
            pass
        for i in range(len(self.commands)):
            self.config_.set("Status", f"{self.commands[i]}",
                             "On" if self.frames[i].get_value() == "" else self.frames[i].get_value())
        with open('../config.ini', 'w') as configfile:
            self.config_.write(configfile)
        self.window.destroy()
        self.window = None


def activate(title: str = "test", size: str = "1089x612", mode: str = "System", **kwargs):
    ''' activate the app '''
    app = App(title=title, size=size, mode=mode, **kwargs)
    app.mainloop()


def open_dialog(title_: str, text_: str):
    window = CTk.CTk()
    window.resizable(False, False)
    dialog = CTk.CTkInputDialog(text=text_, title=title_)
    return dialog.get_input()


if __name__ == '__main__':
    activate(title="D-bot", size=f"{1020 / 2}x{720 / 2}", resizable_=True)

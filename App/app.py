import tkinter, tkinter.messagebox
import customtkinter as CTk
from PIL import Image
import discord


class Status(CTk.CTkFrame):
    def __init__(self, *args, header_name="command_1", **kwargs):
        super().__init__(*args, **kwargs)

        self.header_name = "Status for "+header_name

        self.header = CTk.CTkLabel(self, text=self.header_name)
        self.header.grid(row=0, column=0, padx=10, pady=10)

        self.radio_button_var = CTk.StringVar(value="")

        self.radio_button_1 = CTk.CTkRadioButton(self, text="On", value=True,
                                                           variable=self.radio_button_var)
        self.radio_button_1.grid(row=1, column=0, padx=10, pady=10)
        self.radio_button_2 = CTk.CTkRadioButton(self, text="Off", value=False,
                                                           variable=self.radio_button_var)
        self.radio_button_2.grid(row=2, column=0, padx=10, pady=10)

    def get_value(self):
        """ returns selected value as a string, returns an empty string if nothing selected """
        return self.radio_button_var.get()


class App(CTk.CTk):
    def __init__(self, title: str, size: str, resizable_: bool = False, mode: str = "System"):
        super().__init__()
        # settings
        self._set_appearance_mode(mode)
        self.geometry(size)
        self.title(title)
        self.resizable(resizable_, resizable_)
        self.on_start()

        # configure grid layout (4x4)
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1, 2, 3), weight=1)

        self.textbox = CTk.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lor\n\n")


        CTk.CTkLabel(master=self, text='').grid(padx=(0,0))

        self.bot_user = CTk.CTkFrame(master=self, fg_color="transparent")
        self.bot_user.grid(row=1, column=1)


        # self.entry_user = CTk.CTkEntry(master=self.bot_user, width=132).grid(row=1, column=0, padx=(10, 20))

    def on_start(self):
        window = CTk.CTkToplevel(self)
        window.geometry(f'{630}x{660}')
        window.title('команды для работы с D-85:')
        window.minsize(height=520,width=372)

        # configure grid layout (4x4)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        self.appearance_mode_label = CTk.CTkLabel(master=window, text="Выберете команды для работы с D-85:", anchor="w",
                                                  font=('Roboto', 15))
        self.appearance_mode_label.grid(row=0, column=0)

        # create radio button frames
        self.frames = {}
        for i in range(3):
            self.frames[i] = Status(window, header_name=f"test {i}")
            self.frames[i].grid(row=3 + i, column=0, padx=0, pady=0)

    def value_frame(self, frame, text="Frame value: "):
        print(text+frame.get_value())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        CTk.set_appearance_mode(new_appearance_mode)


def activate(title: str = "test", size: str = "1089x612", mode: str = "System", **kwargs):
    app = App(title=title, size=size, mode=mode, **kwargs)
    app.mainloop()

def open_dialog(title_: str, text_: str):
    window=CTk.CTk()
    window.resizable(False, False)
    dialog = CTk.CTkInputDialog(text=text_, title=title_)
    return dialog.get_input()


if __name__ == '__main__':
    activate(title="D-bot", size=f"{1020/2}x{720/2}", resizable_=True)



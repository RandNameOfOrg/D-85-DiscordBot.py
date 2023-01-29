import customtkinter as CTk
from PIL import Image
import discord


class App(CTk.CTk):
    def __init__(self, title: str, size: str, resizable_: bool = False, bot=None, mode: str = "System"):
        super().__init__()
        # settings
        self._set_appearance_mode(mode)
        self.geometry(size)
        self.title(title)
        self.resizable(resizable_, resizable_)

        CTk.CTkLabel(master=self, text='последние сообщения').grid(padx=(0,))

        self.bot_user = CTk.CTkFrame(master=self, fg_color="transparent")
        self.bot_user.grid(row=0, column=0, padx=(12, 801))
        # self.entry_user = CTk.CTkEntry(master=self.bot_user, width=132).grid(row=1, column=0, padx=(10, 20))


def activate(title: str = "test", size: str = "1089x612", mode: str = "System", bot=None, **kwargs):
    app = App(title=title, size=size, mode=mode, bot=bot, **kwargs)
    app.mainloop()

def open_dialog(title_: str, text_: str):
    window=CTk.CTk()
    window.resizable(False, False)
    dialog = CTk.CTkInputDialog(text=text_, title=title_)
    return dialog.get_input()

# activate(title="Daniil_85-bot logs", size="1089x612")

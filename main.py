import requests
from tkinter import PhotoImage
import customtkinter as ctk
from webbrowser import open_new_tab

from inspector_tab import InspectorTab
from comparator_tab import ComparatorTab

class MainApp(ctk.CTk):
    WND_WIDTH, WND_HEIGHT = 750, 500
    PADDING_X, PADDING_Y = 100, 100
    
    def __init__(self):
        super().__init__()

        self.geometry(f'{self.WND_WIDTH}x{self.WND_HEIGHT}+{self.PADDING_X}+{self.PADDING_Y}')
        self.title("Pbinfo Profile Inspector")
        self.wm_iconbitmap('pbinfo.ico') # must be .ico btw, always

        tab_view = ctk.CTkTabview(self, fg_color='transparent', width = self.WND_WIDTH, height = self.WND_HEIGHT)
        tab_view._segmented_button.configure()
        tab_view.pack()

        tab_1 = tab_view.add('Inspector')
        tab_2 = tab_view.add('Comparator')

        inspector_tab = InspectorTab(tab_1)
        comparator_tab = ComparatorTab(tab_2)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
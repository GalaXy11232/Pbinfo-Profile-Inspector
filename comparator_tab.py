import requests
import customtkinter as ctk
from webbrowser import open_new_tab

from functions import *

class ComparatorTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        master.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight = 1)
        master.columnconfigure((0, 2, 3, 4, 5), weight = 1)

        frame_common = ctk.CTkScrollableFrame(master)
        frame_diff_user1 = ctk.CTkScrollableFrame(master)
        frame_diff_user2 = ctk.CTkScrollableFrame(master)

        user1_entry = ctk.CTkEntry(master, placeholder_text = 'Introdu numele utilizatorului 1')
        user2_entry = ctk.CTkEntry(master, placeholder_text = 'Introdu numele utilizatorului 2')

        common_label = ctk.CTkLabel(master, text = '')
        user1_label = ctk.CTkLabel(master, text = '')
        user2_label = ctk.CTkLabel(master, text = '')

        common_label_number = ctk.CTkLabel(master, text = '')
        user1_label_number = ctk.CTkLabel(master, text = '')
        user2_label_number = ctk.CTkLabel(master, text = '')

        users_button = ctk.CTkButton(
            master = master, 
            text = 'Compara cei 2 utilizatori', 
            command = lambda: 
                update_labels_comm_diff(
                    user1_entry, user2_entry,
                    frame_common, frame_diff_user1, frame_diff_user2, 
                    common_label, user1_label, user2_label, common_label_number, user1_label_number, user2_label_number
                )
        )


        query_user1_entry = ctk.CTkEntry(master, placeholder_text = "Cauta problema pt utilizatorul 1")
        query_user2_entry = ctk.CTkEntry(master, placeholder_text = "Cauta problema pt utilizatorul 2")
        query_user1_label = ctk.CTkLabel(master, text = '')
        query_user2_label = ctk.CTkLabel(master, text = '')
        button_user1 = ctk.CTkButton(master, text = "Cauta", command = lambda: search_problem_by_id(query_user1_entry.get().strip(), user1_entry, query_user1_label))
        button_user2 = ctk.CTkButton(master, text = "Cauta", command = lambda: search_problem_by_id(query_user2_entry.get().strip(), user2_entry, query_user2_label))


        user1_entry.grid(row = 0, column = 0, columnspan = 3, sticky = 'ew', padx = 5, pady = 10)
        user2_entry.grid(row = 0, column = 3, columnspan = 3, sticky = 'ew', padx = 5, pady = 10)
        users_button.grid(row = 1, column = 0, columnspan = 6, sticky = 'n', pady = (0, 25))

        common_label.grid(row = 2, column = 0, columnspan = 2)
        user1_label.grid(row = 2, column = 2, columnspan = 2)
        user2_label.grid(row = 2, column = 4, columnspan = 2)

        frame_common.grid(row = 3, column = 0, columnspan = 2, sticky = 'nsew', padx = 5)
        frame_diff_user1.grid(row = 3, column = 2, columnspan = 2, sticky = 'nsew', padx = 5)
        frame_diff_user2.grid(row = 3, column = 4, columnspan = 2, sticky = 'nsew', padx = 5)

        common_label_number.grid(row = 4, column = 0, columnspan = 2, pady = (5, 25))
        user1_label_number.grid(row = 4, column = 2, columnspan = 2, pady = (5, 25))
        user2_label_number.grid(row = 4, column = 4, columnspan = 2, pady = (5, 25))

        query_user1_entry.grid(row = 5, column = 0, columnspan = 3, sticky = 'ew', padx = 5, pady = (0, 10))
        query_user2_entry.grid(row = 5, column = 3, columnspan = 3, sticky = 'ew', padx = 5, pady = (0, 10))
        button_user1.grid(row = 6, column = 0, columnspan = 3)
        button_user2.grid(row = 6, column = 3, columnspan = 3)
        query_user1_label.grid(row = 7, column = 0, columnspan = 3)
        query_user2_label.grid(row = 7, column = 3, columnspan = 3)

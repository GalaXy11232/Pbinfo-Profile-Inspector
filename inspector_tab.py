import requests
import customtkinter as ctk
from webbrowser import open_new_tab

from functions import *

class InspectorTab(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        master.rowconfigure((0, 2, 5, 6), weight = 1)
        master.columnconfigure((0, 1, 2, 3), weight = 1)

        frame = ctk.CTkScrollableFrame(master)
        frame_label = ctk.CTkLabel(master, text = "Probleme rezolvate", font = ("Times New Roman", 25, 'bold'))

        frame_tried = ctk.CTkScrollableFrame(master)
        frame_tried_label = ctk.CTkLabel(master, text = "Probleme încercate", font = ("Times New Roman", 25, 'bold'))

        solved_num_label = ctk.CTkLabel(master, text = '')
        tried_num_label = ctk.CTkLabel(master, text = '')

        user_entry = ctk.CTkEntry(master, placeholder_text = "si daca nu vreau ce faci")
        user_button = ctk.CTkButton(
            master, 
            text = "Cauta", 
            command = lambda: search_query(user_entry.get(), frame, frame_tried, solved_label = solved_num_label, tried_label = tried_num_label)
        )

        problem_entry = ctk.CTkEntry(master, placeholder_text = 'ID-ul sau numele problemei')
        searched_problem_label = ctk.CTkLabel(master, text = "")
        search_problem_button = ctk.CTkButton(
            master, 
            text = "Cauta", 
            command = lambda: 
                search_problem_by_id(problem_entry.get(), user_entry, searched_problem_label)
        )


        user_entry.grid(row = 0, column = 0, columnspan = 3, sticky = 'ew', padx = 5)
        user_button.grid(row = 0, column = 3, padx = 5)

        frame_label.grid(row = 1, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady = 10)
        frame_tried_label.grid(row = 1, column = 2, columnspan = 2, sticky = 'ew', padx = 5, pady = 10)

        frame.grid(row = 2, column = 0, columnspan = 2, sticky = 'nsew', padx = 5)
        frame_tried.grid(row = 2, column = 2, columnspan = 2, sticky = 'nsew', padx = 5)

        solved_num_label.grid(row = 3, column = 0, columnspan = 2, padx = 5)
        tried_num_label.grid(row = 3, column = 2, columnspan = 2, padx = 5)

        ctk.CTkLabel(master, text = "Caută o problemă anume", font = ('Times New Roman', 20, 'bold')).grid(row = 4, column = 0, columnspan = 3, sticky = 'ws', padx = 5)
        problem_entry.grid(row = 5, column = 0, columnspan = 3, sticky = 'ews')
        search_problem_button.grid(row = 5, column = 3, sticky = 's')
        searched_problem_label.grid(row = 6, column = 0, columnspan = 4, sticky = 'n')

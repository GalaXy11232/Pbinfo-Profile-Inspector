import requests
from tkinter import PhotoImage
import customtkinter as ctk
from webbrowser import open_new_tab
#pyinstaller --onefile --noconsole --add-data="./pbinfo.ico:." main.py

WND_WIDTH, WND_HEIGHT = 750, 500
PADDING_X, PADDING_Y = 100, 100

HEADERS = {
    'Host': 'www.pbinfo.ro',
    'Referer': 'https://www.pbinfo.ro/profil/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def _is_string_number(string: str) -> bool:
    string = str(string)
    if string[0] == '0': 
        return False # numbers cant start with 0
    for ch in string:
        if not ch.isdigit(): 
            return False
    return True

def return_solved_and_tried_problems(username) -> list:
    session = requests.Session()
    session.headers.update(HEADERS)

    url_get = f"https://www.pbinfo.ro/ajx-module/profil/json-jurnal.php?user={username}"
    raw_response = session.get(url_get)

    resp = raw_response.json()['content']
    solved = {}
    tried = {}

    for each in resp:
        if each['scor'] == 100 and each['id'] not in solved.keys():
            solved[each['id']] = each['denumire']
    
    # Gather problems that dont have 100p
    for each in resp:
        if each['scor'] != 100 and each['id'] not in list(tried.keys()) + list(solved.keys()):
            tried[each['id']] = each['denumire']

    print(f'{len(tried)} probleme diferite incercate')
    return solved, tried

def _change_to_entry_label(label: ctk.CTkLabel, text, url):
    label.configure(text = text)
    label.bind('<Button-1>', lambda e: open_new_tab(url))
    label.bind('<Enter>', lambda e: label.configure(font = ('', 12, 'underline'), cursor = 'hand2'))
    label.bind('<Leave>', lambda e: label.configure(font = ('', 12), cursor = 'arrow'))

def _problem_entry_label(root, pid, name) -> ctk.CTkLabel:
    problem_url = f'https://www.pbinfo.ro/probleme/{pid}/{name}'
    label = ctk.CTkLabel(root, text = f'#{pid} {name}', font = ('', 12))
    label.bind('<Button-1>', lambda e: open_new_tab(problem_url))
    label.bind('<Enter>', lambda e: label.configure(font = ('', 12, 'underline'), cursor = 'hand2'))
    label.bind('<Leave>', lambda e: label.configure(font = ('', 12), cursor = 'arrow'))

    return label


def search_problem_by_id(problem_entry, user_entry: ctk.CTkEntry, solved_dict: dict, tried_dict: dict, label: ctk.CTkLabel):
    ## Reset label configurations first
    label.unbind('<Button-1>')
    label.unbind('<Enter>')
    label.unbind('<Leave>')

    pid = None
    if _is_string_number(problem_entry):
        pid = int(problem_entry)
    else:
        for key, value in list(solved_dict.items()) + list(tried_dict.items()):
            if value.lower() == problem_entry:
                pid = key
                break

    if pid and pid in list(solved_dict.keys()) + list(tried_dict):
        name = user_entry.get()
        if pid in solved_dict.keys():
            _change_to_entry_label(label, f'Rezolvată -> #{pid} {solved_dict[int(pid)]}', f'https://www.pbinfo.ro/solutii/user/{name}/problema/{pid}/{solved_dict[int(pid)].lower()}')
        elif pid in tried_dict.keys():
            _change_to_entry_label(label, f'Încercată -> #{pid} {tried_dict[int(pid)]}', f'https://www.pbinfo.ro/solutii/user/{name}/problema/{pid}/{tried_dict[int(pid)].lower()}')
    else:
        label.configure(text = 'Nicio sursă găsită.')


def search_query(username, frame: ctk.CTkScrollableFrame, frame_tried: ctk.CTkScrollableFrame, **kwargs) -> None:
    global solved, tried
    solved, tried = return_solved_and_tried_problems(username)

    # Clear existing labels inside frames
    for wd in frame.winfo_children() + frame_tried.winfo_children():
        wd.destroy()
    
    for each in solved.keys():
        _problem_entry_label(frame, each, solved[each]).pack(anchor = 'w')
    for each in tried.keys():
        _problem_entry_label(frame_tried, each, tried[each]).pack(anchor = 'w')
    
    # Resolve **kwargs
    solved_label, tried_label = kwargs.get('solved_label', None), kwargs.get('tried_label', None)
    if solved_label:
        kwargs['solved_label'].configure(text = f'{len(solved)} probleme rezolvate.')
    if tried_label:
        kwargs['tried_label'].configure(text = f'{len(tried)} probleme incercate.')



root = ctk.CTk()#fg_color = '#4f006e')
root.geometry(f'{WND_WIDTH}x{WND_HEIGHT}+{PADDING_X}+{PADDING_Y}')
root.title("Pbinfo Profile Inspector")
root.wm_iconbitmap('pbinfo.ico') # must be .ico btw, always

tab_view = ctk.CTkTabview(root, fg_color='transparent', width=WND_WIDTH, height=WND_HEIGHT)
tab_view._segmented_button.configure() # Modify tab buttons
tab_view.pack()

tab_1 = tab_view.add('Inspector')
tab_2 = tab_view.add('Comparator')
# tab_3 = tab_view.add('<nu stiu>')

## ========================= TAB 1 ========================= ###
tab_1.rowconfigure((0, 2, 5, 6), weight = 1)
tab_1.columnconfigure((0, 1, 2, 3), weight = 1)

frame = ctk.CTkScrollableFrame(tab_1)
frame_label = ctk.CTkLabel(tab_1, text = "Probleme rezolvate", font = ("Times New Roman", 25, 'bold'))

frame_tried = ctk.CTkScrollableFrame(tab_1)
frame_tried_label = ctk.CTkLabel(tab_1, text = "Probleme încercate", font = ("Times New Roman", 25, 'bold'))

solved_num_label = ctk.CTkLabel(tab_1, text = '')
tried_num_label = ctk.CTkLabel(tab_1, text = '')

user_entry = ctk.CTkEntry(tab_1, placeholder_text = "Introdu usernameul utilizatorului dorit")
user_button = ctk.CTkButton(
    tab_1, 
    text = "Cauta", 
    command = lambda: search_query(user_entry.get(), frame, frame_tried, solved_label = solved_num_label, tried_label = tried_num_label)
)

problem_entry = ctk.CTkEntry(tab_1, placeholder_text = 'ID-ul sau numele problemei')
searched_problem_label = ctk.CTkLabel(tab_1, text = "")
search_problem_button = ctk.CTkButton(tab_1, text = "Cauta", command = lambda: search_problem_by_id(problem_entry.get(), user_entry, solved, tried, searched_problem_label))


user_entry.grid(row = 0, column = 0, columnspan = 3, sticky = 'ew', padx = 5)
user_button.grid(row = 0, column = 3, padx = 5)

frame_label.grid(row = 1, column = 0, columnspan = 2, sticky = 'ew', padx = 5, pady = 10)
frame_tried_label.grid(row = 1, column = 2, columnspan = 2, sticky = 'ew', padx = 5, pady = 10)

frame.grid(row = 2, column = 0, columnspan = 2, sticky = 'nsew', padx = 5)
frame_tried.grid(row = 2, column = 2, columnspan = 2, sticky = 'nsew', padx = 5)

solved_num_label.grid(row = 3, column = 0, columnspan = 2, padx = 5)
tried_num_label.grid(row = 3, column = 2, columnspan = 2, padx = 5)

ctk.CTkLabel(tab_1, text = "Caută o problemă anume", font = ('Times New Roman', 20, 'bold')).grid(row = 4, column = 0, columnspan = 3, sticky = 'ws', padx = 5)
problem_entry.grid(row = 5, column = 0, columnspan = 3, sticky = 'ews')
search_problem_button.grid(row = 5, column = 3, sticky = 's')
searched_problem_label.grid(row = 6, column = 0, columnspan = 4, sticky = 'n')


## ========================= TAB 2 ========================= ###
def get_common_and_different_solved_problems(user1, user2):
    global solved_user1, solved_user2
    
    solved_user1, _ = return_solved_and_tried_problems(username = user1)
    solved_user2, _ = return_solved_and_tried_problems(username = user2)

    common = {key: value for key, value in solved_user1.items() if key in solved_user2.keys()}
    diff_1 = {key: value for key, value in solved_user1.items() if key not in solved_user2.keys()} # Ce e in 1 si nu e in 2
    diff_2 = {key: value for key, value in solved_user2.items() if key not in solved_user1.keys()} # Ce e in 2 si nu e in 1
    
    return common, diff_1, diff_2

def update_labels_comm_diff(frame_common, frame_diff1, frame_diff2, *args):
    common, diff1, diff2 = get_common_and_different_solved_problems(user1_entry.get(), user2_entry.get())

    # print(len(diff1))
    for wd in list(frame_diff1.winfo_children()) + \
              list(frame_diff2.winfo_children()) + \
              list(frame_common.winfo_children()):
        wd.destroy()
    
    for each in common.keys(): 
        _problem_entry_label(frame_common, each, common[each]).pack()
    for each in diff1.keys(): 
        _problem_entry_label(frame_diff1, each, diff1[each]).pack()
    for each in diff2.keys(): 
        _problem_entry_label(frame_diff2, each, diff2[each]).pack()
    
    # Resolve *args (labels to be updated)
    args[0].configure(text = "Probleme comune")
    args[1].configure(text = f"Exclusive - {user1_entry.get().upper()}")
    args[2].configure(text = f"Exclusive - {user2_entry.get().upper()}")

    args[3].configure(text = f'{len(common)} probleme găsite.')
    args[4].configure(text = f'{len(diff1)} probleme găsite.')
    args[5].configure(text = f'{len(diff2)} probleme găsite.')

tab_2.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight = 1)
tab_2.columnconfigure((0, 2, 3, 4, 5), weight = 1)

frame_common = ctk.CTkScrollableFrame(tab_2)
frame_diff_user1 = ctk.CTkScrollableFrame(tab_2)
frame_diff_user2 = ctk.CTkScrollableFrame(tab_2)

user1_entry = ctk.CTkEntry(tab_2, placeholder_text = 'Introdu numele utilizatorului 1', textvariable = ctk.StringVar(root, 'tiron_filip'))
user2_entry = ctk.CTkEntry(tab_2, placeholder_text = 'Introdu numele utilizatorului 2', textvariable = ctk.StringVar(root, 'neamtu_matei_constantin'))

common_label = ctk.CTkLabel(tab_2, text = '')
user1_label = ctk.CTkLabel(tab_2, text = '')
user2_label = ctk.CTkLabel(tab_2, text = '')

common_label_number = ctk.CTkLabel(tab_2, text = '')
user1_label_number = ctk.CTkLabel(tab_2, text = '')
user2_label_number = ctk.CTkLabel(tab_2, text = '')

users_button = ctk.CTkButton(
    master = tab_2, 
    text = 'Compara cei 2 utilizatori', 
    command = lambda: 
        update_labels_comm_diff(frame_common, frame_diff_user1, frame_diff_user2, common_label, user1_label, user2_label, common_label_number, user1_label_number, user2_label_number)
)


query_user1_entry = ctk.CTkEntry(tab_2, placeholder_text = "Cauta problema pt utilizatorul 1")
query_user2_entry = ctk.CTkEntry(tab_2, placeholder_text = "Cauta problema pt utilizatorul 2")
query_user1_label = ctk.CTkLabel(tab_2, text = '')
query_user2_label = ctk.CTkLabel(tab_2, text = '')
button_user1 = ctk.CTkButton(tab_2, text = "Cauta", command = lambda: search_problem_by_id(query_user1_entry.get(), user1_entry, solved_user1, {}, query_user1_label))
button_user2 = ctk.CTkButton(tab_2, text = "Cauta", command = lambda: search_problem_by_id(query_user2_entry.get(), user2_entry, solved_user2, {}, query_user2_label))


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

query_user1_entry.grid(row = 5, column = 0, columnspan = 3, sticky = 'ew')
query_user2_entry.grid(row = 5, column = 3, columnspan = 3, sticky = 'ew')
button_user1.grid(row = 6, column = 0, columnspan = 3)
button_user2.grid(row = 6, column = 3, columnspan = 3)
query_user1_label.grid(row = 7, column = 0, columnspan = 3)
query_user2_label.grid(row = 7, column = 3, columnspan = 3)

root.mainloop()
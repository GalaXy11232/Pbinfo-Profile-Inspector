import requests
from tkinter import PhotoImage
import customtkinter as ctk
from webbrowser import open_new_tab

## Headers preferred for requests (User-Agent is necessary though)
HEADERS = {
    'Host': 'www.pbinfo.ro',
    'Referer': 'https://www.pbinfo.ro/profil/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0',
    'X-Requested-With': 'XMLHttpRequest'
}


def _is_string_number(string: str) -> bool:
    """Checks if string represents a valid number. Used to check if problem can be queried by ID, not by name."""
    string = str(string)
    if len(string) == 0: 
        return False

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


def search_problem_by_id(problem_entry, user_entry: ctk.CTkEntry, label: ctk.CTkLabel):
    ## Reset label configurations first
    label.unbind('<Button-1>')
    label.unbind('<Enter>')
    label.unbind('<Leave>')

    name = user_entry.get().strip()
    solved_dict, tried_dict = return_solved_and_tried_problems(name)

    pid = None
    if _is_string_number(problem_entry):
        pid = int(problem_entry)
    else:
        for key, value in list(solved_dict.items()) + list(tried_dict.items()):
            if value.lower() == problem_entry:
                pid = key
                break

    if pid and pid in list(solved_dict.keys()) + list(tried_dict):
        if pid in solved_dict.keys():
            _change_to_entry_label(label, f'Rezolvată -> #{pid} {solved_dict[int(pid)]}', f'https://www.pbinfo.ro/solutii/user/{name}/problema/{pid}/{solved_dict[int(pid)].lower()}')
        elif pid in tried_dict.keys():
            _change_to_entry_label(label, f'Încercată -> #{pid} {tried_dict[int(pid)]}', f'https://www.pbinfo.ro/solutii/user/{name}/problema/{pid}/{tried_dict[int(pid)].lower()}')
    else:
        label.configure(text = 'Nicio sursă găsită.')


def search_query(username, frame: ctk.CTkScrollableFrame, frame_tried: ctk.CTkScrollableFrame, **kwargs) -> None:
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


# == Tab 2 exclusive == #
def get_common_and_different_solved_problems(user1, user2):    
    solved_user1, _ = return_solved_and_tried_problems(username = user1)
    solved_user2, _ = return_solved_and_tried_problems(username = user2)

    common = {key: value for key, value in solved_user1.items() if key in solved_user2.keys()}
    diff_1 = {key: value for key, value in solved_user1.items() if key not in solved_user2.keys()} # Ce e in 1 si nu e in 2
    diff_2 = {key: value for key, value in solved_user2.items() if key not in solved_user1.keys()} # Ce e in 2 si nu e in 1
    
    return common, diff_1, diff_2

def update_labels_comm_diff(user1_entry, user2_entry, frame_common, frame_diff1, frame_diff2, *args):
    common, diff1, diff2 = get_common_and_different_solved_problems(user1_entry.get().strip(), user2_entry.get().strip())

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
    args[1].configure(text = f"Exclusive - {user1_entry.get().strip().upper()}")
    args[2].configure(text = f"Exclusive - {user2_entry.get().strip().upper()}")

    args[3].configure(text = f'{len(common)} probleme găsite.')
    args[4].configure(text = f'{len(diff1)} probleme găsite.')
    args[5].configure(text = f'{len(diff2)} probleme găsite.')
from tkinter import *
from tkinter import ttk
import json
from pathlib import Path


def check_todo():
    todo_path = Path("todo.json")
    if not todo_path.exists():
        with todo_path.open("w", encoding="utf-8") as file:
            default_todolist = {}
            json.dump(default_todolist, file, ensure_ascii=False, indent=2)


def read_todo():
    check_todo()
    ret_lst = []
    todo_path = Path("todo.json")
    if todo_path.exists():
        with open("todo.json", "r", encoding="utf-8") as file:
            loaded_todo = json.load(file)
            for key, val in loaded_todo.items():
                if key or val:
                    ret_lst.append(key)
                else:
                    ret_lst.append("")
            return ret_lst


def save_in_json(text):
    todo_path = Path("todo.json")
    if todo_path.exists():
        with open("todo.json", "r", encoding="utf-8") as file:
            todo_loaded = json.load(file)
            
        todo_loaded[text] = ''

        with open("todo.json", "w", encoding="utf-8") as file:
            json.dump(todo_loaded, file, ensure_ascii=False, indent=2)
            
def delete_from_json(text):
    todo_path = Path("todo.json")
    if todo_path.exists():
        with open("todo.json", "r", encoding="utf-8") as file:
            todo_loaded = json.load(file)
            
        todo_loaded.pop(text,None)

        with open("todo.json", "w", encoding="utf-8") as file:
            json.dump(todo_loaded, file, ensure_ascii=False, indent=2)
            
            
def delete_task():
    selection = todo_listbox.curselection()
    index=selection[0]
    key=todo_listbox.get(index)
    delete_from_json(key)
    todo_list_var.set(read_todo())
    update_checkpoints(checkpoints_frame)

def add_task():
    text = entry.get()
    if text:
        save_in_json(text)
    entry.delete(0, END)
    todo_list_var.set(read_todo())
    update_checkpoints(checkpoints_frame)
    

    
    
def update_checkpoints(checkpoints_frame):
    for widget in checkpoints_frame.winfo_children():
        widget.destroy()
    for text in read_todo():
        enabled = IntVar()
        Checkbutton(checkpoints_frame, text=text, variable=enabled).pack(anchor='w')

root = Tk()
notebook = ttk.Notebook()
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
root.title("Список задач")
root.geometry("400x265+1000+500")

entry = ttk.Entry(frame2)
entry.pack(anchor="nw", padx=3, pady=3)

buttons_frame = ttk.Frame(frame2)
buttons_frame.pack(anchor="nw", padx=3, pady=3)

ttk.Button(buttons_frame, text="Добавить", command=add_task).pack(side=LEFT)
ttk.Button(buttons_frame, text="Удалить", command=delete_task).pack(side=LEFT, padx=8, pady=3)


todo_list_var = Variable(value=read_todo())

todo_listbox = Listbox(frame2,listvariable=todo_list_var)

todo_listbox.pack(anchor=NW, padx=3, pady=5)


notebook.pack(expand=True, fill=BOTH)
notebook.add(frame1, text="Отметка задач")
notebook.add(frame2, text="Создание задач")

checkpoints_frame = ttk.Frame(frame1, borderwidth=1, relief=SOLID, padding=[8, 10])
checkpoints_frame.pack(anchor="n", fill=BOTH, expand=True)
update_checkpoints(checkpoints_frame)


root.mainloop()

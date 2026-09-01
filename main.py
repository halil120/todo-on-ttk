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


root = Tk()
root.title("Список задач")
root.geometry("400x250+1000+500")

entry = ttk.Entry(root)
entry.pack(padx=8, pady=8)



def add_task():
    text = entry.get()
    save_in_json(text)
    entry.delete(0, END)
    todo_list_var.set(read_todo())

Button(root, text="Добавить", command=add_task).pack()



todo_list = read_todo()
todo_list_var = Variable(value=todo_list)

todo_listbox = Listbox(listvariable=todo_list_var)

todo_listbox.pack(anchor=NW, padx=90, pady=5)


root.mainloop()

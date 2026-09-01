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

def add_task():
    text = entry.get()
    if text:
        save_in_json(text)
    entry.delete(0, END)
    todo_list_var.set(read_todo())

root = Tk()
root.title("Список задач")
root.geometry("400x250+1000+500")

entry = ttk.Entry(root)
entry.pack(anchor="nw", padx=3, pady=3)

buttons_frame = Frame(root)
buttons_frame.pack(anchor="nw", padx=3, pady=3)

Button(buttons_frame, text="Добавить", command=add_task).pack(side=LEFT)
Button(buttons_frame, text="Удалить", command=delete_task).pack(side=LEFT, padx=8, pady=3)


todo_list = read_todo()
todo_list_var = Variable(value=todo_list)

todo_listbox = Listbox(listvariable=todo_list_var)

todo_listbox.pack(anchor=NW, padx=3, pady=5)


root.mainloop()

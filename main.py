from tkinter import *
from tkinter import ttk
import json
from pathlib import Path
import sqlite3 as sql


def check_todo_db(cursor, conn):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, name TEXT NOT NULL, enable INTEGER ) "
    )
    conn.commit()


def read_todo_db(cursor, conn):
    check_todo_db(cursor, conn)
    cursor.execute("SELECT name,enable FROM todo")
    return cursor.fetchall()


def text_from_todo_db(todo_list):
    lst = []
    for text, _ in todo_list:
        lst.append(text)
    return lst


def add_in_db(cursor, conn, text):
    cursor.execute("INSERT INTO todo (name, enable) VALUES (?, ?)", (text, 0))
    conn.commit()


def delete_from_db(cursor, conn, text):
    cursor.execute("DELETE FROM todo WHERE name = ?", (text,))
    conn.commit()


def delete_task_db(cursor, conn):
    selection = todo_listbox.curselection()
    if selection:
        index = selection[0]
        key = todo_listbox.get(index)
        delete_from_db(cursor, conn, key)
        todo_list_var.set(text_from_todo_db(read_todo_db(cursor, conn)))
        update_checkpoints_db(cursor, conn, checkpoints_frame)


def add_task_db(cursor, conn):
    text = entry.get()
    if text:
        add_in_db(cursor, conn, text)
    entry.delete(0, END)
    todo_list_var.set(text_from_todo_db(read_todo_db(cursor, conn)))
    update_checkpoints_db(cursor, conn, checkpoints_frame)


def toggle_status_db(cursor, conn, key, var):
    check_todo_db(cursor, conn)
    cursor.execute("UPDATE todo SET enable = ? WHERE name = ?", (1, key))
    conn.commit()


def update_checkpoints_db(cursor, conn, checkpoints_frame):
    for widget in checkpoints_frame.winfo_children():
        widget.destroy()
    for text, flag in read_todo_db(cursor, conn):
        enabled = IntVar(value=1 if flag else 0)
        Checkbutton(
            checkpoints_frame,
            text=text,
            variable=enabled,
            command=lambda t=text, v=enabled: toggle_status_db(cursor, conn, t, v),
        ).pack(anchor="w")


conn = sql.connect("todo.db")
cursor = conn.cursor()

root = Tk()
notebook = ttk.Notebook()
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
root.title("Список задач")
root.geometry("400x265+1000+500")
root.resizable(False, True)
root.iconbitmap(default="icon.ico")

entry = ttk.Entry(frame2)
entry.pack(anchor="nw", padx=3, pady=3)

buttons_frame = ttk.Frame(frame2)
buttons_frame.pack(anchor="nw", padx=3, pady=3)

ttk.Button(
    buttons_frame, text="Добавить", command=lambda: add_task_db(cursor, conn)
).pack(side=LEFT)
ttk.Button(
    buttons_frame, text="Удалить", command=lambda: delete_task_db(cursor, conn)
).pack(side=LEFT, padx=8, pady=3)


todo_list_var = Variable(value=text_from_todo_db(read_todo_db(cursor, conn)))

todo_listbox = Listbox(frame2, listvariable=todo_list_var)

todo_listbox.pack(anchor=NW, padx=3, pady=5)


notebook.pack(expand=True, fill=BOTH)
notebook.add(frame1, text="Отметка задач")
notebook.add(frame2, text="Создание задач")

checkpoints_frame = ttk.Frame(frame1, borderwidth=1, relief=SOLID, padding=[8, 10])
checkpoints_frame.pack(anchor="n", fill=BOTH, expand=True)
update_checkpoints_db(cursor, conn, checkpoints_frame)


root.mainloop()

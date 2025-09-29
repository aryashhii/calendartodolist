import tkinter as tk
import json, os
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar
import sys, os
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "tasks.json")
if os.path.exists(DATA_FILE):
    with open(DATA_FILE,"r") as f:
        tasks_by_date = json.load(f)
else:
    tasks_by_date = {}    
def save_tasks():
    with open(DATA_FILE,"w") as f:
        json.dump(tasks_by_date,f)
def add_task(date):
    task = simpledialog.askstring("Add task",f"enter task for {date}:")
    if task:
        tasks_by_date.setdefault(date,[]).append(task)
        save_tasks()
        messagebox.showinfo("Task added",f"task added for {date}:")
def show_tasks():
    if not tasks_by_date:
        messagebox.showinfo("Tasks","No tasks added yet")
        return
    task_window = tk.Toplevel(root)
    task_window.configure(bg="yellow")
    task_window.title("ALL TASKS")
    task_window.geometry("300x400")    
    tk.Label(task_window, text="task list", font=("Arial",20),bg="violet").pack(pady=15)
    def refresh_window():
        task_window.destroy()
        show_tasks()
    for date in sorted(tasks_by_date.keys()):
        tk.Label(task_window,text=f"{date}",font=("Arial",14,"bold"),bg="pink").pack(anchor="w",padx=15)
        for task in tasks_by_date[date]:
            var = tk.BooleanVar()
            def remove_task(d=date,t=task,v=var):
                if v.get():
                    tasks_by_date[d].remove(t)
                    if not tasks_by_date[d]:
                        del tasks_by_date[d]
                    save_tasks()    
                    refresh_window()
            cb = tk.Checkbutton(task_window,text=task,variable=var,command=lambda d=date,t=task,v=var: remove_task(d,t,v),bg="pink", activebackground="light pink")
            cb.pack(anchor="w",padx=20)         
def on_date_select(event):
    selected_date = cal.get_date()
    add_task(selected_date)
root = tk.Tk()
root.configure(bg="pink")
root.title("Calendar To-Do List")
root.geometry("400x400")  
cal = Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd', background="blue")
cal.pack(pady=20)
cal.bind("<<CalendarSelected>>",on_date_select)
task_btn = tk.Button(root,text="view all tasks",command =show_tasks)
task_btn.pack(pady=10)
root.mainloop()   

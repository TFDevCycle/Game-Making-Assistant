import json
import tkinter as tk

class Task:
    def __init__(self, description, completed=False):
        self.description = description
        self.completed = completed

    def __repr__(self):
        status = "[X]" if self.completed else "[ ]"
        return f"{status} {self.description}"

class TodoList:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.update_listbox()

    def remove_task(self, task):
        self.tasks.remove(task)
        self.update_listbox()

    def mark_task_complete(self, task):
        task.completed = True
        self.update_listbox()

    def mark_task_incomplete(self, task):
        task.completed = False
        self.update_listbox()

    def save(self, filename):
        data = {"name": self.name, "tasks": [task.__dict__ for task in self.tasks]}
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        self.name = data["name"]
        self.tasks = [Task(**task_data) for task_data in data["tasks"]]
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, str(task))

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Development TODO List")

        self.todo_list = TodoList("Game Development TODO List")

        self.add_task_entry = tk.Entry(self.master)
        self.add_task_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.remove_task_button = tk.Button(self.master, text="Remove Task", command=self.remove_task)
        self.complete_task_button = tk.Button(self.master, text="Mark Task Complete", command=self.mark_task_complete)
        self.incomplete_task_button = tk.Button(self.master, text="Mark Task Incomplete", command=self.mark_task_incomplete)
        self.save_button = tk.Button(self.master, text="Save List", command=self.save)
        self.load_button = tk.Button(self.master, text="Load List", command=self.load)

        self.listbox = tk.Listbox(self.master, width=50)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        self.add_task_entry.grid(row=0, column=0)
        self.add_task_button.grid(row=0, column=1)
        self.remove_task_button.grid(row=1, column=0)
        self.complete_task_button.grid(row=1, column=1)
        self.incomplete_task_button.grid(row=1, column=2)
        self.save_button.grid(row=2, column=0)
        self.load_button.grid(row=2, column=1)

        self.listbox.grid(row=3, column=0, columnspan=3)

    def add_task(self):
        description = self.add_task_entry.get()
        task = Task(description)
        self.todo_list.add_task(task)
        self.add_task_entry.delete(0, tk.END)

    def remove_task(self):
        selection = self.listbox.curselection()
        if selection:
            task = self.todo_list.tasks[selection[0]]
            self.todo_list.remove_task(task)

    def mark_task_complete(self):
        selection = self.listbox.curselection()
        if selection
        task = self.todo_list.tasks[selection[0]]
        self.todo_list.mark_task_complete(task)

    def mark_task_incomplete(self):
        selection = self.listbox.curselection()
        if selection:
           task = self.todo_list.tasks[selection[0]]
           self.todo_list.mark_task_incomplete(task)

    def save(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".json")
        if filename:
           self.todo_list.save(filename)

    def load(self):
        filename = tk.filedialog.askopenfilename(defaultextension=".json")
        if filename:
           self.todo_list.load(filename)

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
           task = self.todo_list.tasks[selection[0]]
           if task.completed:
              self.complete_task_button.config(state=tk.DISABLED)
              self.incomplete_task_button.config(state=tk.NORMAL)
           else:
              self.complete_task_button.config(state=tk.NORMAL)
              self.incomplete_task_button.config(state=tk.DISABLED)

root = tk.Tk()
app = App(root)
root.mainloop()

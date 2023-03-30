import tkinter as tk
import os

class Program:
    def __init__(self, name, category, path):
        self.name = name
        self.category = category
        self.path = path

class ProgramFrame:
    def __init__(self, master):
        self.master = master
        self.master.title("Overview")

        self.programs = [
            Program("Map Editor", "Development", "modules\map-editor.py"),
            Program("Sprite Maker", "Development", "modules\sprite-maker.py"),
            Program("Tileset Creator", "Development", "modules\tileset-creator.py"),
            Program("GitHub Repo",  "Tools", "programs\GitHub-Repo.py"),
            Program("ToDo",  "Tools", "programs\Todo.py"),
            Program("GameBoy",  "Emulator", "emulators\emulator.py"),
        ]

        self.category_var = tk.StringVar()
        self.category_var.set("All")
        self.category_option_menu = tk.OptionMenu(self.master, self.category_var, "All", "Development", "Tools", "Emulator", command=self.filter_programs)

        self.program_listbox = tk.Listbox(self.master, width=50)
        self.program_listbox.bind("<Double-Button-1>", self.on_program_selected)

        self.category_option_menu.pack(padx=5, pady=5)
        self.program_listbox.pack(padx=5, pady=5)

        self.selected_program = None

    def filter_programs(self, category):
        if category == "All":
            filtered_programs = self.programs
        else:
            filtered_programs = [p for p in self.programs if p.category == category]
        self.program_listbox.delete(0, tk.END)
        for p in filtered_programs:
            self.program_listbox.insert(tk.END, p.name)

    def on_program_selected(self, event):
        self.selected_program = None
        selected_program_name = self.program_listbox.get(self.program_listbox.curselection())
        for p in self.programs:
            if p.name == selected_program_name:
                self.selected_program = p
                break
        if self.selected_program and self.selected_program.path.endswith('.py'):
            os.system(f'py {self.selected_program.path}')

# Example usage
root = tk.Tk()
frame = ProgramFrame(root)
root.mainloop()

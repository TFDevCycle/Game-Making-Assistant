import requests
import tkinter as tk
from tkinter import ttk

class GithubRepoViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Github Repo Viewer")

        self.repo_name_label = tk.Label(self.master, text="Repository name:")
        self.repo_name_entry = tk.Entry(self.master)
        self.repo_name_entry.focus_set()
        self.get_repo_button = tk.Button(self.master, text="Get Repo Info", command=self.get_repo_info)

        self.repo_info_treeview = ttk.Treeview(self.master, columns=("Name", "Description", "URL"))
        self.repo_info_treeview.heading("#0", text="ID")
        self.repo_info_treeview.heading("Name", text="Name")
        self.repo_info_treeview.heading("Description", text="Description")
        self.repo_info_treeview.heading("URL", text="URL")
        self.repo_info_treeview.column("#0", width=0, stretch=tk.NO)
        self.repo_info_treeview.column("Name", width=200, stretch=tk.YES)
        self.repo_info_treeview.column("Description", width=400, stretch=tk.YES)
        self.repo_info_treeview.column("URL", width=300, stretch=tk.YES)

        self.repo_name_label.grid(row=0, column=0)
        self.repo_name_entry.grid(row=0, column=1)
        self.get_repo_button.grid(row=0, column=2)

        self.repo_info_treeview.grid(row=1, column=0, columnspan=3)

    def get_repo_info(self):
        self.repo_info_treeview.delete(*self.repo_info_treeview.get_children())
        repo_name = self.repo_name_entry.get().strip()
        if repo_name:
            response = requests.get(f"https://api.github.com/repos/{repo_name}")
            if response.ok:
                repo_info = response.json()
                self.repo_info_treeview.insert("", tk.END, text="1", values=(repo_info["name"], repo_info["description"], repo_info["html_url"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = GithubRepoViewer(root)
    root.mainloop()

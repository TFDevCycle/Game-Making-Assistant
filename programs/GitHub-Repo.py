import requests
import tkinter as tk
from tkinter import ttk
import os

class GithubRepoViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Github Repo Viewer")

        self.repo_name_label = tk.Label(self.master, text="Repository name:")
        self.repo_name_entry = tk.Entry(self.master)
        self.repo_name_entry.focus_set()
        self.get_repo_button = tk.Button(self.master, text="Get Repo Info", command=self.get_repo_info)

        self.repo_listbox = tk.Listbox(self.master)
        self.repo_listbox.bind("<Double-Button-1>", self.on_repo_selected)

        self.file_listbox = tk.Listbox(self.master)
        self.file_listbox.bind("<Double-Button-1>", self.on_file_selected)
        self.current_path = ""

        self.repo_name_label.grid(row=0, column=0)
        self.repo_name_entry.grid(row=0, column=1)
        self.get_repo_button.grid(row=0, column=2)

        self.repo_listbox.grid(row=1, column=0, padx=5, pady=5)
        self.file_listbox.grid(row=1, column=1, padx=5, pady=5)

        self.download_button = tk.Button(self.master, text="Download File", command=self.download_file, state=tk.DISABLED)
        self.download_button.grid(row=2, column=1)

        self.back_button = tk.Button(self.master, text="Back", command=self.go_back, state=tk.DISABLED)
        self.back_button.grid(row=2, column=0)

    def get_repo_info(self):
        self.repo_listbox.delete(0, tk.END)
        self.file_listbox.delete(0, tk.END)
        repo_name = self.repo_name_entry.get().strip()
        if repo_name:
            response = requests.get(f"https://api.github.com/repos/{repo_name}/contents/")
            if response.ok:
                repo_info = response.json()
                for item in repo_info:
                    if item["type"] == "dir":
                        self.repo_listbox.insert(tk.END, item["name"])
                self.current_path = ""
                self.download_button.config(state=tk.DISABLED)
                self.back_button.config(state=tk.DISABLED)

    def on_repo_selected(self, event):
        self.file_listbox.delete(0, tk.END)
        repo_name = self.repo_name_entry.get().strip()
        if repo_name:
            selected_repo = self.repo_listbox.get(self.repo_listbox.curselection())
            self.current_path = f"{selected_repo}/"
            response = requests.get(f"https://api.github.com/repos/{repo_name}/contents/{selected_repo}")
            if response.ok:
                repo_info = response.json()
                for item in repo_info:
                    if item["type"] == "file":
                        self.file_listbox.insert(tk.END, item["name"])
                self.download_button.config(state=tk.DISABLED)
                self.back_button.config(state=tk.NORMAL)

    def on_file_selected(self, event):
        self.download_button.config(state=tk.NORMAL)

    def download_file(self):
        repo_name = self.repo_name_entry.get().strip()
        selected_file = self.file_listbox.get(self.file_listbox.curselection())
        response = requests.get(f"https://raw.githubusercontent.com/{repo_name}/main/{self.current_path}{selected_file}")
        if response.ok:
            file_content = response.content
            download_dir = "outputs\\files"  # Change this to your preferred download directory
            file_path = os.path.join(download_dir, selected_file)
            with open(file_path, "wb") as f:
                f.write(file_content)
            os.startfile(file_path)


    def go_back(self):
        repo_name = self.repo_name_entry.get().strip()
        if repo_name:
            if "/" in self.current_path:
                # remove the last directory from the current path
                self.current_path = "/".join(self.current_path.split("/")[:-1]) + "/"
                response = requests.get(f"https://api.github.com/repos/{repo_name}/contents/{self.current_path}")
                if response.ok:
                    self.file_listbox.delete(0, tk.END)
                    repo_info = response.json()
                    for item in repo_info:
                        if item["type"] == "file":
                            self.file_listbox.insert(tk.END, item["name"])
                    if "/" in self.current_path:
                        # enable the back button if we are not at the root directory
                        self.back_button.config(state=tk.NORMAL)
                    else:
                        self.back_button.config(state=tk.DISABLED)
                    self.download_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = GithubRepoViewer(root)
    root.mainloop()


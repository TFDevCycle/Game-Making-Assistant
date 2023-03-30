import tkinter as tk

class SpriteMaker:
    def __init__(self):
        self.width = 160
        self.height = 144
        self.selected_color = 0

        self.master = tk.Tk()
        self.master.title("Game Boy Sprite Maker")
        # create canvas tk.Frame
        canvas_frame = tk.Frame(self.master)
        canvas_frame.grid(row=0, column=0, padx=5, pady=5, rowspan=3)

        self.canvas = tk.Canvas(canvas_frame, width=128, height=128, bg="white")
        self.canvas.pack(expand=True, fill="both")

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

        # create palette tk.Frame
        palette_frame = tk.Frame(self.master)
        palette_frame.grid(row=0, column=1, padx=5, pady=5, sticky="n")

        self.color = 1

        self.palette = ["#FFFFFF", "#C0C0C0", "#606060", "#000000"]
        self.palette_labels = []
        for i, color in enumerate(self.palette):
            label = tk.Label(palette_frame, bg=color, width=2, height=1)
            label.grid(row=0, column=i, padx=5, pady=5)
            label.bind("<Button-1>", lambda event, index=i: self.on_palette_click(index))
            self.palette_labels.append(label)

        # create save button
        save_button_frame = tk.Frame(self.master)
        save_button_frame.grid(row=1, column=1, padx=5, pady=5, sticky="n")

        save_label = tk.Label(save_button_frame, text="Save as:")
        save_label.pack(side="left")

        self.save_entry = tk.Entry(save_button_frame, width=10)
        self.save_entry.pack(side="left", padx=5)

        self.save_button = tk.Button(save_button_frame, text="Save", command=self.save_sprite)
        self.save_button.pack(side="left")

        # create grid button
        grid_button_frame = tk.Frame(self.master)
        grid_button_frame.grid(row=3, column=1, padx=5, pady=5, sticky="n")

        self.grid_button = tk.Button(grid_button_frame, text="Toggle Grid", command=self.toggle_grid)
        self.grid_button.pack(expand=True, fill="both")

        self.draw_grid()

        self.master.mainloop()

    def draw_grid(self):
        self.canvas.delete("grid")
        for x in range(0, 129, 8):
            self.canvas.create_line(x, 0, x, 128, tag="grid")
        for y in range(0, 129, 8):
            self.canvas.create_line(0, y, 128, y, tag="grid")

    def on_palette_click(self, index):
        self.color = index


    def on_canvas_click(self, event):
        x = event.x // 8
        y = event.y // 8
        self.canvas.create_rectangle(x * 8, y * 8, (x + 1) * 8, (y + 1) * 8, fill=self.palette[self.color], tag="pixel")

    def on_canvas_drag(self, event):
        x = event.x // 8
        y = event.y // 8
        self.canvas.create_rectangle(x * 8, y * 8, (x + 1) * 8, (y + 1) * 8, fill=self.palette[self.color], tag="pixel")


    def toggle_grid(self):
        if self.canvas.itemcget("grid", "state") == "normal":
            self.canvas.itemconfigure("grid", state="hidden")
        else:
            self.canvas.itemconfigure("grid", state="normal")

    def save_sprite(self):
        filename = self.save_entry.get()
        pixels = []
        for y in range(16):
            row = []
            for x in range(16):
                item = self.canvas.find_closest(x * 8 + 4, y * 8 + 4)
                if "pixel" in self.canvas.gettags(item):
                    color = self.palette.index(self.canvas.itemcget(item, "fill"))
                    row.append(color)
                else:
                    row.append(0)
            pixels.append(row)

        with open(filename, "w") as f:
            for row in pixels:
                f.write("".join([str(x) for x in row]) + "\n")


if __name__ == "__main__":
    editor = SpriteMaker()
import pyboy
import tkinter as tk

class MapEditor:
    def __init__(self):
        self.pyboy = pyboy.PyBoy("emulators\\game.gb")
        self.width = 10
        self.height = 20
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        self.selected_tile = 0

        self.master = tk.Tk()
        self.master.title("Game Boy Map Editor")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.canvas = tk.Canvas(self.master, width=self.width * 16, height=self.height * 16, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=4)

        self.palette = ["#FFFFFF", "#C0C0C0", "#606060", "#000000"]
        self.palette_labels = []
        for i, color in enumerate(self.palette):
            label = tk.Label(self.master, bg=color, width=2, height=1)
            label.grid(row=i, column=1, padx=5, pady=5)
            label.bind("<Button-1>", lambda event, index=i: self.on_palette_click(index))
            self.palette_labels.append(label)

        self.tile_label = tk.Label(self.master, text="Selected Tile: 0")
        self.tile_label.grid(row=0, column=2, padx=5, pady=5)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_map)
        self.save_button.grid(row=len(self.palette) + 1, column=1, columnspan=2, padx=5, pady=5)

        self.draw_tiles()

    def on_closing(self):
        self.save_map()
        self.pyboy.stop()
        self.master.destroy()

    def draw_tiles(self):
        self.canvas.delete("all")
        for x in range(self.width):
            for y in range(self.height):
                tile = self.tiles[x][y]
                color = self.palette[tile]
                self.canvas.create_rectangle(x * 16, y * 16, (x + 1) * 16, (y + 1) * 16, fill=color)

    def on_palette_click(self, index):
        self.selected_tile = index
        self.tile_label.config(text=f"Selected Tile: {index}")

    def save_map(self):
        with open("map.txt", "w") as f:
            for y in range(self.height):
                for x in range(self.width):
                    f.write(str(self.tiles[x][y]))
                f.write("\n")

    def run(self):
        while not self.pyboy.tick():
            self.pyboy.tick()
        self.pyboy.stop()
        self.pyboy = pyboy.PyBoy("emulators/game.gb")
        self.pyboy.set_emulation_speed(0)
        self.pyboy.get_screen_buffer()
        self.pyboy.load_memory(0x8000, [self.selected_tile for y in range(0x1800)])
        self.pyboy.tick()

if __name__ == "__main__":
    editor = MapEditor()
    editor.run()
    editor.master.mainloop()

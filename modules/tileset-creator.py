import tkinter as tk

class TilesetCreator:
    def __init__(self):
        self.width = 128
        self.height = 128
        self.tiles = [[0 for y in range(self.height)] for x in range(self.width)]
        self.selected_tile = 0

        self.master = tk.Tk()
        self.master.title("Game Boy Tileset Creator")

        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg="white")
        self.canvas.grid(row=0, column=0, rowspan=4)

        self.palette = ["#FFFFFF", "#C0C0C0", "#606060", "#000000"]
        self.palette_labels = []
        for i, color in enumerate(self.palette):
            label = tk.Label(self.master, bg=color, width=2, height=1)
            label.grid(row=i, column=0, padx=5, pady=5)
            label.bind("<Button-1>", lambda event, index=i: self.on_palette_click(index))
            self.palette_labels.append(label)

        self.tile_label = tk.Label(self.master, text="Selected Tile: 0")
        self.tile_label.grid(row=0, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_tileset)
        self.save_button.grid(row=len(self.palette) + 1, column=0, columnspan=2, padx=5, pady=5)

        self.draw_tiles()

        self.master.mainloop()

    def draw_tiles(self):
        self.canvas.delete("all")
        for x in range(self.width // 8):
            for y in range(self.height // 8):
                tile = []
                for i in range(8):
                    tile.append(self.tiles[x * 8 + i][y * 8:y * 8 + 8])
                self.draw_tile(tile, x, y)

    def draw_tile(self, tile, x, y):
        for i, row in enumerate(tile):
            for j, color in enumerate(row):
                self.canvas.create_rectangle(x * 8 + j, y * 8 + i, x * 8 + j + 1, y * 8 + i + 1, fill=self.palette[color])

    def on_palette_click(self, index):
        self.selected_tile = index
        self.tile_label.config(text=f"Selected Tile: {index}")

    def save_tileset(self):
        with open("tileset.bin", "wb") as f:
            for x in range(self.width // 8):
                for y in range(self.height // 8):
                    tile = []
                    for i in range(8):
                        tile.extend(self.tiles[x * 8 + i][y * 8:y * 8 + 8])
                    f.write(bytes(tile))

if __name__ == "__main__":
    editor = TilesetCreator()

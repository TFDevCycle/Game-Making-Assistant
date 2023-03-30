from PIL import Image
import tkinter as tk
import os


# Convert .txt files to .png files
for filename in os.listdir("outputs\\txt\\"):
    if filename.endswith('.txt'):
        file = filename.split(".")
        with open("outputs\\txt\\" + filename, "r") as f:
            data = f.readlines()

        pixels = []
        for row in data:
            pixels.append([int(p) for p in row.strip()])

        palette = [(255, 255, 255), (192, 192, 192), (96, 96, 96), (0, 0, 0)]

        image = Image.new("RGB", (16, 16))

        for y in range(16):
            for x in range(16):
                color = pixels[y][x]
                image.putpixel((x, y), palette[color])

        image.save("outputs\\img\\" + str(file[0]) + ".png")


class Window:
    def __init__(self):
        # Create the Tkinter window
        self.window = tk.Tk()

        # Define the dimensions of the window
        self.window.geometry("500x250")

        # Create a label to display the list of converted files
        list_label = tk.Label(self.window, text="List of Converted Files", font=("Arial", 16))
        list_label.pack()

        # Create a listbox to display the files
        self.listbox = tk.Listbox(self.window, width=50, font=("Arial", 12))
        self.listbox.pack(pady=10)

        # Loop through all .txt files in the current directory
        for filename in os.listdir("outputs\\txt\\"):
            if filename.endswith('.txt'):
                # Add the filename to the listbox
                self.listbox.insert(tk.END, filename[:-4] + ".png")

        # Start the Tkinter event loop
        self.window.mainloop()


# Create an instance of the window
window = Window()

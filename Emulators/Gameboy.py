import pyboy

gameboy = pyboy.PyBoy("path/to/rom.gb")

while not gameboy.tick():
    pass

gameboy.stop()

import pyboy

gameboy = pyboy.PyBoy("emulators\\game.gb")

while not gameboy.tick():
    pass

gameboy.stop()

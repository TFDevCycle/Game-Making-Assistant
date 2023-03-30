from PIL import Image

def split_image(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        for x in range(0, width, 16):
            for y in range(0, height, 16):
                box = (x, y, x+16, y+16)
                square = img.crop(box)
                square.save(f"{x//16}_{y//16}.png")


split_image("path/to/image.png")

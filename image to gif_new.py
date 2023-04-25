#带透明度的gif合并
import sys
from PIL import Image

fps = 25
input_files = sys.argv[1:]

output_file = "out.gif"
images = [Image.open(file).convert('RGBA') for file in input_files]

width, height = images[0].size

for image in images:
    print("start process:",image)
    for y in range(height):
        for x in range(width):
            r, g, b, a = image.getpixel((x, y))
            if a < 128:
                image.putpixel((x, y), (0, 0, 0, 0))

print("start gif")

gif_writer = Image.new('RGBA', (width, height))

gif_writer.save(output_file, save_all=True,disposal=2, append_images=images, duration=int(1000/fps), loop=0)

print("done")
input()

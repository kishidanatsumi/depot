#带透明度的gif合并
import sys
from PIL import Image

fps = 30
input_files = sys.argv[1:]
sel = 1

output_file = "out.gif"
images = [Image.open(file).convert('RGBA') for file in input_files]

width, height = images[0].size

def contr(x,con):
    y= x + (x - 127)*con/255
    return int(y)

if sel == 1:
    bright=96
    contrast=100
    #亮度
    for image in images:
        print("start process:",image)
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.getpixel((x, y))
                image.putpixel((x, y), (r+bright, g+bright, b+bright, a))

    #对比度
    for image in images:
        print("start process:",image)
        for y in range(height):
            for x in range(width):
                r, g, b, a = image.getpixel((x, y))
                image.putpixel((x, y), (contr(r,contrast),contr(g,contrast),contr(b,contrast), a))

print("start gif")

images[0].save(output_file, save_all=True,optimize=False, append_images=images[1:], duration=1000/fps, loop=0)

print("done")
input()

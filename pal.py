from PIL import Image
import sys
import re

pic_path = sys.argv[1]

input_image = Image.open(pic_path)
width, height = input_image.size

if (re.search(r".*Mouth.*", pic_path)):
    cut_width = width // 2
    cut_height = height // 2
    out_name = "Mouth"
    out_num = 4
else:
    cut_width = width // 2
    cut_height = height // 4
    out_name = "Eye"
    out_num = 8

quadrants = [
    Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for _ in range(out_num)
]

for i in range(int(out_num/2)):
    for j in range(2):
        print (i)
        print (j)
        left = j * cut_width
        top =  i * cut_height
        right = left + cut_width
        bottom = top + cut_height

        image_parts = input_image.crop((left, top, right, bottom))
        quadrants[i*2 + j].paste(image_parts, (0, 0))

for index, out_image in enumerate(quadrants):
    out_image.save(f"{out_name}_{index + 1}.png")


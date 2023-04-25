#简易的gif合并，无透明度，黑底
import imageio
import os
import sys

pic_path = sys.argv[1]

fps = 25

input_images = [os.path.join(pic_path, f) for f in os.listdir(pic_path) if f.endswith('.jpg') or f.endswith('.png')]

imageio.mimsave('animation.gif', [imageio.imread(f) for f in input_images], fps=fps)

print("done")

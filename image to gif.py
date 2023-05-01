#简易的gif合并，无透明度，黑底
import imageio
import os
import sys

input_files = sys.argv[1:]

fps = 25

imageio.mimsave('animation.gif', [imageio.imread(f) for f in input_files], fps=fps)

print("done")

import sys
import os
import re
import cv2
import numpy as np

#将通道贴图放入mask/文件夹，然后对程序拖入原图片
input_path=sys.argv[1:]
#input_path=["./uv_movie_music5046_011_tex_30.png"]

#缩放比率
resize_factor_h = 1
resize_factor_w = 0.5

if not os.path.exists("./out"):  
 os.makedirs("./out")

#处理文件名
def combine(file_list):
    for single in file_list:
        in_name=os.path.basename(single)
        #通道贴图文件夹
        mask_name="./mask/"+re.sub("\.png","",in_name)+"_mask.png"
        #输出贴图文件夹
        out_name="./out/"+re.sub("\.png","",in_name)+"_out.png" 
        #
        input_bundle=[in_name,mask_name,out_name]
        alphacomb(input_bundle)
    return

#合并alpha通道
def alphacomb(input_list):
#input_list[0]:目标文件
#input_list[1]:alpha通道
#input_list[2]:输出文件
    img = cv2.imread(input_list[0])
    alpha = cv2.imread(input_list[1], cv2.IMREAD_GRAYSCALE)
    alpha = cv2.resize(alpha, (img.shape[1], img.shape[0]))
    out_image = cv2.merge((img[:,:,0], img[:,:,1], img[:,:,2], alpha))
    (width, length, depth) = out_image.shape
    out_image=cv2.resize(out_image, (int(length*resize_factor_h),int(width*resize_factor_w)), dst=None,fx=None,fy=None, interpolation = cv2.INTER_LINEAR)

    if cv2.countNonZero(alpha) == 0:
        print("Output is empty")
        out_image=np.zeros((int(width*resize_factor_w), int(length*resize_factor_h),4), dtype=np.uint8)
        out_image[:,:,3] = 0
        
    cv2.imwrite(input_list[2], out_image)
    print("Output:",input_list[2])
    return

combine(input_path)

print("Done")

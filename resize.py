#图片放缩
import sys
import os
import re
import cv2

input_path=sys.argv[1:]

#缩放比率
resize_factor_h = 1
resize_factor_w = 0.5

if not os.path.exists("./out"):  
 os.makedirs("./out")

#处理文件名
def combine(file_list):
    for single in file_list:
        in_name=os.path.basename(single)
        #输出贴图文件夹
        out_name="./out/"+re.sub("\.png","",in_name)+"_out.png" 
        input_bundle=[in_name,out_name]
        alphacomb(input_bundle)
    return

#合并alpha通道
def alphacomb(input_list):
#input_list[0]:目标文件
#input_list[1]:输出文件
    img = cv2.imread(input_list[0])
    (width, length, depth) = img.shape
    out_image=cv2.resize(img, (int(length*resize_factor_h),int(width*resize_factor_w)), dst=None,fx=None,fy=None, interpolation = cv2.INTER_LINEAR)
    cv2.imwrite(input_list[1], out_image)

    print("Output:",input_list[1])
    return

combine(input_path)

print("Done")

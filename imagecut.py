import cv2
import numpy as np
import os
import sys

#分割尺寸
cut_width = 128
cut_length = 128

#将原图沿横向扩展X倍
resize_factor = 1

#是否按行列反向
reverse_x = 0
reverse_y = 1

#读入拖入的文件
pic_path = sys.argv[1]
#pic_path = 'vj_star.png'
#pic_path = pic_path.replace("\\", "/")

pic_name = os.path.basename(pic_path)
pic_target = pic_name + "_out"

print ("Input picture:",pic_path)

#创建文件夹
if not os.path.exists(pic_target):  
 os.makedirs(pic_target)

# 读取要分割的图片与尺寸
pic_in = cv2.imread(pic_path)
(width, length, depth) = pic_in.shape

# 预处理生成0矩阵
pic_out = np.zeros((cut_width, cut_length, depth))

# 计算横纵可以划分的图片个数
num_width = int(width / cut_width)
num_length = int(length / cut_length)
print("Generating",num_width,"x",num_length,"images in folder :",pic_target)

#放缩图片
if resize_factor != 1 :
 pic_in=cv2.resize(pic_in, (length*resize_factor,width), dst=None,fx=None,fy=None, interpolation = cv2.INTER_LINEAR)
 cut_length = cut_length*resize_factor
 cut_width = cut_width*resize_factor


#循环生成图片
if reverse_x == 1 :
    for i in range(0, num_width):
        for j in range(0, num_length):
            pic_out = pic_in[i*cut_width : (i+1)*cut_width, j*cut_length : (j+1)*cut_length, :]
            result_path = pic_target + "/" + '{}_{}_{}.jpg'.format(pic_name,num_width-i-1, num_length-j)
            cv2.imwrite(result_path, pic_out)
            
elif reverse_y == 1:
    for i in range(0, num_width):
        for j in range(0, num_length):
            pic_out = pic_in[i*cut_width : (i+1)*cut_width, j*cut_length : (j+1)*cut_length, :]
            result_path = pic_target + "/" + '{}_{}_{}.jpg'.format(pic_name,i, j+1)
            cv2.imwrite(result_path, pic_out)

else :
    for i in range(0, num_width):
        for j in range(0, num_length):
            pic_out = pic_in[i*cut_width : (i+1)*cut_width, j*cut_length : (j+1)*cut_length, :]
            result_path = pic_target + "/" + '{}_{}_{}.jpg'.format(pic_name,num_width-i-1, j+1)
            cv2.imwrite(result_path, pic_out)          
print("Done")

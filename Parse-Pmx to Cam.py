#Pmx to CAM(使用前确保动作内只有一个骨骼)

import sys
import os
import csv

#读入拖入的文件
input_path=sys.argv[1]
#以"out_输入文件"格式输出txt
output_name="out_"+os.path.basename(input_path)

#input_path="campmx.txt"
#output_name="out_campmx.csv"
#print(output_name)

with open(input_path, "r", encoding='utf-8') as input_file:
    input_data = list(csv.reader(input_file))
#去头去尾
    input_data = input_data[4:-5]
#提取需要的列数
    output_data = [[row[i] for i in [1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]] for row in input_data]

#提出有多少帧
    rows = len(output_data) 

#构造每帧内容
for i in range(len(output_data)):
     output_data[i] = output_data[i][:1] + ['0'] + output_data[i][1:7] + ['30'] + ['False'] + output_data[i][7:] + ['20'] + ['20'] + ['107'] + ['107']+ ['20'] + ['20'] + ['107'] + ['107']

with open(output_name, "w", newline='', encoding='utf-8') as output_file:
#写入头尾
    output_data.insert(0,["version:",2])
    output_data.insert(1,["modelname:","カメラ・照明"])
    output_data.insert(2,["boneframe_ct:",0])
    output_data.insert(3,["morphframe_ct:",0])
    output_data.insert(4,["camframe_ct:",rows])
    output_data.insert(5,["frame_num","target_dist","Xpos","Ypos","Zpos","Xrot","Yrot","Zrot","FOV","perspective","interp_x_ax","interp_x_ay","interp_x_bx","interp_x_by","interp_y_ax","interp_y_ay","interp_y_bx","interp_y_by","interp_z_ax","interp_z_ay","interp_z_bx","interp_z_by","interp_r_ax","interp_r_ay","interp_r_bx","interp_r_by","interp_dist_ax","interp_dist_ay","interp_dist_bx","interp_dist_by","interp_fov_ax","interp_fov_ay","interp_fov_bx","interp_fov_by"])
    
    output_data.append(["lightframe_ct:",0])
    output_data.append(["shadowframe_ct:",0])
    output_data.append(["ik/dispframe_ct:",0])


#输出
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(output_data)
    
print("Done!")

#参考用csv中的每列内容
#Cam
#0 frame_num
#1 target_dist距离
#2-7 Xpos Ypos Zpos Xrot Yrot Zrot 坐标和旋转
#8 FOV
#9 perspective 透视，就是カメラ操作那边的“バース”
#10-25 interp_x_ax interp_x_ay interp_x_bx interp_x_by interp_y_ax interp_y_ay interp_y_bx interp_y_by interp_z_ax interp_z_ay interp_z_bx interp_z_by interp_r_ax interp_r_ay interp_r_bx interp_r_by
#26-33 interp_dist_ax interp_dist_ay interp_dist_bx interp_dist_by interp_fov_ax interp_fov_ay interp_fov_bx interp_fov_by
#各种补间

#Pmx
#0 bone_name 骨骼名称
#1 frame_num 
#2-7 Xpos Ypos Zpos Xrot Yrot Zrot
#8 phys_disable "False" 是否注册物理关键帧
#9-24 interp_x_ax interp_x_ay interp_x_bx interp_x_by interp_y_ax interp_y_ay interp_y_bx interp_y_by interp_z_ax interp_z_ay interp_z_bx interp_z_by interp_r_ax interp_r_ay interp_r_bx interp_r_by

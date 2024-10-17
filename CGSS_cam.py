#under construction
import json 
import sys
import os
import re
import math
input_json = sys.argv[1]

infile =open(input_json)
print("Input file:",os.path.basename(input_json))

data = json.load(infile)
pos = data["cameraPosKeys"]["thisList"]
pos_frame = [entry["frame"] for entry in pos]
pos_offset = [entry["offset"] for entry in pos]

lkat = data["cameraLookAtKeys"]["thisList"]
lkat_frame = [entry["frame"] for entry in lkat]
lkat_offset = [entry["offset"] for entry in lkat]

#校对相机pos帧和lookat帧
pointer=0
for i in range(0,len(pos_frame)):
    if (pos_frame[i] > lkat_frame[-1]):
        print("Pos",i,":",pos_frame[i]," is over",lkat_frame[-1])
    else:
        for j in range(pointer,len(lkat_frame)):
            if (pos_frame[i] >= lkat_frame[pointer]) and(pos_frame[i] < lkat_frame[j+1]):
                print("Pos",i,":",pos_frame[i]," is between",lkat_frame[j],"and",lkat_frame[j+1])
                break
            pointer=pointer+1
                
#切镜头的相邻帧拉开1帧
for i in range(0,len(pos_frame)):
    if ( i != 0 ) and (pos_frame[i] - pos_frame[i-1] == 1 ):
        pos_frame[i]=pos_frame[i]+1


with open(os.path.basename(input_json)+".txt", "w",encoding='utf-8') as outfile:
    outfile.write('version:,2\n')
    outfile.write('modelname:,カメラ・照明\n')
    outfile.write('boneframe_ct:,0\n')
    outfile.write('morphframe_ct:,0\n')
    outfile.write('camframe_ct:,'+str(len(pos_frame))+'\n')
    outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
    for i in range(0,len(pos_frame)):
        print(pos_frame[i])
        
        outfile.write(''+str(math.ceil(pos_frame[i]/2))+',0.0,'+str(pos_offset[i]['x']*10)+','+str(pos_offset[i]['y']*10)+','+str(pos_offset[i]['z']*10)+',0.0,0.0,0.0,30,False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')
    outfile.write('lightframe_ct:,0\n')
    outfile.write('shadowframe_ct:,0\n')
    outfile.write('ik/dispframe_ct:,0\n')

#under construction
import json 
import sys
import os
import re
import math
#input_json = sys.argv[1]
input_json ="Over_camera.json"
infile =open(input_json)
print("Input file:",os.path.basename(input_json))

data = json.load(infile)
pos = data["cameraPosKeys"]["thisList"]
pos_frame = [entry["frame"] for entry in pos]
pos_offset = [entry["offset"] for entry in pos]

lkat = data["cameraLookAtKeys"]["thisList"]
lkat_frame = [entry["frame"] for entry in lkat]
lkat_offset = [entry["offset"] for entry in lkat]
#不要同步赋值
#rx=ry=d=lkat_x=lkat_y=lkat_z=[0]*len(pos_frame)
rx=[0]*len(pos_frame)
ry=[0]*len(pos_frame)
d=[0]*len(pos_frame)
lkat_x=[0]*len(pos_frame)
lkat_y=[0]*len(pos_frame)
lkat_z=[0]*len(pos_frame)
#校对相机pos帧和lookat帧
pointer=0
#补齐pos帧对应lkat位置
for i in range(0,len(pos_frame)):
    pos_x=pos_offset[i]['x']
    pos_y=-pos_offset[i]['y']
    pos_z=-pos_offset[i]['z']
    
    if (pos_frame[i] > lkat_frame[-1]):
                print("Frame",i,":",pos_frame[i],"is over",lkat_frame[-1])
                lkat_x[i]=lkat_offset[-1]['x']
                lkat_y[i]=-(lkat_offset[-1]['y'])
                lkat_z[i]=-(lkat_offset[-1]['z'])
    else:
        for j in range(pointer,len(lkat_frame)):
            if (pos_frame[i] >= lkat_frame[pointer]) and(pos_frame[i] < lkat_frame[j+1]):
                print("Frame",i,":",pos_frame[i],"is between",lkat_frame[j],"-",lkat_frame[j+1])
                ratio=(pos_frame[i]-lkat_frame[j])/(lkat_frame[j+1]-lkat_frame[j])
                lkat_x[i]=lkat_offset[j]['x']+(lkat_offset[j]['x']-lkat_offset[j+1]['x'])*ratio
                lkat_y[i]=-(lkat_offset[j]['y']+(lkat_offset[j]['y']-lkat_offset[j+1]['y'])*ratio)
                lkat_z[i]=-(lkat_offset[j]['z']+(lkat_offset[j]['z']-lkat_offset[j+1]['z'])*ratio)
                break
            pointer=pointer+1

#计算pos和lkat差量
    dx=round(pos_x-lkat_x[i],3)
    dy=round(pos_y-lkat_y[i],3)
    dz=round(pos_z-lkat_z[i],3)
    d[i]=math.sqrt(pow(dx,2)+pow(dy,2)+pow(dz,2))
    if (dz == 0):
        rx[i]="90"
        ry[i]="90"
    else:
        rx[i]=math.degrees(math.atan(dy/dz))
        ry[i]=math.degrees(math.atan(dx/dz))

                    
    print("Pos x:",pos_x,",y:",pos_y,",z:",pos_z)
    print("lkat x:",lkat_x[i],",y:",lkat_y[i],",z:",lkat_z[i])
    print("dx:",dx,",dy:",dy,",dz:",dz,"d",d[i])
    print("rx:",rx[i],",ry:",ry[i])


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
#        print(pos_frame[i])
        outfile.write(''+str(math.ceil(pos_frame[i]/2))+','+str(-d[i]*10)+','+str(lkat_x[i]*10)+','+str(lkat_y[i]*10)+','+str(lkat_z[i]*10)+','+str(rx[i])+','+str(ry[i])+',0.0,30,False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')

    outfile.write('lightframe_ct:,0\n')
    outfile.write('shadowframe_ct:,0\n')
    outfile.write('ik/dispframe_ct:,0\n')

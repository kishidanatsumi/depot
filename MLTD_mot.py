import json
import os
import sys
import re
import numpy as np
import csv
from scipy.spatial.transform import Rotation as rot
import math

#input_json = sys.argv[1]
input_json='./dan_ratata_01_dan.imo.asset.json'
infile=open(input_json)


dic_mltd = {
"POSITION":"センター","BASE":"グルーブ",
"KOSHI":"下半身","MUNE1":"上半身","MUNE2":"上半身2","KUBI":"首","ATAMA":"頭",

"MOMO_L":"左足","HIZA_L":"左ひざ","ASHI_L":"左足首","TSUMASAKI_L":"左つま先",
"MOMO_R":"右足","HIZA_R":"右ひざ","ASHI_R":"右足首","TSUMASAKI_R":"右つま先",

"SAKOTSU_L":"左肩","KATA_L":"左腕","UDE_L":"左ひじ","TE_L":"左手首",
"SAKOTSU_R":"右肩","KATA_R":"右腕","UDE_R":"右ひじ","TE_R":"右手首",

"OYA3_R":"右親指０","OYA2_R":"右親指１","OYA1_R":"右親指２",
"HITO3_R":"右人指１","HITO2_R":"右人指２","HITO1_R":"右人指３",
"NAKA3_R":"右中指１","NAKA2_R":"右中指２","NAKA1_R":"右中指３",
"KUSU3_R":"右薬指１","KUSU2_R":"右薬指２","KUSU1_R":"右薬指３",
"KO3_R":"右小指１","KO2_R":"右小指２","KO1_R":"右小指３",

"OYA3_L":"左親指０","OYA2_L":"左親指１","OYA1_L":"左親指２",
"HITO3_L":"左人指１","HITO2_L":"左人指２","HITO1_L":"左人指３",
"NAKA3_L":"左中指１","NAKA2_L":"左中指２","NAKA1_L":"左中指３",
"KUSU3_L":"左薬指１","KUSU2_L":"左薬指２","KUSU1_L":"左薬指３",
"KO3_L":"左小指１","KO2_L":"左小指２","KO1_L":"左小指３",

#"KUKO_R":"右ダミー","KUKO_L":"左ダミー",
}

dic_wrot = {
"MODEL_00":[0.0,0.0,0.0],"POSITION":[0.0,0.0,0.0],"BODY_SCALE":[0.0,0.0,0.0],
"BASE":[0.0,90.0,0.0],"KOSHI":[0.0,0.0,90.0],"MOMO_L":[0.0,0.0,0.0],"HIZA_L":[0.0,0.0,0.0],"ASHI_L":[0.0,0.0,0.0],"TSUMASAKI_L":[0.0,0.0,90.0],
"MOMO_R":[0.0,0.0,0.0],"HIZA_R":[0.0,0.0,0.0],"ASHI_R":[0.0,0.0,0.0],"TSUMASAKI_R":[0.0,0.0,90.0],
"MUNE1":[0.0,0.0,-90.0],"MUNE2":[0.0,0.0,0.0],"KUBI":[0.0,0.0,0.0],"ATAMA":[90.0,0.0,-90.0],
"SAKOTSU_L":[-90.0,-90.0,0.0],"KATA_L":[-90.0,0.0,0.0],"UDE_L":[0.0,0.0,0.0],"TE_L":[90.0,0.0,0.0],
"HITO3_L":[0.0,0.0,0.0],"HITO2_L":[0.0,0.0,0.0],"HITO1_L":[0.0,0.0,0.0],"KUKO_L":[0.0,0.0,0.0],
"KO3_L":[0.0,0.0,0.0],"KO2_L":[0.0,0.0,0.0],"KO1_L":[0.0,0.0,0.0],
"KUSU3_L":[0.0,0.0,0.0],"KUSU2_L":[0.0,0.0,0.0],"KUSU1_L":[0.0,0.0,0.0],
"NAKA3_L":[0.0,0.0,0.0],"NAKA2_L":[0.0,0.0,0.0],"NAKA1_L":[0.0,0.0,0.0],
"OYA3_L":[-105.0,-40.40399932861328,20.00699806213379],"OYA2_L":[0.0,0.0,0.0],"OYA1_L":[0.0,0.0,0.0],
"SAKOTSU_R":[-90.0,90.0,0.0],"KATA_R":[-90.0,0.0,0.0],"UDE_R":[0.0,0.0,0.0],"TE_R":[90.0,0.0,0.0],
"HITO3_R":[0.0,0.0,0.0],"HITO2_R":[0.0,0.0,0.0],"HITO1_R":[0.0,0.0,0.0],"KUKO_R":[0.0,0.0,0.0],
"KO3_R":[0.0,0.0,0.0],"KO2_R":[0.0,0.0,0.0],"KO1_R":[0.0,0.0,0.0],
"KUSU3_R":[0.0,0.0,0.0],"KUSU2_R":[0.0,0.0,0.0],"KUSU1_R":[0.0,0.0,0.0],
"NAKA3_R":[0.0,0.0,0.0],"NAKA2_R":[0.0,0.0,0.0],"NAKA1_R":[0.0,0.0,0.0],
"OYA3_R":[-74.99993133544922,-40.40384292602539,-20.007532119750978],"OYA2_R":[0.0,0.0,0.0],"OYA1_R":[0.0,0.0,0.0]
}

dic_parent={
"POSITION":[],"MODEL_00":[],
"BASE":["MODEL_00","BODY_SCALE"],
"MUNE1":["MODEL_00","BODY_SCALE","BASE"],
"MUNE2":["MODEL_00","BODY_SCALE","BASE","MUNE1"],
"SAKOTSU_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2"],
"KATA_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L"],
"UDE_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L"],
"TE_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L"],
"OYA3_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L"],
"OYA2_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","OYA3_L"],
"OYA1_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","OYA3_L","OYA2_L"],
"HITO3_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L"],
"HITO2_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","HITO3_L"],
"HITO1_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","HITO3_L","HITO2_L"],
"NAKA3_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L"],
"NAKA2_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","NAKA3_L"],
"NAKA1_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","NAKA3_L","NAKA2_L"],
"KUKO_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L"],
"KUSU3_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","KUKO_L"],
"KUSU2_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","KUKO_L","KUSU3_L"],
"KUSU1_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","KUKO_L","KUSU3_L","KUSU2_L"],
"KO3_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","KUKO_L"],
"KO2_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","KUKO_L","KO3_L"],
"KO1_L":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_L","KATA_L","UDE_L","TE_L","KUKO_L","KO3_L","KO2_L"],
"SAKOTSU_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2"],
"KATA_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R"],
"UDE_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R"],
"TE_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R"],
"OYA3_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R"],
"OYA2_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","OYA3_R"],
"OYA1_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","OYA3_R","OYA2_R"],
"HITO3_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R"],
"HITO2_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","HITO3_R"],
"HITO1_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","HITO3_R","HITO2_R"],
"NAKA3_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R"],
"NAKA2_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","NAKA3_R"],
"NAKA1_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","NAKA3_R","NAKA2_R"],
"KUKO_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R"],
"KUSU3_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","KUKO_R"],
"KUSU2_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","KUKO_R","KUSU3_R"],
"KUSU1_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","KUKO_R","KUSU3_R","KUSU2_R"],
"KO3_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","KUKO_R"],
"KO2_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","KUKO_R","KO3_R"],
"KO1_R":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","SAKOTSU_R","KATA_R","UDE_R","TE_R","KUKO_R","KO3_R","KO2_R"],
"KUBI":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2"],
"ATAMA":["MODEL_00","BODY_SCALE","BASE","MUNE1","MUNE2","KUBI"],
"KOSHI":["MODEL_00","BODY_SCALE","BASE"],
"MOMO_L":["MODEL_00","BODY_SCALE","BASE","KOSHI"],
"HIZA_L":["MODEL_00","BODY_SCALE","BASE","KOSHI","MOMO_L"],
"ASHI_L":["MODEL_00","BODY_SCALE","BASE","KOSHI","MOMO_L","HIZA_L"],
"TSUMASAKI_L":["MODEL_00","BODY_SCALE","BASE","KOSHI","MOMO_L","HIZA_L","ASHI_L"],
"MOMO_R":["MODEL_00","BODY_SCALE","BASE","KOSHI"],
"HIZA_R":["MODEL_00","BODY_SCALE","BASE","KOSHI","MOMO_R"],
"ASHI_R":["MODEL_00","BODY_SCALE","BASE","KOSHI","MOMO_R","HIZA_R"],
"TSUMASAKI_R":["MODEL_00","BODY_SCALE","BASE","KOSHI","MOMO_R","HIZA_R","ASHI_R"],
"SCALE_POINT":["POSITION"]
}


global frame_len
global high_fps
high_fps=0
export_csv=0

def mmd_rot(in_eular):
       in_quat=rot.from_euler('zyx',in_eular,degrees=True).as_quat()
       #print(in_quat)
       x=float(-in_quat[0])
       y=float(-in_quat[1])
       z=float(-in_quat[2])
       w=float(in_quat[3])
       return rot.from_quat([z,y,x,w])

def unity_rot(in_euler):
    x,y,z=in_euler
    quat=rot.from_euler('zxy',[z,x,y],degrees=True).as_quat()
    #Unity转mmd轴：X取反，Z取反
    return rot.from_quat([-quat[0],quat[1],-quat[2],quat[3]])

#从PMX-VMD-Scripting-Tools扒下来的，可以将MMD的四元数转为MMD的欧拉角
def quaternion_to_euler(in_rot):
	"""
	Convert WXYZ quaternion to XYZ euler angles, using the same method as MikuMikuDance.
	Massive thanks and credit to "Isometric" for helping me discover the transformation method used in mmd!!!!
	
	:param quat: 4x float, W X Y Z quaternion
	:return: 3x float, X Y Z angle in degrees
	"""
	quat=in_rot.as_quat()
	x=quat[0]
	y=quat[1]
	z=quat[2]
	w=quat[3]
	# pitch (y-axis rotation)
	sinx_cosy = 2 * ((w * y) + (x * z))
	cosx_cosy = 1 - (2 * ((x ** 2) + (y ** 2)))
	mmd_y = -math.atan2(sinx_cosy, cosx_cosy)
	
	# yaw (z-axis rotation)
	sinz_cosy = 2 * ((-w * z) - (x * y))
	cosz_cosy = 1 - (2 * ((x ** 2) + (z ** 2)))
	mmd_z = math.atan2(sinz_cosy, cosz_cosy)
	
	# roll (x-axis rotation)
	siny = 2 * ((z * y) - (w * x))
	if (siny >= 1.0):
		mmd_x = -math.pi / 2  # use 90 degrees if out of range
	elif (siny <= -1.0):
		mmd_x = math.pi / 2
	else:
		mmd_x = -math.asin(siny)
	
	# fixing the x rotation, part 1
	if x ** 2 > 0.5 or w < 0:
		if x < 0:
			mmd_x = -math.pi - mmd_x
		else:
			mmd_x = math.pi * math.copysign(1, w) - mmd_x
	
	# fixing the x rotation, part 2
	if mmd_x > (math.pi / 2):
		mmd_x = math.pi - mmd_x
	elif mmd_x < -(math.pi / 2):
		mmd_x = -math.pi - mmd_x
	
	mmd_x = math.degrees(mmd_x)
	mmd_y = math.degrees(mmd_y)
	mmd_z = math.degrees(mmd_z)
	
	return [round(mmd_x,4), round(mmd_y,4), round(mmd_z,4)]


#构造
#传入格式[key type,全frame，对位移是否缩放]
def gen_list(key_type,value,rate=1):
        frame_list=[]
        #Discrete
        if ( key_type[0] == "Discreate" ):
                #print("Discrete - total",int((len(value)-2)/2),"frames with",angle,"angle")
                pt=0
                
                frame_list=[0]*frame_len
           
                for i in range(0,int((len(value)-2)/2)):
                        if ( i > 0 ) and ( i < ( (len(value)-2)/2 - 1 ) ):
                                if not ( value[2*i] <= value[2*i+2] ):
                                        print("Error: timing value",value[2*i],"is larger than next value",value[2*i+2])
                                        exit(1)
                                        
                for i in range(0,frame_len):
                        prs_state=round(value[2*pt]*60)
                        nxt_state=round(value[2*pt+2]*60)
                        delta=nxt_state-prs_state
                        if ( i >= prs_state ) and (i < nxt_state ):
                                frame_list[i]=round( ((nxt_state-i)/delta)*value[2*pt+1] + ((i-prs_state)/delta)*value[2*pt+3] , 5 )
                        elif ( i == nxt_state ):
                                frame_list[i]=value[2*pt+3]
                                pt=pt+1
                        else :
                                print("Error: Throw exception when calculating discrete frame value.")
                                exit(1)


        #Constant
        if ( key_type[0] == "Const" ):
                if ( value[0] > -0.0001 ) and ( value[0] < 0.0001 ):
                        value[0]=0
                #print("Constant - append value",value[0],"to",frame_len,"frames with",angle,"angle")
                frame_list = [value[0]] * frame_len
                        
        #FullFrame
        if ( key_type[0] == "FullFrame" ):
                #print("FullFrame - total",len(value),"frames with",rate,"zoom rate and",angle,"angle")
                if not ( len(value) == frame_len ):
                        print("Error: input FullFrame list length is",len(value),"unequal to expected frame length",frame_len)
                        exit(1)
                frame_list= [round(x*rate,4) for x in value]

        #print("Return list length:",len(frame_list),", Min Value:",min(frame_list)," Max Value:",max(frame_list))
        return frame_list



print("==== Info ====")
print("Input file:",os.path.basename(input_json))

data = json.load(infile)

#initial frame data
#frame_data=[骨骼名,[x旋转],[y旋转],[z旋转],[x位移],[y位移],[z位移]]
frame_data=[]
frame_len = round(data["time_length"]*60)+1
for bone_name in dic_mltd:
        frame_data.append([bone_name,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len])


csv_data=[]

print("Info: time length is",data["time_length"])
print("Info: total frame length is",frame_len)

print("==== Start constructing ====")
curves = data["curves"]

for block in curves:
        path=str(block["path"])
        #所有亲骨骼
        bone_chain=path.split('/')
        bone_name=bone_chain[-1]

        prop_type=re.findall(r"property_type (\w+)*",str(block["attribs"][0]))
        key_type=re.findall(r"key_type (\w+)*",str(block["attribs"][1]))
        value=block["values"]
        #print( bone_chain[-1] )

        if ( bone_name in dic_mltd):
                #print("Path:",path[0],"| Map:",dic_mltd.get(path[0]),"| Property Type:",prop_type[0],"| Key type:",key_type[0],"| Value:",len(value))
                
                index = 0
                for index in range(0,len(frame_data)):
                        if ( frame_data[index][0] == bone_name ):
                                    if ( prop_type[0] == "AngleX" ):
                                            frame_data[index][1]=gen_list(key_type,value,1)
                                            break
                                    if ( prop_type[0] == "AngleY" ):
                                            frame_data[index][2]=gen_list(key_type,value,1)
                                            break
                                    if ( prop_type[0] == "AngleZ" ):
                                            frame_data[index][3]=gen_list(key_type,value,1)
                                            break
                                    if ( prop_type[0] == "PositionX" ):
                                            frame_data[index][4]=gen_list(key_type,value,-10)
                                            break
                                    if ( prop_type[0] == "PositionY" ):
                                            frame_data[index][5]=gen_list(key_type,value,10)
                                            break
                                    if ( prop_type[0] == "PositionZ" ):
                                            frame_data[index][6]=gen_list(key_type,value,-10)
                                            break
                                    index=index+1

        else:
                print("Warning:",bone_chain[-1],"not in dic_mltd, prop_type:",prop_type[0],", Key type:",key_type[0])
                
print("==== End constructing ====")

print("==== Start converting ====")
out_data=[]
#out_data=[MMD骨骼名,[xyz旋转],[xyz位移]]
for frame in frame_data:
        axis=mmd_rot([0,0,0])
        if ( frame[0] in dic_parent ) :
                print("Info: calculating",frame[0],"bone as",dic_mltd.get(frame[0]))
                axis=mmd_rot([0,0,0])
                for parent_bone in dic_parent.get(frame[0]):
                        #print("For bone",frame[0],"calculating",parent_bone)
                        if (parent_bone in dic_wrot):
                                axis=axis*mmd_rot(dic_wrot.get(parent_bone))
                        else:
                                print("Warning: parent bone",parent_bone,"wrot is missing")
                if ( frame[0] in dic_wrot ):
                        origin_pose=axis*mmd_rot(dic_wrot.get(frame[0]))
                else:
                        print("Error: bone",frame[0],"wrot is missing")
                

                out_rot=[]
                out_pos=[]
                for i in range(0,frame_len):
                        target_pose=axis*unity_rot([frame[1][i],frame[2][i],frame[3][i]])
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose*origin_pose.inv())
                        out_rot.append([x_rot,y_rot,z_rot])
                        if ( frame[0] == "BASE"):
                               out_pos.append([frame[4][i],frame[5][i]-8.73,frame[6][i]])
                        else:
                               out_pos.append([frame[4][i],frame[5][i],frame[6][i]])
                if not (frame[0] in dic_mltd):
                        print("Warning:",frame[0],"is not listed in dic_mltd")

                out_data.append([dic_mltd.get(frame[0]),out_rot,out_pos])
                
        else:
                print("Warning:",frame[0],"is not listed in parent_dic")
print("==== End converting ====")

#导出动作txt
with open(os.path.basename(input_json)+".txt", "w",encoding='utf-8') as outfile:
        outfile.write('version:,2\n')
        outfile.write('modelname:,foobar\n')
        outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len/2))+'\n')
        outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
        if ( high_fps == 1 ):
               for frame in out_data:
                      for i in range(0,frame_len):
                             outfile.write(str(frame[0])+','+str(i)+','+str(frame[2][i][0])+','+str(frame[2][i][1])+','+str(frame[2][i][2])+','+str(frame[1][i][0])+','+str(frame[1][i][1])+','+str(frame[1][i][2])+',False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')

        else:
               for frame in out_data:
                      for i in range(0,int(frame_len/2)):
                             outfile.write(str(frame[0])+','+str(i)+','+str(frame[2][2*i][0])+','+str(frame[2][2*i][1])+','+str(frame[2][2*i][2])+','+str(frame[1][2*i][0])+','+str(frame[1][2*i][1])+','+str(frame[1][2*i][2])+',False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')

        outfile.write('morphframe_ct:,0\n')
        outfile.write('camframe_ct:,0\n')
        outfile.write('lightframe_ct:,0\n')
        outfile.write('shadowframe_ct:,0\n')
        outfile.write('ik/dispframe_ct:,0\n')
print("Info: output txt as",os.path.basename(input_json)+".txt")

#导出debug用csv
if ( export_csv == 1 ):
        print("==== Start output csv ====")
        with open(os.path.basename(input_json)+".csv", "w",newline='',encoding='utf-8') as csvfile:
                writer=csv.writer(csvfile)
                for block in curves:
                        path=re.findall(r"[\/]?(\w+)+$",str(block["path"]))
                        prop_type=re.findall(r"property_type (\w+)*",str(block["attribs"][0]))
                        key_type=re.findall(r"key_type (\w+)*",str(block["attribs"][1]))
                        value=block["values"]
        
                        if ( key_type[0] == "Discreate" ):
                                csv_value=[]
                                for i in range(0,int((len(value)-2)/2)):
                                                csv_value.append(value[2*i+1])
                        if ( key_type[0] == "Const" ):
                                csv_value=value
                        if ( key_type[0] == "FullFrame" ):
                                csv_value=value
                        writer.writerow([path[0],prop_type[0],key_type[0]] + csv_value)
        print("Info: output csv as",os.path.basename(input_json)+".csv")
        print("==== End output csv ====")

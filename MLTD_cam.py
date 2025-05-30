import json
import os
import sys
import re
import numpy as np
from scipy.spatial.transform import Rotation as rot
np.set_printoptions(suppress=True)


#input_json = sys.argv[1]
input_json='./cam_sunris_cam.imo.json'
infile=open(input_json)

global frame_len
global high_fps
#0=30fps,1=60fps
high_fps=0
#0=30FOV,1=加FOV,2=FOV加算距离
add_fov=1

def bezier(value):
        #pointer:value中的第几项
        pt=0
        frame_list=[0]*frame_len
        #int(len(value)/4)
        for i in range(0,frame_len):
                
                prs_state=round(value[4*pt]*60)
                nxt_state=round(value[4*pt+4]*60)
                delta=nxt_state-prs_state
                p0=value[4*pt+1]
                p3=value[4*pt+5]
                if (value[4*pt+2]!="Infinity"):
                        #左控制点=p0+左斜率*dt/3
                        p1=p0+value[4*pt+2]*(value[4*pt+4]-value[4*pt])/3
                else:
                        p1="NA"
                if (value[4*pt+3]!="Infinity"):
                        #右控制点=p3-右斜率*dt/3
                        p2=p3-value[4*pt+3]*(value[4*pt+4]-value[4*pt])/3
                else:
                        p2="NA"
                t=(i-prs_state)/delta
                
                if ( i >= prs_state ) and (i < nxt_state ):
                        #p1p2全断点，线性
                        if (value[4*pt+2]=="Infinity") and (value[4*pt+3]=="Infinity"):
                                frame_list[i]=(1-t)*p0+t*p3
                        #p1断点,只算p2的二次曲线
                        elif (value[4*pt+2]=="Infinity"):
                                frame_list[i]=((1-t)**2)*p0+2*(1-t)*t*p2+(t**2)*p3
                        #p2断点
                        elif (value[4*pt+3]=="Infinity"):
                                frame_list[i]=((1-t)**2)*p0+2*(1-t)*t*p1+(t**2)*p3
                        else:
                                frame_list[i]=((1-t)**3)*p0+3*((1-t)**2)*t*p1+3*(1-t)*(t**2)*p2+(t**3)*p3
                                #print("p0",p0,"p1",p1,"p2",p2,"p3",p3)
                elif ( i == nxt_state ):
                        frame_list[i]=p3
                        pt=pt+1
                else :
                        print("Error: Throw exception when calculating discrete frame value.")
                        exit(1)
                        
        return frame_list

def rot_cal(pos,tgt,rot_in):
        front = [0,0,1]
        delta=tgt-pos
        
        if (np.linalg.norm(delta) == 0):
        	print("Error: delta vector has 0 length")
        	exit()
            
        forward=delta/np.linalg.norm(delta)
        rotAxis=np.cross(forward,front)
        rotAxis=rotAxis/np.linalg.norm(rotAxis)
        dot=np.dot(forward,front)
        rotAngle=np.acos(dot)
        result=rot.from_rotvec(rotAngle*rotAxis,degrees=False)
        z,x,y=result.as_euler(seq="zxy",degrees=True)
        return [-x+180,y,-rot_in+180]

def fov_cal(fov_len):
        fov=2*np.atan(10/fov_len)
        return np.rad2deg(fov)

print("==== Info ====")
print("Input file:",os.path.basename(input_json))

data = json.load(infile)

#initial frame data
frame_len = round(data["time_length"]*60)+1
cam_data=[[0]*frame_len]*8

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
        value=block["values"]
        if (len(block["attribs"]) == 2):
                key_type=re.findall(r"key_type (\w+)*",str(block["attribs"][1]))
                print("Path:",path,"| Property Type:",prop_type[0],"| Key type:",key_type[0],"| Value:",len(value))
                
        else:
                property_name=re.findall(r"property_name (\w+)*",str(block["attribs"][1]))
                key_type=re.findall(r"key_type (\w+)*",str(block["attribs"][2]))
                print("Path:",path,"| Property Type:",prop_type[0],"| Property Name:",property_name[0],"| Key type:",key_type[0],"| Value:",len(value))
                
        if ( path == "CamBaseS" ):
                if ( prop_type[0] == "PositionX" ):
                        cam_data[0]=bezier(value)
                if ( prop_type[0] == "PositionY" ):
                        cam_data[1]=bezier(value)
                if ( prop_type[0] == "PositionZ" ):
                        cam_data[2]=bezier(value)
                if ( prop_type[0] == "AngleZ" ):
                        cam_data[6]=bezier(value)
        elif ( path == "CamTgtS" ):
                if ( prop_type[0] == "PositionX" ):
                        cam_data[3]=bezier(value)
                if ( prop_type[0] == "PositionY" ):
                        cam_data[4]=bezier(value)
                if ( prop_type[0] == "PositionZ" ):
                        cam_data[5]=bezier(value)
        elif ( path == "CamBase" ):
                if (  property_name[0] == "focalLength" ):
                        cam_data[7]=bezier(value)

print("==== End constructing ====")

#导出动作txt
with open(os.path.basename(input_json)+".txt", "w",encoding='utf-8') as outfile:
        outfile.write('version:,2\n')
        outfile.write('modelname:,カメラ・照明\n')
        outfile.write('boneframe_ct:,0\n')
        outfile.write('morphframe_ct:,0\n')
        if (high_fps==1):
                outfile.write('camframe_ct:,'+str(int(frame_len))+'\n')
                outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
                for i in range(0,frame_len):
                        rotate=rot_cal(np.array([cam_data[0][i],cam_data[1][i],cam_data[2][i]]),np.array([cam_data[3][i],cam_data[4][i],cam_data[5][i]]),cam_data[6][i])
                        distance=1.25*np.linalg.norm(np.array([cam_data[3][i]-cam_data[0][i],cam_data[4][i]-cam_data[1][i],cam_data[5][i]-cam_data[2][i]]))
                        if (add_fov==1):
                                fov=str(int(fov_cal(cam_data[7][i])))
                        elif (add_fov==2):
                                fov=str(30)
                                distance=distance+cam_data[7][i]/2
                        else:
                                fov=str(30)
                                
                        outfile.write(str(i)+','+str(round(distance,3))+','+str(round(-cam_data[0][i]*12.5,3))+','+str(round(cam_data[1][i]*12.5,3))+','+str(round(-cam_data[2][i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')
        else:
                outfile.write('camframe_ct:,'+str(int(frame_len/2))+'\n')
                outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
                for i in range(0,int(frame_len/2)):
                        rotate=rot_cal(np.array([cam_data[0][2*i],cam_data[1][2*i],cam_data[2][2*i]]),np.array([cam_data[3][2*i],cam_data[4][2*i],cam_data[5][2*i]]),cam_data[6][2*i])
                        distance=1.25*np.linalg.norm(np.array([cam_data[3][2*i]-cam_data[0][2*i],cam_data[4][2*i]-cam_data[1][2*i],cam_data[5][2*i]-cam_data[2][2*i]]))
                        if (add_fov==1):
                                fov=str(int(fov_cal(cam_data[7][2*i])))
                        elif (add_fov==2):
                                fov=str(30)
                                distance=distance+cam_data[7][2*i]/2
                        else:
                                fov=str(30)
                                
                        outfile.write(str(i)+','+str(round(distance,3))+','+str(round(-cam_data[0][2*i]*12.5,3))+','+str(round(cam_data[1][2*i]*12.5,3))+','+str(round(-cam_data[2][2*i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')

        outfile.write('lightframe_ct:,0\n')
        outfile.write('shadowframe_ct:,0\n')
        outfile.write('ik/dispframe_ct:,0\n')
print("Info: output txt as",os.path.basename(input_json)+".txt")

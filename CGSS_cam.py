import json
import os
import sys
import re
import numpy as np
from scipy.spatial.transform import Rotation as rot

#input_json = sys.argv[1]
input_json='./Palette_Camera.json'
if not os.path.exists(input_json):
        print("don't exist")
        input()
else:
        split=os.path.splitext(os.path.basename(input_json))
        out_name=split[0]


global hi_fps
global frame_len
global rip_list

#0=关键帧,1=逐帧
full_frame=0

#0=30fps,1=60fps
hi_fps=0

mouth_dic = {0: 'にやり', 1: 'あ', 2: 'い', 3: 'う', 4: 'え', 5: 'お', 6: 'にやり', 7: 'にやり', 8: 'ワ', 10: 'ワ'}
eyel_dic = {10: 'ウィンク２', 11: 'ウィンク', 2: 'ウィンク'}
eyer_dic = {10: 'ウィンク２右', 11: 'ウィンク右', 2: 'ウィンク右'}

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
        if y>0:
                y=y-360
        elif y<-360:
                y=y+360

        return [x,y+180,-rot_in]

def bezier(frame_in):
        #[frame,value,curve,interpolateType,bezier]
        #pointer:list第几项
        pt=0
        #[x,y,z]
        frame_out=[0]*frame_len
        prs_state=frame_in[pt][0]
        nxt_state=frame_in[pt+1][0]
        for i in range(0,frame_len):
                p0=frame_in[pt][1]
                p3=frame_in[pt+1][1]
                if ( i >= prs_state ) and (i < nxt_state ):
                        #有曲线
                        if (len(frame_in[pt+1][2])>0) :
                                t=(i-prs_state)/(nxt_state-prs_state)
                                for j in range(0,len(frame_in[pt+1][2])-1):
                                        if  (frame_in[pt+1][2][j]["time"]<=t<frame_in[pt+1][2][j+1]["time"]):
                                                k0=frame_in[pt+1][2][j]["outSlope"]
                                                k3=frame_in[pt+1][2][j+1]["inSlope"]
                                                t0=frame_in[pt+1][2][j]["time"]
                                                t3=frame_in[pt+1][2][j+1]["time"]
                                                v0=frame_in[pt+1][2][j]["value"]
                                                v3=frame_in[pt+1][2][j+1]["value"]
                                                #print("frame=",i)
                                                #print("Curve info: k0=",k0,"k3=",k3,"v0=",v0,"v3=",v3)

                                t_curve=(t-t0)/(t3-t0)
                                v_curve=v0+(v3-v0)*(k0*((1-t_curve)**2)*t_curve+(3-k3)*(1-t_curve)*(t_curve**2)+t_curve**3)

                                frame_out[i]=p0+(p3-p0)*v_curve
                        #无曲线，无贝塞尔点，插值interpolateType!=0，使用默认曲线
                        elif frame_in[pt+1][3]!=0 and len(frame_in[pt+1][2])==0 and len(frame_in[pt+1][4])!=1 :

                                t0=frame_in[pt][0]
                                t3=frame_in[pt+1][0]
                                v0=prs_state
                                v3=nxt_state

                                t_curve=(i-t0)/(t3-t0)
                                v_curve=3*(1-t_curve)*(t_curve**2)+t_curve**3
                                frame_out[i]=p0+(p3-p0)*v_curve
                        elif (len(frame_in[pt+1][4])>0) and (frame_in[pt][0]>0):
                                t0=prs_state
                                t3=nxt_state
                                v0=frame_in[pt][1]
                                v3=frame_in[pt+1][1]

                                if (v3==v0):
                                        frame_out[i]=v3
                                #单贝塞尔点
                                elif(len(frame_in[pt+1][4])==1):
                                        #print(t0,t3,v3,v0,10*frame_in[pt+1][4][0])
                                        p=-frame_in[pt+1][4][0]/(v3-v0)
                                        t_curve=(i-t0)/(t3-t0)
                                        #1-\left(2\cdot0.569\left(1-t\right)t+\left(1-t\right)^{2}\right)
                                        v_curve=1-(2*p*t_curve*(1-t_curve)+(1-t_curve)**2)
                                        #if i==1645*2:   
                                                
                                        #        print(i,v3,v0,frame_in[pt+1][4][0],p)
                                        frame_out[i]=v0+(v3-v0)*v_curve
                                #双贝塞尔点
                                elif(len(frame_in[pt+1][4])==2):
                                        p2=-frame_in[pt+1][4][1]/(v3-v0)
                                        p3=-frame_in[pt+1][4][2]/(v3-v0)
                                        t_curve=(i-t0)/(t3-t0)
                                        v_curve=1-(3*p3*(1-t_curve)*(t_curve**2)+3*p2*((1-t_curve)**2)*t+(1-t_curve)**3)
                                        frame_out[i]=v0+(v3-v0)*v_curve
                                #贝塞尔点>2，没见到例子但留个case
                                else:
                                        print("Warning: frame",frame_in[pt][0],"to",frame_in[pt+1][0],"has",len(frame_in[pt+1][4]),"bezier point and",len(frame_in[pt+1][2]),"curve")
                                        frame_out[i]=p0
                        else:
                                #interpolateType=0，定值
                                frame_out[i]=p0
                                
                elif ( i == nxt_state ):
                        frame_out[i]=p3
                        prs_state=nxt_state
                        if ( prs_state == frame_in[-1][0] ) and ( frame_in[-1][0] < frame_len ):
                                nxt_state=frame_len
                        else:
                                pt=pt+1
                                nxt_state=frame_in[pt+1][0]


                        if (frame_in[pt+1][3]!=2) and (len(frame_in[pt+1][2])>0):
                                print("frame",frame_in[pt][0],"to",frame_in[pt+1][0],"has interpolateType",frame_in[pt+1][3],"but",len(frame_in[pt+1][2]),"curve")
                        if (len(frame_in[pt+1][4])!=0):
                                print("frame",frame_in[pt][0],"to",frame_in[pt+1][0],"has",len(frame_in[pt+1][4]),"bezier point and",len(frame_in[pt+1][2]),"curve")


                else :
                        print("Error: Throw exception when calculating discrete frame value.")
                        exit(1)
        return frame_out


def parse_rip(rip_keys,mouth_keys=[]):
        rip_list=[]
        for i,key in enumerate(rip_keys):
                write_true=1
                frame=key["frame"]
                if (len(mouth_keys)>1):
                        for j,dat in enumerate(mouth_keys) :
                                if ( frame <= dat["frame"] ):
                                        #print(frame,mouth_keys[i-1]["attribute"])
                                        if (mouth_keys[j-1]["attribute"]==65536):
                                                write_true=0
                                        elif (mouth_keys[j-1]["attribute"]==0):
                                                write_true=1
                                        else :
                                                print("attribute=",mouth_keys[j-1]["attribute"])
                                                write_true=1
                                        break

                if (hi_fps != 1):
                        frame=int(frame/2)
                if ( key["vowel"] in mouth_dic) and (write_true==1):
                        value=mouth_dic[key["vowel"]]
                else:
                        value="bar"
                
                if ( i == 0 ):
                        value_prev="bar"
                        rip_list.append([frame,value,1.0])
                elif ( value != value_prev ):
                        if (value_prev == "い"):
                                rip_list.append([frame,value_prev,1.0])    
                                rip_list.append([frame+1,value_prev,0.0])
                        else:
                                rip_list.append([frame,value_prev,1.0])    
                                rip_list.append([frame+2,value_prev,0.0])
                        
                        if (value == "い"):
                                rip_list.append([frame,value,0.0])
                                rip_list.append([frame+1,value,1.0])
                        else:
                                rip_list.append([frame,value,0.0])
                                rip_list.append([frame+2,value,1.0])
                value_prev=value
        return rip_list

def parse_eye(eye_keys):
        eyer_list=eyel_list=[]
        for i,key in enumerate(eye_keys):
                frame=key["frame"]
                if (hi_fps != 1):
                        frame=int(frame/2)
                     
                if ( key["eyeRFlag"] in eyer_dic):
                        eyer=eyer_dic[key["eyeRFlag"]]
                else:
                        eyer="foo"+str(key["eyeRFlag"])
                        
                if ( key["eyeLFlag"] in eyel_dic):
                        eyel=eyel_dic[key["eyeLFlag"]]
                else:
                        eyel="foo"+str(key["eyeLFlag"])
                if ( i == 0 ):
                        eyer_prev="bar"
                        eyel_prev="bar"
                        eyer_list.append([frame,eyer,1])
                        eyel_list.append([frame,eyel,1])
                        
                else:
                        if ( eyer_prev != eyer ):
                                eyer_list.append([frame,eyer_prev,1.0])
                                eyer_list.append([frame+2,eyer_prev,0.0])
                        
                                eyer_list.append([frame,eyer,0.0])          
                                eyer_list.append([frame+2,eyer,1.0])
                        
                        if ( eyel_prev != eyel ):
                                eyel_list.append([frame,eyel_prev,1.0])
                                eyel_list.append([frame+2,eyel_prev,0.0])
                        
                                eyel_list.append([frame,eyel,0.0])          
                                eyel_list.append([frame+2,eyel,1.0])

                eyer_prev=eyer
                eyel_prev=eyel 
        return eyer_list,eyel_list

def write_facial(f_path,list_group):
        with open(f_path, "w",encoding='utf-8') as outfile:
                length=0
                out=""
                for i in list_group:
                        length+=len(i)
                        for data in i:
                                out=out+data[1]+','+str(data[0])+','+str(data[2])+"\n"
                outfile.write('version:,2\n')
                outfile.write('modelname:,foobar\n')
                outfile.write('boneframe_ct:,0\n')
                outfile.write('morphframe_ct:,'+str(length)+'\n')
                outfile.write('morph_name,frame_num,value\n')
                outfile.write(out)
                outfile.write('camframe_ct:,0\n')
                outfile.write('lightframe_ct:,0\n')
                outfile.write('shadowframe_ct:,0\n')
                outfile.write('ik/dispframe_ct:,0\n')
        print("Output:",f_path)



with open(input_json, encoding='utf-8') as infile:
    data = json.load(infile)


print("Info: input file is",os.path.basename(input_json))

#pos txt
off_name=list(data["formationOffsetSet"])
for position in off_name:
        off_list=[]
        out=""
        pos_dat=data["formationOffsetSet"][position]["thisList"]
        if ( len(pos_dat) > 1):
                with open(out_name+"_pos_"+position+".txt", "w",encoding='utf-8') as outfile:
                        outfile.write('version:,2\n')
                        outfile.write('modelname:,foobar\n')
                        outfile.write('boneframe_ct:,'+str(len(pos_dat)*2-1)+'\n')
                        outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
                        for i in range(0,len(pos_dat)):
                                frame=pos_dat[i]["frame"]
                                if ( hi_fps != 1):
                                        frame=int(frame/2)
                                if ( i != 0 ):
                                        outfile.write('センター'+','+str(frame-1)+','+str(-pos_dat[i-1]["posXZ"]["x"]*12.5)+','+str(pos_dat[i-1]["posY"]*12.5)+','+str(-pos_dat[i-1]["posXZ"]["y"]*12.5)+',0,'+str(-pos_dat[i-1]["rotY"])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n') 

                                outfile.write('センター'+','+str(frame)+','+str(-pos_dat[i]["posXZ"]["x"]*12.5)+','+str(pos_dat[i]["posY"]*12.5)+','+str(-pos_dat[i]["posXZ"]["y"]*12.5)+',0,'+str(-pos_dat[i]["rotY"])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n') 
                        outfile.write('morphframe_ct:,0\n')
                        outfile.write('camframe_ct:,0\n')
                        outfile.write('lightframe_ct:,0\n')
                        outfile.write('shadowframe_ct:,0\n')
                        outfile.write('ik/dispframe_ct:,0\n')
                print("Output:",out_name+"_pos_"+position+".txt")

#facial
#rip_keys = data["ripSyncKeys"]["thisList"]
#eye_keys = data["facial1Set"]["eyeKeys"]["thisList"]
mouth_keys = data["facial1Set"]["mouthKeys"]["thisList"]

eyer_list,eyel_list=parse_eye(data["facial1Set"]["eyeKeys"]["thisList"])
rip_list_full=parse_rip(data["ripSyncKeys"]["thisList"])
write_facial(out_name+"_mouth.txt",[rip_list_full])


rip_list=parse_rip(data["ripSyncKeys"]["thisList"],data["facial1Set"]["mouthKeys"]["thisList"])
write_facial(out_name+"_facial_main.txt",[eyer_list,eyel_list,rip_list])


if (len(data["other4FacialArray"]) != 0 ):
        for i,sdata in enumerate(data["other4FacialArray"]):
                eyer_list,eyel_list=parse_eye(sdata["eyeKeys"]["thisList"])
                rip_list=parse_rip(data["ripSyncKeys"]["thisList"],sdata["mouthKeys"]["thisList"])
                if (len(eyer_list)!=0) or (len(eyel_list)!=0):
                        write_facial(out_name+"_facial_other_"+str(i)+".txt",[eyer_list,eyel_list,rip_list])

#cam
pos_keys = data["cameraPosKeys"]["thisList"]
lookat_keys = data["cameraLookAtKeys"]["thisList"]
roll_keys = data["cameraRollKeys"]["thisList"]
fov_keys = data["cameraFovKeys"]["thisList"]
#print(len(pos_keys))
#print(len(lookat_keys))
#print(len(roll_keys))
frame_len=pos_keys[-1]["frame"]
#print(frame_len)

key_frame=[]
cam_data=[[0]*frame_len]*8

posx_list=[]
posy_list=[]
posy_abs_list=[]
posz_list=[]
lkatx_list=[]
lkaty_list=[]
lkatz_list=[]
roll_list=[]
fov_list=[]

for key in pos_keys:
        key_frame.append(key["frame"])
        bezierx_list=[]
        beziery_list=[]
        bezierz_list=[]
        if(len(key["bezierPoints"])>0):
                #print(key["frame"],len(key["bezierPoints"]))
                for i in range(0,len(key["bezierPoints"])):
                        bezierx_list.append(key["bezierPoints"][i]["x"])
                        beziery_list.append(key["bezierPoints"][i]["y"])
                        
#[frame,value,curve data,inerpolateType,bezier]
        if key["setType"]==2:
                #用offset
                posx_list.append([key["frame"],key["offset"]["x"],key["curve"]["m_Curve"],key["interpolateType"],bezierx_list])
                posy_list.append([key["frame"],key["offset"]["y"],key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
                if (key["charaRelativeBase"]==0):
                        posy_abs_list.append([key["frame"],key["offset"]["y"],key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
                else:
                        posy_abs_list.append([key["frame"],key["offset"]["y"]+1.35,key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
                posz_list.append([key["frame"],key["offset"]["z"],key["curve"]["m_Curve"],key["interpolateType"],bezierz_list])
        else:
                #用posDirect
                posx_list.append([key["frame"],key["posDirect"]["x"],key["curve"]["m_Curve"],key["interpolateType"],bezierx_list])
                posy_list.append([key["frame"],key["posDirect"]["y"],key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
                if (key["charaRelativeBase"]==0):
                        posy_abs_list.append([key["frame"],key["posDirect"]["y"],key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
                else:
                        posy_abs_list.append([key["frame"],key["posDirect"]["y"]+1.35,key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
                posz_list.append([key["frame"],key["posDirect"]["z"],key["curve"]["m_Curve"],key["interpolateType"],bezierz_list])

for key in lookat_keys:
        key_frame.append(key["frame"])
        bezierx_list=[]
        beziery_list=[]
        bezierz_list=[]
        if(len(key["bezierPoints"])>0):
                for i in range(0,len(key["bezierPoints"])):
                        bezierx_list.append(key["bezierPoints"][i]["x"])
                        beziery_list.append(key["bezierPoints"][i]["y"])
                        bezierz_list.append(-key["bezierPoints"][i]["z"])

        
        lkatx_list.append([key["frame"],key["offset"]["x"],key["curve"]["m_Curve"],key["interpolateType"],bezierx_list])
        lkaty_list.append([key["frame"],key["offset"]["y"],key["curve"]["m_Curve"],key["interpolateType"],beziery_list])
        lkatz_list.append([key["frame"],key["offset"]["z"],key["curve"]["m_Curve"],key["interpolateType"],bezierz_list])


for key in roll_keys:
        key_frame.append(key["frame"])
        roll_list.append([key["frame"],key["degree"],key["curve"]["m_Curve"],key["interpolateType"],[]])

for key in fov_keys:
        key_frame.append(key["frame"])
        fov_list.append([key["frame"],key["fov"],key["curve"]["m_Curve"],key["interpolateType"],[]])

print("Processing:posX")
posx_frame=bezier(posx_list)
posx_frame.append(posx_frame[-1])
print("Processing:posY")
posy_frame=bezier(posy_list)
posy_frame.append(posy_frame[-1])
print("Processing:posYabs")
posy_abs_frame=bezier(posy_abs_list)
posy_abs_frame.append(posy_abs_frame[-1])
print("Processing:posZ")
posz_frame=bezier(posz_list)
posz_frame.append(posz_frame[-1])
print("Processing:lkat")
lkatx_frame=bezier(lkatx_list)
lkatx_frame.append(lkatx_frame[-1])
lkaty_frame=bezier(lkaty_list)
lkaty_frame.append(lkaty_frame[-1])
lkatz_frame=bezier(lkatz_list)
lkatz_frame.append(lkatz_frame[-1])
print("Processing:roll")
roll_frame=bezier(roll_list)
roll_frame.append(roll_frame[-1])
print("Processing:fov")
fov_frame=bezier(fov_list)
fov_frame.append(fov_frame[-1])

key_frame=sorted(set(key_frame))
print(key_frame)
#camera txt
with open(out_name+"_cam.txt", "w",encoding='utf-8') as outfile:
        outfile.write('version:,2\n')
        outfile.write('modelname:,カメラ・照明\n')
        outfile.write('boneframe_ct:,0\n')
        outfile.write('morphframe_ct:,0\n')

        if (hi_fps==1):
                if(full_frame==1):
                        outfile.write('camframe_ct:,'+str(frame_len-1)+'\n')
                        outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
                        for i in range(0,frame_len-1):
                                rotate=rot_cal(np.array([posx_frame[i],posy_frame[i],posz_frame[i]]),np.array([lkatx_frame[i],lkaty_frame[i],lkatz_frame[i]]),roll_frame[i])
                                distance=-1.25*np.linalg.norm(np.array([lkatx_frame[i]-posx_frame[i],lkaty_frame[i]-posy_frame[i],lkatz_frame[i]-posz_frame[i]]))
                                #fov=str(30)
                                distance=0
                                fov=str(int(fov_frame[i]))
                                outfile.write(str(i)+','+str(round(distance,3))+','+str(round(-posx_frame[i]*12.5,3))+','+str(round((posy_frame[i])*12.5,3))+','+str(round(-posz_frame[i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')

                else:
                        outfile.write('camframe_ct:,'+str(int(len(key_frame)))+'\n')
                        outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
                        for i in key_frame:
                                rotate=rot_cal(np.array([posx_frame[i],posy_frame[i],posz_frame[i]]),np.array([lkatx_frame[i],lkaty_frame[i],lkatz_frame[i]]),roll_frame[i])
                                distance=-1.25*np.linalg.norm(np.array([lkatx_frame[i]-posx_frame[i],lkaty_frame[i]-posy_frame[i],lkatz_frame[i]-posz_frame[i]]))
                                #fov=str(30)
                                distance=0
                                fov=str(int(fov_frame[i]))
                                outfile.write(str(i)+','+str(round(distance,3))+','+str(round(-posx_frame[i]*12.5,3))+','+str(round((posy_abs_frame[i])*12.5,3))+','+str(round(-posz_frame[i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')


        else:
                if(full_frame==1):
                        outfile.write('camframe_ct:,'+str(int(frame_len/2)-1)+'\n')
                        outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
                        for i in range(0,int(frame_len/2)-1):
                                rotate=rot_cal(np.array([posx_frame[2*i],posy_frame[2*i],posz_frame[2*i]]),np.array([lkatx_frame[2*i],lkaty_frame[2*i],lkatz_frame[2*i]]),roll_frame[2*i])
                                distance=-1.25*np.linalg.norm(np.array([lkatx_frame[2*i]-posx_frame[2*i],lkaty_frame[2*i]-posy_frame[2*i],lkatz_frame[2*i]-posz_frame[2*i]]))
                                #fov=str(30)
                                distance=0
                                fov=str(int(fov_frame[2*i]))
                                outfile.write(str(i)+','+str(round(distance,3))+','+str(round(-posx_frame[2*i]*12.5,3))+','+str(round((posy_abs_frame[2*i])*12.5,3))+','+str(round(-posz_frame[2*i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')

                else:
                        outfile.write('camframe_ct:,'+str(int(len(key_frame)))+'\n')
                        outfile.write('frame_num,target_dist,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,FOV,perspective,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by,interp_dist_ax,interp_dist_ay,interp_dist_bx,interp_dist_by,interp_fov_ax,interp_fov_ay,interp_fov_bx,interp_fov_by\n')
                        for i in key_frame:
                                rotate=rot_cal(np.array([posx_frame[i],posy_frame[i],posz_frame[i]]),np.array([lkatx_frame[i],lkaty_frame[i],lkatz_frame[i]]),roll_frame[i])
                                distance=-1.25*np.linalg.norm(np.array([lkatx_frame[i]-posx_frame[i],lkaty_frame[i]-posy_frame[i],lkatz_frame[i]-posz_frame[i]]))
                                distance=0
                                fov=str(int(fov_frame[i]))
                                if i-1 in key_frame:
                                        outfile.write(str(int((i+1)/2))+','+str(round(distance,3))+','+str(round(-posx_frame[i]*12.5,3))+','+str(round((posy_abs_frame[i])*12.5,3))+','+str(round(-posz_frame[i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')
                                else:
                                        outfile.write(str(int(i/2))+','+str(round(distance,3))+','+str(round(-posx_frame[i]*12.5,3))+','+str(round((posy_abs_frame[i])*12.5,3))+','+str(round(-posz_frame[i]*12.5,3))+','+str(round(rotate[0],3))+','+str(round(rotate[1],3))+','+str(round(rotate[2],3))+','+fov+',False,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107,20,20,107,107\n')
                         
        outfile.write('lightframe_ct:,0\n')
        outfile.write('shadowframe_ct:,0\n')
        outfile.write('ik/dispframe_ct:,0\n')
print("Info: output txt as",os.path.basename(input_json)+".txt")


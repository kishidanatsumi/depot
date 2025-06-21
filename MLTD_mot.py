import json,os,sys,re,csv,math
import numpy as np
from scipy.spatial.transform import Rotation as rot

global frame_len
global high_fps

#文件名
input_song='cmfeel'
#0=30fps,1=60fps
high_fps=0
#舞蹈文件id
dance_id='01'
#站位id(无=0)
pos_id=0
#是否导出debug用数据表
export_csv=0

#input_json = sys.argv[1]
input_json='./dan_'+input_song+'_'+dance_id+'_dan.imo.asset.json'
input_json_yoko='./'+input_song+'_scenario_yoko_sobj.json'

dic_mltd2 = {
"POSITION":"センター",
}

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
"MODEL_00":[0,0,0],"BODY_SCALE":[0,0,0],"POSITION":[0,0,0],
"BASE":[0,90,0],"KOSHI":[0,0,90],"MOMO_L":[0,0,0],"HIZA_L":[0,0,0],"ASHI_L":[0,0,0],"TSUMASAKI_L":[0,0,90],
"MOMO_R":[0,0,0],"HIZA_R":[0,0,0],"ASHI_R":[0,0,0],"TSUMASAKI_R":[0,0,90],
"MUNE1":[0,0,-90],"MUNE2":[0,0,0],"KUBI":[0,0,0],"ATAMA":[90,0,-90],
"SAKOTSU_L":[-90,-90,0],"KATA_L":[-90,0,0],"UDE_L":[0,0,0],"TE_L":[90,0,0],
"HITO3_L":[0,0,0],"HITO2_L":[0,0,0],"HITO1_L":[0,0,0],"KUKO_L":[0,0,0],
"KO3_L":[0,0,0],"KO2_L":[0,0,0],"KO1_L":[0,0,0],
"KUSU3_L":[0,0,0],"KUSU2_L":[0,0,0],"KUSU1_L":[0,0,0],
"NAKA3_L":[0,0,0],"NAKA2_L":[0,0,0],"NAKA1_L":[0,0,0],
"OYA3_L":[-105.0,-40.404,20.00753212],"OYA2_L":[0,0,0],"OYA1_L":[0,0,0],
"SAKOTSU_R":[-90,90,0],"KATA_R":[-90,0,0],"UDE_R":[0,0,0],"TE_R":[90,0,0],
"HITO3_R":[0,0,0],"HITO2_R":[0,0,0],"HITO1_R":[0,0,0],"KUKO_R":[0,0,0],
"KO3_R":[0,0,0],"KO2_R":[0,0,0],"KO1_R":[0,0,0],
"KUSU3_R":[0,0,0],"KUSU2_R":[0,0,0],"KUSU1_R":[0,0,0],
"NAKA3_R":[0,0,0],"NAKA2_R":[0,0,0],"NAKA1_R":[0,0,0],
"OYA3_R":[-75,-40.404,-20.00753212],"OYA2_R":[0,0,0],"OYA1_R":[0,0,0]
}

def world_rot(in_euler):
    x,y,z=in_euler
    return rot.from_euler('xyz',[-x,-y,-z],degrees=True)

def unity_rot(in_euler):
    x,y,z=in_euler
    return rot.from_euler('zxy',[-z,-x,y],degrees=True)

def mmd_rot(in_rot):
    z,x,y=in_rot.as_euler('zxy',degrees=True)
    return [round(x,4), round(-y,4), round(-z,4)]

#传入格式[key type,全frame，对位移缩放系数]
def gen_list(key_type,value,rate=1):
        frame_list=[]
        #Discrete
        if ( key_type[0] == "Discreate" ):
                #print("Discrete - total",int((len(value)-2)/2),"frames with",angle,"angle")
                pt=0
                #构造全0数列
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
infile=open(input_json)
data=json.load(infile)
#构造全0数据块
#frame_data=[骨骼名,[x旋转],[y旋转],[z旋转],[x位移],[y位移],[z位移],[亲骨骼序列]]
frame_data=[]
frame_len = round(data["time_length"]*60)+1
for bone_name in dic_mltd:
        frame_data.append([bone_name,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[]])

print("Info: time length is",data["time_length"])
print("Info: total frame length is",frame_len)

print("==== Start constructing ====")
curves = data["curves"]

for block in curves:
        path=str(block["path"])
        bone_chain=path.split('/')
        bone_name=bone_chain[-1]
        prop_type=re.findall(r"property_type (\w+)*",str(block["attribs"][0]))
        key_type=re.findall(r"key_type (\w+)*",str(block["attribs"][1]))
        value=block["values"]
        #print( bone_chain[-1] )
        
        if ( bone_name in dic_mltd):
                print("Info: Path name - ",bone_name,"| Property Type - ",prop_type[0],"| Key type -",key_type[0])
                
                #print("Path:",bone_name,"| Map:",dic_mltd.get(path[0]),"| Property Type:",prop_type[0],"| Key type:",key_type[0],"| Value:",len(value))
                index = 0
                for index in range(0,len(frame_data)):
                        if ( frame_data[index][0] == bone_name ):
                                    frame_data[index][7]=bone_chain[:-1]
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

#out_data=[时间,x,y,z,w]
pos_data=[]
if (pos_id != 0):
        infile_yoko=open(input_json_yoko)
        data_yoko=json.load(infile_yoko)
        scenario = data_yoko["scenario"]
        for block in scenario:
                if (block["type"]==52) and ( pos_id <= len(block["formation"])):
                        #print("Param:",block["param"],"| Time:",float(block["absTime"]),"| Pos:",block["formation"][pos_id-1])
                        pos_data.append([float(block["absTime"]),block["formation"][pos_id-1]["x"]*10,block["formation"][pos_id-1]["y"]*10,block["formation"][pos_id-1]["z"]*10,block["formation"][pos_id-1]["w"]])
                elif (block["type"]==52) and ( pos_id > len(block["formation"])):
                        print("Warning: position id",pos_id,"out of range, data width is",len(block["formation"]))
                        break

print("Info: position id",pos_id,"include",len(pos_data),"position data")
print("==== End constructing ====")

print("==== Start converting ====")
out_data=[]
#out_data=[MMD骨骼名,[xyz旋转],[xyz位移]]
for frame in frame_data:
        axis=world_rot([0,0,0])
        if ( frame[0] in dic_wrot ):
                print("Info: calculating",frame[0],"bone as",dic_mltd.get(frame[0]))
                axis=world_rot([0,0,0])
                print ("Info: parent bone chain is",frame[7])
                for parent_bone in frame[7]:
                        #print("For bone",frame[0],"calculating",parent_bone)
                        if (parent_bone in dic_wrot):
                                axis=axis*world_rot(dic_wrot.get(parent_bone))
                        else:
                                print("Warning: parent bone",parent_bone,"wrot is missing")
                if ( frame[0] in dic_wrot ):
                        #骨骼本身的世界旋转
                        origin_pose=axis*world_rot(dic_wrot.get(frame[0]))
                else:
                        print("Warning: bone",frame[0],"wrot is missing")
                
                out_rot=[]
                out_pos=[]
                for i in range(0,frame_len):
                        #应用动画后的世界旋转
                        target_pose=axis*unity_rot([frame[1][i],frame[2][i],frame[3][i]])
                        x_rot,y_rot,z_rot=mmd_rot(target_pose*origin_pose.inv())
                        out_rot.append([x_rot,y_rot,z_rot])
                        if ( frame[0] == "BASE"):
                               out_pos.append([frame[4][i],frame[5][i]-8.67,frame[6][i]])
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
        if ( high_fps == 1 ):
               if ( pos_id != 0 ) and ( len(pos_data) > 0 ):
                      print("Info: export motion with position id",pos_id)
                      outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len)+2*len(pos_data)-1)+'\n')
                      outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')

                      outfile.write('全ての親'+','+str(round(pos_data[0][0]*60))+','+str(round(pos_data[0][1],4))+','+str(round(pos_data[0][2],4))+','+str(round(pos_data[0][3],4))+',0,'+str(pos_data[0][4])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
                      for i in range(1,len(pos_data)):
                                     outfile.write('全ての親'+','+str(round(pos_data[i][0]*60)-1)+','+str(round(pos_data[i-1][1],4))+','+str(round(pos_data[i-1][2],4))+','+str(round(pos_data[i-1][3],4))+',0,'+str(pos_data[i-1][4])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
                                     outfile.write('全ての親'+','+str(round(pos_data[i][0]*60))+','+str(round(pos_data[i][1],4))+','+str(round(pos_data[i][2],4))+','+str(round(pos_data[i][3],4))+',0,'+str(pos_data[i][4])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
                                  
               elif ( pos_id != 0 ) and ( len(pos_data) == 0 ):
                      print("Info: export motion without position since position id",pos_id,"is out of range")
                      outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len))+'\n')
                      outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')

               else:
                      print("Info: export motion without position")
                      outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len))+'\n')
                      outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')

               for frame in out_data:
                      for i in range(0,frame_len):
                             outfile.write(str(frame[0])+','+str(i)+','+str(round(frame[2][i][0],4))+','+str(round(frame[2][i][1],4))+','+str(round(frame[2][i][2],4))+','+str(frame[1][i][0])+','+str(frame[1][i][1])+','+str(frame[1][i][2])+',False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')

        else:
               if ( pos_id != 0 ) and ( len(pos_data) > 0 ):
                      print("Info: export motion with position id",pos_id)
                      outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len/2)+2*len(pos_data)-1)+'\n')
                      outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')

                      outfile.write('全ての親'+','+str(round(pos_data[0][0]*60))+','+str(round(pos_data[0][1],4))+','+str(round(pos_data[0][2],4))+','+str(round(pos_data[0][3],4))+',0,'+str(pos_data[0][4])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
                      for i in range(1,len(pos_data)):
                                     outfile.write('全ての親'+','+str(round(pos_data[i][0]*30)-1)+','+str(round(pos_data[i-1][1],4))+','+str(round(pos_data[i-1][2],4))+','+str(round(pos_data[i-1][3],4))+',0,'+str(pos_data[i-1][4])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
                                     outfile.write('全ての親'+','+str(round(pos_data[i][0]*30))+','+str(round(pos_data[i][1],4))+','+str(round(pos_data[i][2],4))+','+str(round(pos_data[i][3],4))+',0,'+str(pos_data[i][4])+',0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')

               elif ( pos_id != 0 ) and ( len(pos_data) == 0 ):
                      print("Info: export motion without position since position id",pos_id,"is out of range")
                      outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len/2))+'\n')
                      outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')

               else:
                      print("Info: export motion without position")
                      outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len/2))+'\n')
                      outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')

               for frame in out_data:
                      for i in range(0,int(frame_len/2)):
                             outfile.write(str(frame[0])+','+str(i)+','+str(round(frame[2][2*i][0],4))+','+str(round(frame[2][2*i][1],4))+','+str(round(frame[2][2*i][2],4))+','+str(frame[1][2*i][0])+','+str(frame[1][2*i][1])+','+str(frame[1][2*i][2])+',False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')

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

import json
import os
import sys
import re
import numpy as np
import csv


#input_json = sys.argv[1]
input_json='./dan_cmfeel_01_dan.imo.asset.json'
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

dic_fix = {
}


global frame_len
global high_fps
high_fps=0
export_csv=1

def gen_list(key_type,value,rate=1,angle=0):
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
                                frame_list[i]=round( ((nxt_state-i)/delta)*value[2*pt+1] + ((i-prs_state)/delta)*value[2*pt+3]+angle , 5 )
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
                frame_list = [value[0]+angle] * frame_len
                        
        #FullFrame
        if ( key_type[0] == "FullFrame" ):
                #print("FullFrame - total",len(value),"frames with",rate,"zoom rate and",angle,"angle")
                if not ( len(value) == frame_len ):
                        print("Error: input FullFrame list length is",len(value),"unequal to expected frame length",frame_len)
                        exit(1)
                frame_list= [round(x*rate+angle,4) for x in value]


        #print("Return list length:",len(frame_list),", Min Value:",min(frame_list)," Max Value:",max(frame_list))
        return frame_list

#initial frame data
def data_init(dic,frame_len):
        frame_data= [['foo',[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len,[0]*frame_len] for i in range(len(dic))]
        i=0
        for t in dic:
                frame_data[i][0]=dic_mltd.get(t)
                i=i+1
        return frame_data


print("==== Info ====")
print("Input file:",os.path.basename(input_json))

data = json.load(infile)
frame_len = round(data["time_length"]*60)+1
frame_data = data_init(dic_mltd,frame_len)
csv_data=[]

print("time_length:",data["time_length"],"\nframe_length:",frame_len,"\n")

print("==== Start constructing ====")
curves = data["curves"]


for block in curves:
        path=str(block["path"])
        #所有亲骨骼
        path_group=path.split('/')
        #print(path_group)
        path=re.findall(r"[\/]?(\w+)+$",path)

        prop_type=re.findall(r"property_type (\w+)*",str(block["attribs"][0]))
        key_type=re.findall(r"key_type (\w+)*",str(block["attribs"][1]))
        value=block["values"]

        if (path[0] in dic_mltd):
                print("Path:",path[0],"| Map:",dic_mltd.get(path[0]),"| Property Type:",prop_type[0],"| Key type:",key_type[0],"| Value:",len(value))
                

                if ( str(path[0]+'_'+prop_type[0]) in dic_fix ):
                        angle=float(dic_fix.get(str(path[0]+'_'+prop_type[0])))
                else:
                        angle=0
                        
                            
                for index,array_value in enumerate(frame_data):
                            if ( dic_mltd.get(path[0]) == frame_data[index][0]):
                                    if ( prop_type[0] == "AngleX" ):
                                            #print("Insert AngleX data for bone",dic_mltd.get(path[0]))
                                            frame_data[index][1]=gen_list(key_type,value,1,angle)
                                            break
                                    if ( prop_type[0] == "AngleY" ):
                                            #print("Insert AngleY data for bone",dic_mltd.get(path[0]))
                                            frame_data[index][2]=gen_list(key_type,value,1,angle)
                                            break
                                    if ( prop_type[0] == "AngleZ" ):
                                            #print("Insert AngleZ data for bone",dic_mltd.get(path[0]))
                                            frame_data[index][3]=gen_list(key_type,value,1,angle)
                                            break
                                    if ( prop_type[0] == "PositionX" ):
                                            #print("Insert PositionX data for bone",dic_mltd.get(path[0]))
                                            frame_data[index][4]=gen_list(key_type,value,10,0)
                                            break
                                    if ( prop_type[0] == "PositionY" ):
                                            #print("Insert PositionY data for bone",dic_mltd.get(path[0]))
                                            frame_data[index][5]=gen_list(key_type,value,10,0)
                                            break
                                    if ( prop_type[0] == "PositionZ" ):
                                            #print("Insert PositionZ data for bone",dic_mltd.get(path[0]))
                                            frame_data[index][6]=gen_list(key_type,value,10,0)
                                            break
                                        

        else:
                print("Warning:",path[0],"is not in dic")
                
print("==== End constructing ====")

print("==== Start converting ====")
#for index,array_value in enumerate(frame_data):
#       
#        if ( frame_data[index][0] == "グルーブ" ):
#                print(frame_data[index][5])

with open(os.path.basename(input_json)+".txt", "w",encoding='utf-8') as outfile:
        outfile.write('version:,2\n')
        outfile.write('modelname:,foobar\n')
        if ( high_fps == 1 ):
                outfile.write('boneframe_ct:,'+str(len(frame_data))+'\n')
                outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
                for frame in frame_data:
                        for i in range(0,frame_len):
                                outfile.write(str(frame[0])+','+str(i)+','+str(frame[4][i])+','+str(frame[5][i])+','+str(frame[6][i])+','+str(frame[1][i])+','+str(frame[2][i])+','+str(frame[3][i])+',False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
        else:
                outfile.write('boneframe_ct:,'+str(len(frame_data)*int(frame_len/2))+'\n')
                outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
                for frame in frame_data:
                        for i in range(0,int(frame_len/2)):
                                outfile.write(str(frame[0])+','+str(i)+','+str(frame[4][2*i])+','+str(frame[5][2*i])+','+str(frame[6][2*i])+','+str(frame[1][2*i])+','+str(frame[2][2*i])+','+str(frame[3][2*i])+',False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')

        outfile.write('morphframe_ct:,0\n')
        outfile.write('camframe_ct:,0\n')
        outfile.write('lightframe_ct:,0\n')
        outfile.write('shadowframe_ct:,0\n')
        outfile.write('ik/dispframe_ct:,0\n')
print("Output:",os.path.basename(input_json)+".txt")
print("==== End converting ====")


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
        print("Output:",os.path.basename(input_json)+".csv")
        print("==== End output csv ====")



import json
import os
import csv
import re

input='ratata'
input_json='./'+input+'_scenario_sobj.json'
input_json_tate='./'+input+'_scenario_tate_sobj.json'
input_json_yoko='./'+input+'_scenario_yoko_sobj.json'

#口型param
dic_lip = {
0:"あ",1:"い",2:"う",3:"え",4:"お",50:"ん",
54:"close",56:"foo",
}

#眼睛param
dic_eye = {
1:"ウィンク２",2:"ウィンク２右",
3:"ウィンク",4:"ウィンク右",
}

print("==== Info ====")
lip_data = []
lip_flag=0
eye_data = []
eye_flag = 0
lrc_data = []
lrc_flag = 0

def lip_write(input_json,out_file=""):
    global lip_flag
    global lip_data
    
    with open(input_json, encoding='utf-8') as infile:
        data = json.load(infile)
        
    print("Info: input file - ",os.path.basename(input_json))
    scenario = data["scenario"]

    #初始为闭嘴状态
    prs_stat=54
    for block in scenario:
        if ( block["type"] == 43 ) and ( block["idol"] == 0 ):
            if ( block["param"] in dic_lip ):
                #打log用
                #print("time:",round(block["absTime"]*30),"| Param:",block["param"],"| Map:",dic_lip.get(block["param"]))
                if ( block["param"] != prs_stat ):
                    ftr_stat=block["param"]
                    #对除了闭嘴以外的口型注册帧
                    #为MMD着想，口型"i"需要用一帧而非两帧切换
                    if (prs_stat != 54) and (prs_stat != 1):
                    #当前状态口型归零
                        lip_data.append([dic_lip.get(prs_stat),round(block["absTime"]*30),1.0])
                        lip_data.append([dic_lip.get(prs_stat),round(block["absTime"]*30)+3,0.0])
                    elif (prs_stat == 1):
                        lip_data.append([dic_lip.get(prs_stat),round(block["absTime"]*30),1.0])
                        lip_data.append([dic_lip.get(prs_stat),round(block["absTime"]*30)+2,0.0])
                    if (ftr_stat != 54) and (ftr_stat != 1):
                    #下个状态口型置一
                        lip_data.append([dic_lip.get(ftr_stat),round(block["absTime"]*30),0.0])
                        lip_data.append([dic_lip.get(ftr_stat),round(block["absTime"]*30)+3,1.0])
                    elif (ftr_stat == 1):
                        lip_data.append([dic_lip.get(ftr_stat),round(block["absTime"]*30),0.0])
                        lip_data.append([dic_lip.get(ftr_stat),round(block["absTime"]*30)+2,1.0])
                    #切换状态
                    prs_stat=ftr_stat
            else:
                #不在字典里的情况
                print("Error: param",block["param"],"is not in dic")
                
            #口型完成,flag置一
            if ( lip_flag == 0 ):
                print("Info: lip write done")
                lip_flag=1

    if ( lip_flag == 0 ):
        print("Info: Lip data not found in",input_json)
        
    return lip_flag

def eye_write(input_json,out_file=""):
    global eye_flag
    global eye_data
    
    with open(input_json, encoding='utf-8') as infile:
        data = json.load(infile)
        
    print("Info: Input file:",os.path.basename(input_json))
    scenario = data["scenario"]
    
    #默认状态,0睁眼1闭眼2笑
    prs_stat_l=0
    prs_stat_r=0
    ftr_stat_l=0
    ftr_stat_r=0
    
    for block in scenario:
        if ( block["type"] == 45 ) and ( block["idol"] == 1 ):
            if ( block["eyeclose"] == 1 ) and  ( block["param"] == 9 ):
                #闭眼
                ftr_stat_l=1
                ftr_stat_r=2
            elif ( block["eyeclose"] == 0 ):
                if ( block["param"] == 5 ):
                #笑
                     ftr_stat_l=3
                     ftr_stat_r=4
                else:
                     ftr_stat_l=0
                     ftr_stat_r=0
                     
            #左眼
            if ( prs_stat_l != ftr_stat_l ):
                if ( prs_stat_l != 0 ):
                    eye_data.append([dic_eye.get(prs_stat_l),round(block["absTime"]*30),1.0])
                    eye_data.append([dic_eye.get(prs_stat_l),round(block["absTime"]*30)+2,0.0])
                if ( ftr_stat_l != 0 ):
                    eye_data.append([dic_eye.get(ftr_stat_l),round(block["absTime"]*30),0.0])
                    eye_data.append([dic_eye.get(ftr_stat_l),round(block["absTime"]*30)+2,1.0])
                prs_stat_l=ftr_stat_l

            #右眼
            if ( prs_stat_r != ftr_stat_r ):
                if ( prs_stat_r != 0 ):
                    eye_data.append([dic_eye.get(prs_stat_r),round(block["absTime"]*30),1.0])
                    eye_data.append([dic_eye.get(prs_stat_r),round(block["absTime"]*30)+2,0.0])
                if ( ftr_stat_r != 0 ):
                    eye_data.append([dic_eye.get(ftr_stat_r),round(block["absTime"]*30),0.0])
                    eye_data.append([dic_eye.get(ftr_stat_r),round(block["absTime"]*30)+2,1.0])
                prs_stat_r=ftr_stat_r
            
            if ( eye_flag == 0 ):
                print("Info: eye write done")
                eye_flag=1

    if ( eye_flag == 0 ):
        print("Info: Eye data not found in",input_json)

def lrc_write(input_json,out_file=""):
    global lrc_flag
    global lrc_data
    with open(input_json, encoding='utf-8') as infile:
        data = json.load(infile)

    print("Info: Input file:",os.path.basename(input_json))
    scenario = data["scenario"]
    for block in scenario:
        if ( block["type"] == 11 ):
            lrc_data.append([round(block["absTime"],2),re.sub(r"　"," ",block["str"])])
            if ( lrc_flag == 0 ):
                print("Info: lrc write done")
                lrc_flag=1
    
print("==== Start constructing ====")
#一个json里没数据就换一个
lip_write(input_json)
if ( lip_flag == 0 ):
    lip_write(input_json_tate)
if ( lip_flag == 0 ):
    lip_write(input_json_yoko)

eye_write(input_json)
if ( eye_flag == 0 ):
    eye_write(input_json_tate)
if ( eye_flag == 0 ):
    eye_write(input_json_yoko)

lrc_write(input_json)
if ( lrc_flag == 0 ):
    lrc_write(input_json_tate)
if ( lrc_flag == 0 ):
    lrc_write(input_json_yoko)
    
print("==== End constructing ====")
'''
for frame in lip_data:
    print(str(frame[0])+','+str(frame[1])+','+str(frame[2]))

exit()

for frame in eye_data:
    print(str(frame[0])+','+str(frame[1])+','+str(frame[2]))

exit()
'''


print("==== Start converting ====")
with open(os.path.basename(input_json)+"_facial.txt", "w",encoding='utf-8') as outfile:
        outfile.write('version:,2\n')
        outfile.write('modelname:,foobar\n')
        outfile.write('boneframe_ct:,0\n')
        #outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
        outfile.write('morphframe_ct:,'+str(len(lip_data)+len(eye_data))+'\n')
        outfile.write('morph_name,frame_num,value\n')
        #逐帧构造
        for frame in lip_data:
            outfile.write(str(frame[0])+','+str(frame[1])+','+str(frame[2])+'\n')
        for frame in eye_data:
            outfile.write(str(frame[0])+','+str(frame[1])+','+str(frame[2])+'\n')
        outfile.write('camframe_ct:,0\n')
        outfile.write('lightframe_ct:,0\n')
        outfile.write('shadowframe_ct:,0\n')
        outfile.write('ik/dispframe_ct:,0\n')
print("Output:",os.path.basename(input_json)+"_facial.txt")

with open(os.path.basename(input_json)+".ass", "w",encoding='utf-8') as outfile:
        outfile.write('[V4+ Styles]\n')
        outfile.write('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n')
        outfile.write('Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n')
        outfile.write('\n')
        outfile.write('[Events]\n')
        outfile.write('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')

        for i in range(0,len(lrc_data)-1):
            if( i != len(lrc_data) ):
                outfile.write('Dialogue: 0,'+str(int(lrc_data[i][0]/3600))+':'+str(int(lrc_data[i][0]/60)%60)+':'+str(round(lrc_data[i][0]%60,2))+','+str(int(lrc_data[i+1][0]/3600))+':'+str(int(lrc_data[i+1][0]/60)%60)+':'+str(round(lrc_data[i+1][0]%60,2))+',Default,,0,0,0,,'+lrc_data[i][1]+'\n')
            else:
                outfile.write('Dialogue: 0,'+str(int(lrc_data[i][0]/3600))+':'+str(int(lrc_data[i][0]/60)%60)+':'+str(round(lrc_data[i][0]%60,2))+','+str(int(lrc_data[i][0]/3600))+':'+str(int(lrc_data[i][0]/60)%60)+':'+str(round((lrc_data[i][0]+2)%60,2))+',Default,,0,0,0,,'+lrc_data[i][1]+'\n')
                
print("Output:",os.path.basename(input_json)+".ass")


print("==== End converting ====")




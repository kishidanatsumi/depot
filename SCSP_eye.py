import os,sys,json
infile='002_yumeas_01_exp.json'


#眼睛param
dic_eye = {
"CloseEye":"まばたき",
"":"ウィンク２",2:"ウィンク２右",
3:"ウィンク",4:"ウィンク右",
}

eye_data = []
eye_flag = 0

with open(infile, encoding='utf-8') as infile:
    data = json.load(infile)


    #默认状态,0睁眼1闭眼2笑
    prs_stat_l=0
    prs_stat_r=0
    ftr_stat_l=0
    ftr_stat_r=0
for s_data in data["events"]:
    name=s_data["eventName"]
    frame=s_data["startFrame"]
    arg1=s_data["arg1"]
    arg2=s_data["arg2"]
    if name=="CloseEyeSmile" :
        if arg1==10:
            prs_stat_l=2
            prs_stat_r=2
        elif arg1==3:
            prs_stat_l=2
        elif arg1==5:
            prs_stat_r=2
    elif name=="CloseEye" :
        if arg1==10:
            prs_stat_l=1
            prs_stat_r=1
        elif arg1==3:
            prs_stat_l=1
        elif arg1==5:
            prs_stat_r=1
    elif (name=="OpenEye") or (name=="OpenEyeSmile") :
        prs_stat_l=0
        prs_stat_r=0
    elif name=="Blink" :
            prs_stat_l=1
            prs_stat_r=1
            
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

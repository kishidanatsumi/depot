import os,sys,json


def eye_write(input_json):
    split=os.path.splitext(os.path.basename(input_json))
    out_name=split[0]
    eye_data = []
    eye_flag = 0
    with open(input_json, encoding='utf-8') as infile:
        data = json.load(infile)


    #默认状态,0睁眼1闭眼2笑3眨眼4眨眼笑
    pst_stat_l=0
    pst_stat_r=0
    prs_stat_l=0
    prs_stat_r=0
    ftr_stat_l=0
    ftr_stat_r=0
        
    for s_data in data["events"]:
            name=s_data["eventName"]
            frame=s_data["startFrame"]
            arg1=s_data["arg1"]
            arg2=s_data["arg2"]
            #print(name,frame,arg1,arg2)
            if name=="CloseEyeSmile" :
                    prs_stat_l=2
                    prs_stat_r=2
            elif name=="CloseEye" :
                    prs_stat_l=1
                    prs_stat_r=1
            elif (name=="OpenEye") or (name=="OpenEyeSmile") :
                    prs_stat_l=0
                    prs_stat_r=0
            elif name=="Blink" :
                    prs_stat_l=3
                    prs_stat_r=3
            elif name=="WinkLSmile":
                    prs_stat_l=4
            elif name=="WinkRSmile":
                    prs_stat_r=4
                
            elif name=="ChangeTarget" or name=="EyebrowAddUp" or name=="EyebrowAddDown" or name=="EyebrowSerious" or name=="EyebrowNormal" :
                pass
            else:
                print("Warning: No facial match -",name)


            #左眼
            if ( pst_stat_l != prs_stat_l ):
                if ( prs_stat_l == 1 ):
                    eye_data.append(["ウィンク２",frame,0.0])
                    eye_data.append(["ウィンク２",frame+4,1.0])
                elif ( prs_stat_l == 2 ):
                    eye_data.append(["ウィンク",frame,0.0])
                    eye_data.append(["ウィンク",frame+4,1.0])
                elif ( prs_stat_l == 3 ):
                    eye_data.append(["ウィンク２",frame,0.0])
                    eye_data.append(["ウィンク２",frame+4,1.0])
                    eye_data.append(["ウィンク２",frame+8,1.0])
                    eye_data.append(["ウィンク２",frame+12,0.0])
                elif ( prs_stat_l == 4 ):
                    eye_data.append(["ウィンク",frame,0.0])
                    eye_data.append(["ウィンク",frame+4,1.0])
                    eye_data.append(["ウィンク",frame+8,1.0])
                    eye_data.append(["ウィンク",frame+12,0.0])
                elif ( prs_stat_l == 0 ):
                    if pst_stat_l == 1:
                        eye_data.append(["ウィンク２",frame,1.0])
                        eye_data.append(["ウィンク２",frame+4,0.0])
                    elif pst_stat_l == 2:
                        eye_data.append(["ウィンク",frame,1.0])
                        eye_data.append(["ウィンク",frame+4,0.0])
                    else:
                        print("Warning:L eye can't reset.")

                pst_stat_l=prs_stat_l

            #右眼
            if ( pst_stat_r != prs_stat_r ):
                if ( prs_stat_r == 1 ):
                    eye_data.append(["ウィンク２右",frame,0.0])
                    eye_data.append(["ウィンク２右",frame+4,1.0])
                elif ( prs_stat_r == 2 ):
                    eye_data.append(["ウィンク右",frame,0.0])
                    eye_data.append(["ウィンク右",frame+4,1.0])
                elif ( prs_stat_r == 3 ):
                    eye_data.append(["ウィンク２右",frame,0.0])
                    eye_data.append(["ウィンク２右",frame+4,1.0])
                    eye_data.append(["ウィンク２右",frame+8,1.0])
                    eye_data.append(["ウィンク２右",frame+12,0.0])
                elif ( prs_stat_r == 4 ):
                    eye_data.append(["ウィンク右",frame,0.0])
                    eye_data.append(["ウィンク右",frame+4,1.0])
                    eye_data.append(["ウィンク右",frame+8,1.0])
                    eye_data.append(["ウィンク右",frame+12,0.0])
                elif ( prs_stat_r == 0 ):
                    if pst_stat_r == 1:
                        eye_data.append(["ウィンク右２",frame,1.0])
                        eye_data.append(["ウィンク右２",frame+4,0.0])
                    elif pst_stat_r == 2:
                        eye_data.append(["ウィンク右",frame,1.0])
                        eye_data.append(["ウィンク右",frame+4,0.0])
                    else:
                        print("Warning:R eye can't reset.",prs_stat_r,pst_stat_r)

                pst_stat_r=prs_stat_r
            


    with open(out_name+".txt", "w",encoding='utf-8') as outfile:
            outfile.write('version:,2\n')
            outfile.write('modelname:,foobar\n')
            outfile.write('boneframe_ct:,0\n')
            #outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
            outfile.write('morphframe_ct:,'+str(len(eye_data))+'\n')
            outfile.write('morph_name,frame_num,value\n')
            #逐帧构造

            for frame in eye_data:
                outfile.write(str(frame[0])+','+str(frame[1])+','+str(frame[2])+'\n')
            outfile.write('camframe_ct:,0\n')
            outfile.write('lightframe_ct:,0\n')
            outfile.write('shadowframe_ct:,0\n')
            outfile.write('ik/dispframe_ct:,0\n')
    print("Output:",os.path.basename(input_json)+"_facial.txt")

infile = sys.argv[1]
#infile='002_yumeas_01_exp.json'
if not os.path.exists(infile):
        print("don't exist")
        exit
else:
        eye_write(infile)



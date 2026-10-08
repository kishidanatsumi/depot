import math,os,csv,array
from scipy.spatial.transform import Rotation as rot

class vmd:
    def __init__(self,name,bone,facial,cam,light,shadow,ik):
        #name:string
        self.name=name
        
        #bone:list
        '''
        [0]骨骼名称 string
        [1]时间 int
        [2:4]x,y,z 位置 float
        [5:8],x,y,z,w 四元数旋转 float
        [9:24]:补间曲线
        [9:12]"X移动"左下点x/y 右上点x/y float
        [13:16]"Y移动"左下点x/y 右上点x/y float
        [17:20]"Z移动"左下点x/y 右上点x/y float
        [21:24]"旋转"左下点x/y 右上点x/y float
        '''
        self.bone=bone
        
        #facial:list
        '''
        [0]表情名称 string
        [1]时间 int
        [2]权重(0.0-1.0) float
        '''
        self.facial=facial

        #camera:list
        '''
        [0]时间 int
        [1]距离 float
        [2:4]x,y,z 位置 float
        [5:7],x,y,z 欧拉角旋转 float
        [8:24]:补间曲线 
        [8:11]"X移动"左下点x/y 右上点x/y float
        [12:15]"Y移动"左下点x/y 右上点x/y float
        [16:19]"Z移动"左下点x/y 右上点x/y float
        [20:23]"旋转"左下点x/y 右上点x/y float
        [24:27]"距离"左下点x/y 右上点x/y float
        [28:31]"FOV"左下点x/y 右上点x/y float
        [32:35]"FOV"左下点x/y 右上点x/y float
        [36]FOV int
        '''
        self.cam=cam

        #light:list
        '''
        [0]时间 int
        [1:3]照明RGB float
        [4:6]照明XYZ float
        '''
        self.light=light

        #shadow:list
        '''
        [0]时间 int
        [1]模式 int
        [2]阴影范围 float
        '''
        self.shadow=shadow

        '''
        [0]时间 int
        [1]模型表示 boolean
        [2]IK列表 list [IK名称 string,IK启用 boolean]
        '''
        self.ik=ik
        
    def show(self):
        print("Model name:",self.name)

def decode(name_raw):
    #print(model_name_raw)
    try:
        name=name_raw.decode('shift-jis')
    except UnicodeDecodeError:
        print("No name decoded")
        return
    return name

#struct.unpack('f',inbytes)
#IEEE 754 binary32
def bytes_to_float(inbytes):
    bits = 0
    #int_from bytes
    for i, b in enumerate(inbytes):
         bits |= b << (i * 8)  
    mantissa = ((bits&8388607)/8388608.0)
    exponent = (bits>>23)&255
    if (bits>>31) ==0:
        sign = 1.0 
    else:
        sign = -1.0
    if exponent != 0:
        mantissa+=1.0
    elif mantissa==0.0:
        return sign*0.0
    return sign*pow(2.0,exponent-127)*mantissa

def float_to_bytes(in_float):
    in_float=float(in_float)
    byte_array = array.array('f', [in_float])
    return byte_array.tobytes()

def bytes_to_int(inbytes):
    return int.from_bytes(inbytes, byteorder='little', signed=False)

def int_to_bytes(in_num:int,pad=4):
    in_num=int(in_num)
    return int.to_bytes(in_num,byteorder='little', signed=False,length=pad)

def pad(pad_data,width):
    if width < len(pad_data):
        print("error")
    elif width == len(pad_data):
        return pad_data
    else:
        return pad_data+b'\x00'*(width-len(pad_data))

def vmd_to_data(infile):
    is_camera=0
    vmd_data=vmd("",[],[],[],[],[],[])
    print("input file is:",infile)
    with open(os.path.splitext(os.path.basename(infile))[0]+".txt", "w",newline='',encoding='shift-jis') as out_file:
        out_writer=csv.writer(out_file, delimiter=',')
        with open(infile, 'rb') as f:
            data = f.read()
        #header
        #print(data[0:30])


        #model name
        model_name_raw=data[30:50].split(b'\x00')[0]
        #print(data[30:50])
        #print(model_name_raw)
        vmd_data.name=decode(model_name_raw)
        print("Model:",vmd_data.name)
        data=data[50:]
        
        #bone data
        bone_list=[]
        bone_frame=int.from_bytes(data[0:4], byteorder='little', signed=False)
        print("Bone frame:",bone_frame)
        data=data[4:]
        if (bone_frame != 0):
            for i in range(bone_frame):
                        block=data[111*i:111*(i+1)]
                        bone_name=decode(block[0:15].split(b'\x00')[0])
                        time=bytes_to_int(block[15:19])
                        #position
                        x=bytes_to_float(block[19:23])
                        y=bytes_to_float(block[23:27])
                        z=bytes_to_float(block[27:31])
                        #rotation
                        xr=bytes_to_float(block[31:35])
                        yr=bytes_to_float(block[35:39])
                        zr=bytes_to_float(block[39:43])
                        wr=bytes_to_float(block[43:47])
                        #interpolate curve
                        int_x_bl_x=bytes_to_int(block[47:48])
                        int_x_bl_y=bytes_to_int(block[51:52])
                        int_x_tr_x=bytes_to_int(block[55:56])
                        int_x_tr_y=bytes_to_int(block[59:60])
                        int_y_bl_x=bytes_to_int(block[63:64])
                        int_y_bl_y=bytes_to_int(block[67:68])
                        int_y_tr_x=bytes_to_int(block[71:72])
                        int_y_tr_y=bytes_to_int(block[75:76])
                        int_z_bl_x=bytes_to_int(block[79:80])
                        int_z_bl_y=bytes_to_int(block[83:84])
                        int_z_tr_x=bytes_to_int(block[87:88])
                        int_z_tr_y=bytes_to_int(block[91:92])
                        int_rot_bl_x=bytes_to_int(block[95:96])
                        int_rot_bl_y=bytes_to_int(block[99:100])
                        int_rot_tr_x=bytes_to_int(block[103:104])
                        int_rot_tr_y=bytes_to_int(block[107:108])
                        '''
                        bone_data=[bone_name,time,x,y,z,xr,yr,zr,wr,
                              int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                              int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                              int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                              int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y]
                        '''
                        vmd_data.bone.append([bone_name,time,x,y,z,xr,yr,zr,wr,
                              int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                              int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                              int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                              int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y])
                        
                        #print(int_data)
                        if (xr==0) and (yr==0) and (zr==0):
                                continue
        
                        #print(bone_data)
                        #in_rot=rot.from_quat([xr,yr,zr,wr])
                        #rot_x,rot_y,rot_z=in_rot.as_euler('zxy',degrees=True)
                        #print([-x,y,-z])
            data=data[111*(i+1):]

        #facial
        facial_frame=bytes_to_int(data[0:4])
        data=data[4:]
        print("Facial frame:",facial_frame)
        facial_list=[]
        if (facial_frame != 0):
            for i in range(facial_frame):
                    block=data[23*i:23*(i+1)]
                    facial_name=decode(block[0:15].split(b'\x00')[0])
                    time=bytes_to_int(block[15:19])
                    #print(block[0:15],facial_name)
                    weight=bytes_to_float(block[19:23])
                    #facial_data=[facial_name,time,weight]
                    vmd_data.facial.append([facial_name,time,weight])
            data=data[23*(i+1):]

        #cam
        cam_frame=bytes_to_int(data[0:4])
        data=data[4:]
        print("Camera frame:",cam_frame)
        cam_list=[]
        if (cam_frame != 0):
            if model_name_raw==b'\x83J\x83\x81\x83\x89\x81E\x8f\xc6\x96\xbe':
                pass
            for i in range(cam_frame):
                block=data[61*i:61*(i+1)]
                print(block)
                time=bytes_to_int(block[0:4])
                dist=bytes_to_float(block[4:8])
                x=bytes_to_float(block[8:12])
                y=bytes_to_float(block[12:16])
                z=bytes_to_float(block[16:20])
                xr=bytes_to_float(block[20:24])
                yr=bytes_to_float(block[24:28])
                zr=bytes_to_float(block[28:32])
                #interpolate curve
                int_x_bl_x=bytes_to_int(block[32:33])
                int_x_bl_y=bytes_to_int(block[33:34])
                int_x_tr_x=bytes_to_int(block[34:35])
                int_x_tr_y=bytes_to_int(block[35:36])
                int_y_bl_x=bytes_to_int(block[36:37])
                int_y_bl_y=bytes_to_int(block[37:38])
                int_y_tr_x=bytes_to_int(block[38:39])
                int_y_tr_y=bytes_to_int(block[39:40])
                int_z_bl_x=bytes_to_int(block[40:41])
                int_z_bl_y=bytes_to_int(block[41:42])
                int_z_tr_x=bytes_to_int(block[42:43])
                int_z_tr_y=bytes_to_int(block[43:44])
                int_rot_bl_x=bytes_to_int(block[44:45])
                int_rot_bl_y=bytes_to_int(block[45:46])
                int_rot_tr_x=bytes_to_int(block[46:47])
                int_rot_tr_y=bytes_to_int(block[47:48])
                int_dis_bl_x=bytes_to_int(block[48:49])
                int_dis_bl_y=bytes_to_int(block[49:50])
                int_dis_tr_x=bytes_to_int(block[50:51])
                int_dis_tr_y=bytes_to_int(block[51:52])
                int_fov_bl_x=bytes_to_int(block[52:53])
                int_fov_bl_y=bytes_to_int(block[53:54])
                int_fov_tr_x=bytes_to_int(block[54:55])
                int_fov_tr_y=bytes_to_int(block[55:56])
                
                fov=bytes_to_int(block[56:60])
                #24 value curve
                vmd_data.cam.append([time,dist,x,y,z,xr,yr,zr,
                              int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                              int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                              int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                              int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y,
                              int_dis_bl_x,int_dis_bl_y,int_dis_tr_x,int_dis_tr_y,
                              int_fov_bl_x,int_fov_bl_y,int_fov_tr_x,int_fov_tr_y,fov])
                print([time,dist,x,y,z,xr,yr,zr,
                              int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                              int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                              int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                              int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y,
                              int_dis_bl_x,int_dis_bl_y,int_dis_tr_x,int_dis_tr_y,
                              int_fov_bl_x,int_fov_bl_y,int_fov_tr_x,int_fov_tr_y,fov])
                data=data[61*(i+1):]

        #light
        light_frame=bytes_to_int(data[0:4])
        data=data[4:]
        print("Light frame:",light_frame)
        light_list=[]
        if (light_frame != 0):
            for i in range(light_frame):
                block=data[28*i:28*(i+1)]
                time=bytes_to_int(block[0:4])
                lightr=bytes_to_float(block[4:8])
                lightg=bytes_to_float(block[8:12])
                lightb=bytes_to_float(block[12:16])
                x=bytes_to_float(block[16:20])
                y=bytes_to_float(block[20:24])
                z=bytes_to_float(block[24:28])
                vmd_data.light.append([time,lightr,lightg,lightb,x,y,z])
                data=data[28*(i+1):]
        
        #shadow
        shadow_frame=bytes_to_int(data[0:4])
        data=data[4:]
        print("shadow frame:",shadow_frame)
        shadow_list=[]
        if (shadow_frame != 0):
            for i in range(shadow_frame):
                block=data[13*i:13*(i+1)]
                print(block)
                time=bytes_to_int(block[0:4])
                mode=bytes_to_int(block[4:5])
                
                shadow_range=round(10000 - (bytes_to_float(block[5:13]) * 100000))
                vmd_data.light.append([mode,shadow_range])
                data=data[13*(i+1):]


        #IK
        ik_frame=bytes_to_int(data[0:4])
        data=data[4:]
        print("ik frame:",ik_frame)
        if (ik_frame != 0):
            for i in range(ik_frame):
                time=bytes_to_int(data[0:4])
                ap=bytes_to_int(data[4:5])
                ik_number=bytes_to_int(data[5:9])
                ik_block=[time,ap,[]]
                data=data[9:]
                for i in range(ik_number):
                    name=decode(data[0:20].split(b'\x00')[0])
                    enable=bytes_to_int(data[20:21])
                    ik_block[2].append([name,enable])
                    data=data[21:]
                vmd_data.ik.append(ik_block)
            print(vmd_data.ik)

                
        print("Rest data is",data)

        
    return vmd_data
            
def data_to_txt(out_file,name="",bone=[],facial=[],cam=[],light=[],shadow=[],ik=[]):
    with open(out_file, 'w', newline='') as csvfile:
        out_writer = csv.writer(csvfile, delimiter=',')
        if len(facial) > 0 :
            for i in data:
                out_writer.writerow(["facial_frame"]+i) 
        if len(bone) > 0 :
            for i in bone:
                out_writer.writerow(["bone_frame"]+i) 
        if len(cam) > 0 :
            for i in cam:
                print(i)
                out_writer.writerow(["camera_example","name","time","dist","x","y","z","xr","yr","zr","20","108","20","108","20","108","20","108","20","108","20","108","20","108","20","108","20","108","20","108","20","108","20","108","fov"]) 
                out_writer.writerow(["camera_frame"]+i)
        if len(light) > 0 :
            for i in light:
                out_writer.writerow(["light_example","time","lightR","lightG","lightB","x","y","z"]) 
                out_writer.writerow(["light_frame"]+i) 
        if len(shadow) > 0 :
            for i in shadow:
                out_writer.writerow(["shadow_example","time","mode","range"]) 
                out_writer.writerow(["shadow_frame"]+i) 
        if len(ik) > 0 :
            for i in ik:
                out_writer.writerow(["ik_example","time","model_ap","ik list"])
                ik_bone=""
                for j in ik_data[2]:
                    ik_bone=ik_bone+str(j)
                out_writer.writerow(["ik_frame"]+ik_bone )

            
    return

def txt_to_data(in_txt):
    name=""
    bone_data=[]
    facial_data=[]
    cam_data=[]
    light_data=[]
    with open(in_txt, newline='', encoding='shift-jis') as in_csv:
        reader = csv.reader(in_csv, delimiter=',')
        for row in reader:
            if row[0]=="model_name":
                model_name=row[1]
            elif row[0]=="bone_frame":
                bone_data.appnd(row[1:])
            elif row[0]=="facial_frame":
                facial_data.appnd(row[1:])
            elif row[0]=="camera_frame":
                cam_data.append(row[1:])
            elif row[0]=="light_frame":
                light_data.append(row[1:])
            else:
                pass
    return(model_name,bone_data,facial_data,cam_data,light_data,shadow_data)

def data_to_vmd(name="NA",bone_data=[],facial_data=[],cam_data=[],light_data=[],shadow_data=[],ik_data=[]):
    #Header
    out_data=b'Vocaloid Motion Data 0002\x00\x00\x00\x00\x00'
    #model name
    out_data=out_data+pad(name.encode('shift-jis'),20)
    #bone
    out_data=out_data+int_to_bytes(len(bone_data))
    for bone in bone_data:
        out_data=out_data+pad(bone[0].encode('shift-jis'),15)+int_to_bytes(bone[1])+float_to_bytes(bone[2])+float_to_bytes(bone[3])+float_to_bytes(bone[4])+float_to_bytes(bone[5])+float_to_bytes(bone[6])+float_to_bytes(bone[7])+float_to_bytes(bone[8])
        #Interpolate curve
        for i in range(9,25):
            out_data=out_data+int_to_bytes(bone[i])
    #facial
    out_data=out_data+int_to_bytes(len(facial_data))
    for facial in facial_data:
        out_data=out_data+pad(facial[0].encode('shift-jis'),15)+int_to_bytes(facial[1])+float_to_bytes(facial[2])

    #cam
    out_data=out_data+int_to_bytes(len(cam_data))
    for cam in cam_data:
        out_data=out_data+int_to_bytes(cam[0])+float_to_bytes(cam[1])
        #move/rotate
        for i in range(2,8):
            out_data=out_data+float_to_bytes(cam[i])
        #curve
        for i in range(8,32):
            out_data=out_data+int_to_bytes(cam[i],1)
        #FOV
        out_data=out_data+int_to_bytes(cam[32],1)
    
    #light
    out_data=out_data+int_to_bytes(len(light_data))
    for light in light_data:
        out_data=out_data+int_to_bytes(light[0])
        #rgb
        for i in range(1,7):
            out_data=out_data+float_to_bytes(light[i])
            
    #shadow
    out_data=out_data+int_to_bytes(len(shadow_data))

    #ik
    out_data=out_data+int_to_bytes(len(ik_data))
    for ik in ik_data:
        #time
        out_data=out_data+int_to_bytes(ik[0])
        #ap
        out_data=out_data+int_to_bytes(ik[1],1)
        out_data=out_data+int_to_bytes(len(ik[2]))
        for ik_block in ik[2]:
            out_data=out_data+pad(ik_block[0].encode('shift-jis'),20)+int_to_bytes(ik_block[1],1)
        
        
    with open("out.vmd", "wb") as out_file:
        out_file.write(out_data)
  
infile='cam.vmd'
if infile.endswith(".txt"):
    print("txt to vmd")
elif infile.endswith(".vmd"):
    print("vmd to txt")
else:
    print("file is not txt or vmd, exit")
    exit()
vmd_data=vmd_to_data(infile)
data_to_vmd(name=vmd_data.name,bone_data=vmd_data.bone,facial_data=vmd_data.facial,cam_data=vmd_data.cam,light_data=vmd_data.light,ik_data=vmd_data.ik)
#data_to_txt(out_file="./out.txt",name=vmd_data.name,bone=vmd_data.bone,facial=vmd_data.facial,cam=vmd_data.cam,shadow=vmd_data.shadow,light=vmd_data.light,ik=vmd_data.ik)
data_to_txt(out_file="./out.txt",name=vmd_data.name,bone=vmd_data.bone,facial=vmd_data.facial,cam=vmd_data.cam,shadow=vmd_data.shadow,light=vmd_data.light,ik=vmd_data.ik)

import math,os,csv,array
# Load VMD file
from scipy.spatial.transform import Rotation as rot


def decode(name_raw):
    #print(model_name_raw)
    try:
       name=name_raw.decode("utf-8")
    except UnicodeDecodeError:
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
    byte_array = array.array('f', [in_float])
    return byte_array.tobytes()

float_num = 3.14
bytes_data = float_to_bytes(float_num)
print(bytes_data)

def bytes_to_int(inbytes):
    return int.from_bytes(inbytes, byteorder='little', signed=False)

def int_to_bytes(in_num):
    out_bytes = []
    for _ in range(4):
        out_bytes.append(in_num & 0xFF)
        in_num >>= 8
    #print(bytes(out_bytes))
    return bytes(out_bytes)

def pad(pad_data,width):
    if width < len(pad_data):
        print("error")
    elif width == len(pad_data):
        return pad_data
    else:
        return pad_data+b'\x00'*(width-len(pad_data))

def vmd_to_txt(infile):
        print("input file is:",infile)
        with open(os.path.splitext(os.path.basename(infile))[0]+".csv", "w",encoding='utf-8') as out_file:
            out_writer=csv.writer(out_file, delimiter=',')
            with open(infile, 'rb') as f:
                data = f.read()
            print(data[0:50])
            model_name_raw=data[30:50].split(b'\x00')[0]
            print(data[30:50])
            print(model_name_raw)
            model=decode(model_name_raw)
            print("Model:",model)
            data=data[50:]
            print("Bone data")
            bone_list=[]
            frame=int.from_bytes(data[0:4], byteorder='little', signed=False)
            print(data[0:4],"Frame:",frame)
            data=data[4:]
            if (frame != 0):
                    for i in range(frame):
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
                            bone_data=[bone_name,time,x,y,z,xr,yr,zr,wr,
                                  int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                                  int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                                  int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                                  int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y]
                            bone_list.append(bone_data)
                            
                            #print(int_data)
                            if (xr==0) and (yr==0) and (zr==0):
                                    continue
            
                            #print(bone_data)
                            in_rot=rot.from_quat([xr,yr,zr,wr])
                            rot_x,rot_y,rot_z=in_rot.as_euler('zxy',degrees=True)
                            #print([-x,y,-z])
                    data=data[111*(i+1):]

        
            print("Facial data")
            facial_list=[]
            frame=int.from_bytes(data[0:4], byteorder='little', signed=False)
            
            #print(data[0:4],"Frame:",frame)
            data=data[4:]
            if (frame != 0):
                    for i in range(frame):
                            block=data[23*i:23*(i+1)]
                            facial_name=decode(block[0:15].split(b'\x00')[0])
                            time=bytes_to_int(block[15:19])
                            #print(block[0:15],facial_name)
                            weight=bytes_to_float(block[19:23])
                            facial_data=[facial_name,time,weight]
                            facial_list.append(facial_data)
                    data=data[23*(i+1):]
            '''
            
            print("other data")
            frame=int.from_bytes(data[0:4], byteorder='little', signed=False)
            data=data[4:]
            print("Frame:",frame)
            print(len(bone_list))
            print(len(facial_list))
            print(facial_list)
            '''
            #write csv

            out_writer.writerow(["name",model])
            if len(facial_list) > 0 :
                for facial in facial_list:
                    out_writer.writerow(["facial"]+facial) 
            if len(bone_list) > 0 :
                for bone in bone_list:
                    out_writer.writerow(["bone"]+bone) 
        
        
        return [model,bone_list,facial_list]

def txt_to_vmd(in_data):
    '''
    model:string
    bone:list[bone_name,time,x,y,z,xr,yr,zr,wr
                              int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                              int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                              int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                              int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y]
    facial:list[facial_name,time,weight]
    '''
    #Header and model name
    out_data=b'Vocaloid Motion Data 0002\x00\x00\x00\x00\x00'+pad(in_data[0].encode('shift-jis'),20)
    #bone
    out_data=out_data+int_to_bytes(len(in_data[1]))
    #print(out_data)
    for bone in in_data[1]:
        out_data=out_data+pad(bone[0].encode('shift-jis'),15)+int_to_bytes(bone[1])+float_to_bytes(bone[2])+float_to_bytes(bone[3])+float_to_bytes(bone[4])+float_to_bytes(bone[5])+float_to_bytes(bone[6])+float_to_bytes(bone[7])+float_to_bytes(bone[8])

        #Interpolate curve
        for i in range(9,25):
            out_data=out_data+int_to_bytes(bone[i])
    #facial
    for facial in in_data[2]:
        out_data=out_data+pad(facial[0].encode('shift-jis'),15)+int_to_bytes(facial[1])+float_to_bytes(facial[2])
    with open("out.vmd", "wb") as out_file:
        out_file.write(out_data)
  
 

infile='test.vmd'
if infile.endswith(".txt"):
    print("txt to vmd")
elif infile.endswith(".vmd"):
    print("vmd to txt")
else:
    print("file is not txt or vmd, exit")
    exit()
vmd_data=vmd_to_txt(infile)
txt_to_vmd(vmd_data)



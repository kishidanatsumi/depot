import struct
import math
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

def print_info(in_data):
        return
    

#struct.unpack('f',inbytes)
#IEEE 754 binary32
def float_from_bytes(inbytes):
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

def int_from_bytes(inbytes):
    return int.from_bytes(inbytes, byteorder='little', signed=False)

def quaternion_to_euler(quat):
	"""
	Convert WXYZ quaternion to XYZ euler angles, using the same method as MikuMikuDance.
	Massive thanks and credit to "Isometric" for helping me discover the transformation method used in mmd!!!!
	
	:param quat: 4x float, W X Y Z quaternion
	:return: 3x float, X Y Z angle in degrees
	"""
	w, x, y, z = quat
	
	# pitch (y-axis rotation)
	sinr_cosp = 2 * ((w * y) + (x * z))
	cosr_cosp = 1 - (2 * ((x ** 2) + (y ** 2)))
	pitch = -math.atan2(sinr_cosp, cosr_cosp)
	
	# yaw (z-axis rotation)
	siny_cosp = 2 * ((-w * z) - (x * y))
	cosy_cosp = 1 - (2 * ((x ** 2) + (z ** 2)))
	yaw = math.atan2(siny_cosp, cosy_cosp)
	
	# roll (x-axis rotation)
	sinp = 2 * ((z * y) - (w * x))
	if sinp >= 1.0:
		roll = -math.pi / 2  # use 90 degrees if out of range
	elif sinp <= -1.0:
		roll = math.pi / 2
	else:
		roll = -math.asin(sinp)
	
	# fixing the x rotation, part 1
	if x ** 2 > 0.5 or w < 0:
		if x < 0:
			roll = -math.pi - roll
		else:
			roll = math.pi * math.copysign(1, w) - roll
	
	# fixing the x rotation, part 2
	if roll > (math.pi / 2):
		roll = math.pi - roll
	elif roll < -(math.pi / 2):
		roll = -math.pi - roll
	
	roll = math.degrees(roll)
	pitch = math.degrees(pitch)
	yaw = math.degrees(yaw)
	
	return roll, pitch, yaw


'''




xr  yr  zr  wr 

'''

motion_file='test.vmd'
print("input file is:",motion_file)
with open(motion_file, 'rb') as f:
        data = f.read()


model_name_raw=data[30:50].split(b'\x00')[0]
model=decode(model_name_raw)
print("Model:",model)
data=data[50:]
print("motion data")
#print(struct.unpack('I', raw[50:54])[0])
frame=int.from_bytes(data[0:4], byteorder='little', signed=False)
print("Frame:",frame)
data=data[4:]
if (frame != 0):
        for i in range(frame):
                block=data[111*i:111*(i+1)]
                bone_name=decode(block[0:15].split(b'\x00')[0])
                time=int_from_bytes(block[15:19])
                #position
                x=float_from_bytes(block[19:23])
                y=float_from_bytes(block[23:27])
                z=float_from_bytes(block[27:31])
                #rotation
                xr=float_from_bytes(block[31:35])
                yr=float_from_bytes(block[35:39])
                zr=float_from_bytes(block[39:43])
                wr=float_from_bytes(block[43:47])
                #interpolate curve
                int_x_bl_x=int_from_bytes(block[47:48])
                int_x_bl_y=int_from_bytes(block[51:52])
                int_x_tr_x=int_from_bytes(block[55:56])
                int_x_tr_y=int_from_bytes(block[59:60])
                int_y_bl_x=int_from_bytes(block[63:64])
                int_y_bl_y=int_from_bytes(block[67:68])
                int_y_tr_x=int_from_bytes(block[71:72])
                int_y_tr_y=int_from_bytes(block[75:76])
                int_z_bl_x=int_from_bytes(block[79:80])
                int_z_bl_y=int_from_bytes(block[83:84])
                int_z_tr_x=int_from_bytes(block[87:88])
                int_z_tr_y=int_from_bytes(block[91:92])
                int_rot_bl_x=int_from_bytes(block[95:96])
                int_rot_bl_y=int_from_bytes(block[99:100])
                int_rot_tr_x=int_from_bytes(block[103:104])
                int_rot_tr_y=int_from_bytes(block[107:108])
                
                bone_data=[bone_name,time,x,y,z,xr,yr,zr,
                      int_x_bl_x,int_x_bl_y,int_x_tr_x,int_x_tr_y,
                      int_y_bl_x,int_y_bl_y,int_y_tr_x,int_y_tr_y,
                      int_z_bl_x,int_z_bl_y,int_z_tr_x,int_z_tr_y,
                      int_rot_bl_x,int_rot_bl_y,int_rot_tr_x,int_rot_tr_y]

                #print(int_data)
                if (xr==0) and (yr==0) and (zr==0):
                        continue

                print(bone_data)
                in_rot=rot.from_quat([xr,yr,zr,wr])
                rot_x,rot_y,rot_z=in_rot.as_euler('zxy',degrees=True)
                #print([-x,y,-z])
        data=data[111*(i+1):]



print("facial data")
frame=int.from_bytes(data[0:4], byteorder='little', signed=False)
print("Frame:",frame)
data=data[4:]
if (frame != 0):
        for i in range(frame):
                block=data[23*i:23*(i+1)]
                facial_name=decode(block[0:15].split(b'\x00')[0])
                time=int_from_bytes(block[15:19])
                weight=float_from_bytes(block[19:23])
                facial_data=[facial_name,time,weight]
                print(facial_data)


        data=data[23*(i+1):]

print(data)


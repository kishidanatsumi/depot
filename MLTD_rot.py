'''
center-BASE
pos
0，12.14063，0
data
-1.1893551,-62.912117,-0.19129011
result
-0.191,-27.083,-1.189

上半身-Mune1
0，12.14063，0
data
0.8619723,-3.0989368,-80.454346
result
9.544,3.244,0.874

上半身-Mune2
0,15.20313,0
data
5.3078885,8.749775,-1.3530082
result
-2.143,5.041,8.718
'''



from scipy.spatial.transform import Rotation as rot
import numpy as np
import math

np.set_printoptions(suppress=True, precision=4)

base=[-3.7273958,-104.587364,3.335712]
mune1=[1.6418651,0.38942495,-88.09556]
mune2=[-0.8976578,4.232046,3.5085754]
basic_rot=[0,0,0]

#unity到MMD变换
def conv(in_rot):
    inv_rot=[]
    inv_rot=in_rot.as_quat()
    o_rot=rot.from_quat([-inv_rot[0],inv_rot[1],-inv_rot[2],inv_rot[3]])
    return o_rot

def mmd_rot(in_eular):
       in_quat=rot.from_euler('zyx',in_eular,degrees=True).as_quat()
       print(in_quat)
       x=float(-in_quat[0])
       y=float(-in_quat[1])
       z=float(-in_quat[2])
       w=float(in_quat[3])
       return rot.from_quat([z,y,x,w])


def unity_rot(in_euler):
    x,y,z=in_euler
    quat1=rot.from_euler('xyz',[-x,y,z],degrees=True).as_quat()
    quat2=rot.from_euler('xyz',[x,-y,-z],degrees=True).as_quat()
    out=[quat1[0],quat1[1],quat2[2],quat2[3]]

    return rot.from_quat(out)

#从PMX-VMD-Scripting-Tools扒下来的，可以将MMD的四元数转为MMD的欧拉角
def quaternion_to_euler(in_rot):
	"""
	Convert WXYZ quaternion to XYZ euler angles, using the same method as MikuMikuDance.
	Massive thanks and credit to "Isometric" for helping me discover the transformation method used in mmd!!!!
	
	:param quat: 4x float, W X Y Z quaternion
	:return: 3x float, X Y Z angle in degrees
	"""
	quat=in_rot.as_quat()
	x=quat[0]
	y=quat[1]
	z=quat[2]
	w=quat[3]
	# pitch (y-axis rotation)
	sinx_cosy = 2 * ((w * y) + (x * z))
	cosx_cosy = 1 - (2 * ((x ** 2) + (y ** 2)))
	mmd_y = -math.atan2(sinx_cosy, cosx_cosy)
	
	# yaw (z-axis rotation)
	sinz_cosy = 2 * ((-w * z) - (x * y))
	cosz_cosy = 1 - (2 * ((x ** 2) + (z ** 2)))
	mmd_z = math.atan2(sinz_cosy, cosz_cosy)
	
	# roll (x-axis rotation)
	siny = 2 * ((z * y) - (w * x))
	if siny >= 1.0:
		mmd_x = -math.pi / 2  # use 90 degrees if out of range
	elif siny <= -1.0:
		mmd_x = math.pi / 2
	else:
		mmd_x = -math.asin(siny)
	
	# fixing the x rotation, part 1
	if x ** 2 > 0.5 or w < 0:
		if x < 0:
			mmd_x = -math.pi - mmd_x
		else:
			mmd_x = math.pi * math.copysign(1, w) - mmd_x
	
	# fixing the x rotation, part 2
	if mmd_x > (math.pi / 2):
		mmd_x = math.pi - mmd_x
	elif mmd_x < -(math.pi / 2):
		mmd_x = -math.pi - mmd_x
	
	mmd_x = math.degrees(mmd_x)
	mmd_y = math.degrees(mmd_y)
	mmd_z = math.degrees(mmd_z)
	
	return [round(mmd_x,3), round(mmd_y,3), round(mmd_z,3)]


#子骨骼初始世界旋转: 亲骨骼*子骨骼1*子骨骼2....*子骨骼n
#子骨骼应用动画后的世界旋转：亲骨骼*子骨骼1*子骨骼2....*子骨骼n-1*动画旋转

#初始*目标=应用后
#目标=应用后*初始-1
#unity_rot*?=mmd_rot
#?=mmd_rot*unity_rot-1
basic=mmd_rot([0,0,0])
m00_wrot=mmd_rot([0,0,0])

base_wrot=mmd_rot([0,90,0])
base_rot=unity_rot(base)

mune1_wrot=mmd_rot([0,0,-90])
mune1_rot=unity_rot(mune1)

mune2_wrot=mmd_rot([0,0,-0])
mune2_rot=unity_rot(mune2)


#BASE
axis=basic
old=axis*base_wrot
new=axis*base_rot
print("axis",axis.as_euler('xyz', degrees=True))
print("org_pose",base_wrot.as_euler('xyz', degrees=True))
print("world_old",old.as_euler('xyz', degrees=True))
print("new_pose",base_rot.as_euler('xyz', degrees=True))
print("world_new",new.as_euler('xyz', degrees=True))
out=new*old.inv()
print("base1:",out.as_euler('xyz', degrees=True))
print("base1_mmd:",quaternion_to_euler(out))



#MUNE1
axis=basic*base_wrot
old=axis*mune1_wrot
new=axis*mune1_rot
print("axis",axis.as_euler('xyz', degrees=True))
print("org_pose",mune1_wrot.as_euler('xyz', degrees=True))
print("world_old",old.as_euler('xyz', degrees=True))
print("new_pose",mune1_rot.as_euler('xyz', degrees=True))
print("world_new",new.as_euler('xyz', degrees=True))
out=new*old.inv()
print("MUNE1:",out.as_euler('xyz', degrees=True))
print("MUNE1_mmd:",quaternion_to_euler(out))


#MUNE2
axis=basic*base_wrot*mune1_wrot
old=axis*mune2_wrot
new=axis*mune2_rot
print("axis",axis.as_euler('xyz', degrees=True))
print("org_pose",mune2_wrot.as_euler('xyz', degrees=True))
print("world_old",old.as_euler('xyz', degrees=True))
print("new_pose",mune2_rot.as_euler('xyz', degrees=True))
print("world_new",new.as_euler('xyz', degrees=True))
out=new*old.inv()
print("MUNE2:",out.as_euler('xyz', degrees=True))
print("MUNE2_mmd:",quaternion_to_euler(out))


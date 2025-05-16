import numpy as np
from scipy.spatial.transform import Rotation as rot

def QuaternionToEuler(quat):
    
    r11=2 * (quat[0] * quat[2] + quat[3] * quat[1])
    r12=quat[3] * quat[3] - quat[0] * quat[0] - quat[1] * quat[1] + quat[2] * quat[2]
    r21=-2*(quat[1] * quat[2] - quat[3] * quat[0])
    r31=2 * (quat[0] * quat[1] + quat[3] * quat[2])
    r32=quat[3] * quat[3] - quat[0] * quat[0] + quat[1] * quat[1] - quat[2] * quat[2]
    r0=np.atan2(r31,r32)
    r1=np.asin(r21)
    r2=np.atan2(r11,r12)
    #zxy
    return [r1,r2,r0]

def ComputeOrientation(quat):
    result=QuaternionToEuler(quat)
    result[0]=-result[0]
    #result[1]=result[1]+np.pi
    return result

def ComputeMmdOrientation(quat,rot_in):
    result=ComputeOrientation(quat)
    result[2]=-np.deg2rad(rot_in)
    return result

def FromAxisAngle(axis,rot):
    angle=0.5*rot
    axis=axis/np.linalg.norm(axis)
    axis=axis*np.sin(angle)
    w=np.cos(angle)

    return [axis[0],axis[1],axis[2],w]

def QuaternionLookAt(pos,tgt,unit):
    front = [0,0,1]
    delta=tgt-pos
    forward=delta/np.linalg.norm(delta)
    rotAxis=np.cross(forward,front)
    rotAxis=rotAxis/np.linalg.norm(rotAxis)
    dot=np.dot(forward,front)
    rotAngle=np.acos(dot)
    quat=FromAxisAngle(rotAxis,rotAngle)
    return quat


position=np.array([0.11443213,1.3318373,1.9295515])
target=np.array([-0.052588515,1.1825253,1.0897353])
rot_z=-338.40256

q = QuaternionLookAt(position,target,[0,1,0]);
mvd_rotation = ComputeMmdOrientation(q,rot_z);
vmd_rotation = mvd_rotation+np.array([np.pi,0,np.pi])
print(vmd_rotation)
print(np.rad2deg(vmd_rotation[0]),np.rad2deg(vmd_rotation[1]),np.rad2deg(vmd_rotation[2]))

delta=target-position
print("Position:",[-12.5*position[0],12.5*position[1],-12.5*position[2]])
print("Distance:",1.25*np.linalg.norm(delta))

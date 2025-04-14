import json
import os
import sys
import re
import numpy as np
import csv
from scipy.spatial.transform import Rotation as rot
import math

global frame_len
global high_fps
high_fps=0
export_csv=0

seq_dir=[[1,1,1],[1,1,-1],[1,-1,1],[1,-1,-1],[-1,1,1],[-1,1,-1],[-1,-1,1],[-1,-1,-1]]
rot_dir=["xyz","xzy","yxz","yzx","zxy","zyx"]

def mmd_rot(in_euler,seq_dir,rot_dir):
    x,y,z=in_euler
    if (rot_dir=="xyz"):
        rot_o=rot.from_euler('xyz',[seq_dir[0]*x,seq_dir[1]*y,seq_dir[2]*z],degrees=True)
    if (rot_dir=="xzy"):
        rot_o=rot.from_euler('xzy',[seq_dir[0]*x,seq_dir[1]*z,seq_dir[2]*y],degrees=True)
    if (rot_dir=="yzx"):
        rot_o=rot.from_euler('yzx',[seq_dir[0]*y,seq_dir[1]*z,seq_dir[2]*x],degrees=True)
    if (rot_dir=="yxz"):
        rot_o=rot.from_euler('yxz',[seq_dir[0]*y,seq_dir[1]*x,seq_dir[2]*z],degrees=True)
    if (rot_dir=="zxy"):
        rot_o=rot.from_euler('zxy',[seq_dir[0]*z,seq_dir[1]*x,seq_dir[2]*y],degrees=True)
    if (rot_dir=="zyx"):
        rot_o=rot.from_euler('zyx',[seq_dir[0]*z,seq_dir[1]*y,seq_dir[2]*x],degrees=True)
    return rot_o

def unity_rot(in_euler,seq_dir,rot_dir):
    x,y,z=in_euler
    if (rot_dir=="xyz"):
        rot_o=rot.from_euler('xyz',[seq_dir[0]*x,seq_dir[1]*y,seq_dir[2]*z],degrees=True)
    if (rot_dir=="xzy"):
        rot_o=rot.from_euler('xzy',[seq_dir[0]*x,seq_dir[1]*z,seq_dir[2]*y],degrees=True)
    if (rot_dir=="yzx"):
        rot_o=rot.from_euler('yzx',[seq_dir[0]*y,seq_dir[1]*z,seq_dir[2]*x],degrees=True)
    if (rot_dir=="yxz"):
        rot_o=rot.from_euler('yxz',[seq_dir[0]*y,seq_dir[1]*x,seq_dir[2]*z],degrees=True)
    if (rot_dir=="zxy"):
        rot_o=rot.from_euler('zxy',[seq_dir[0]*z,seq_dir[1]*x,seq_dir[2]*y],degrees=True)
    if (rot_dir=="zyx"):
        rot_o=rot.from_euler('zyx',[seq_dir[0]*z,seq_dir[1]*y,seq_dir[2]*x],degrees=True)
    return rot_o


#从PMX-VMD-Scripting-Tools扒下来的，可以将MMD的四元数转为MMD的欧拉角

def quaternion_to_euler(in_rot,rot_dir):
    if (rot_dir=="xyz"):
        x,y,z=in_rot.as_euler('xyz',degrees=True)
    if (rot_dir=="xzy"):
        x,z,y=in_rot.as_euler('xzy',degrees=True)
    if (rot_dir=="yzx"):
        y,z,x=in_rot.as_euler('yzx',degrees=True)
    if (rot_dir=="yxz"):
        y,x,z=in_rot.as_euler('yxz',degrees=True)
    if (rot_dir=="zxy"):
        z,x,y=in_rot.as_euler('zxy',degrees=True)
    if (rot_dir=="zyx"):
        z,y,x=in_rot.as_euler('zyx',degrees=True)
    return [round(x,4), round(y,4), round(z,4)]


for single_seq in seq_dir:
    for single_seq_o in seq_dir:
        for single_seq_u in seq_dir:
            for rot_seq in rot_dir:
                for rot_seq_o in rot_dir:
                    for rot_seq_u in rot_dir:
                        flag=1
                        #print("Checking rot seq:",single_seq,"unity seq:",single_seq_u,"mmd seq:",single_seq_o)    
                        #上半身
                        out_data_0=[]
                        axis_0=mmd_rot([0,90,0],single_seq,rot_seq)
                        origin_pose_0=axis_0*mmd_rot([0,0,-90],single_seq,rot_seq)
                        #上半身2
                        out_data_1=[]
                        axis_1=mmd_rot([0,90,0],single_seq,rot_seq)*mmd_rot([0,0,-90],single_seq,rot_seq)
                        origin_pose_1=axis_1*mmd_rot([0,0,0],single_seq,rot_seq)
                        #左肩
                        out_data_2=[]
                        axis_2=mmd_rot([0,90,0],single_seq,rot_seq)*mmd_rot([0,0,-90],single_seq,rot_seq)*mmd_rot([0,0,0],single_seq,rot_seq)
                        origin_pose_2=axis_2*mmd_rot([-90,-90,0],single_seq,rot_seq)
                        #左腕
                        out_data_3=[]
                        axis_3=mmd_rot([0,90,0],single_seq,rot_seq)*mmd_rot([0,0,-90],single_seq,rot_seq)*mmd_rot([0,0,0],single_seq,rot_seq)*mmd_rot([-90,-90,0],single_seq,rot_seq)
                        origin_pose_3=axis_3*mmd_rot([-90,0,0],single_seq,rot_seq)
                        #左bishi
                        out_data_4=[]
                        axis_4=mmd_rot([0,90,0],single_seq,rot_seq)*mmd_rot([0,0,-90],single_seq,rot_seq)*mmd_rot([0,0,0],single_seq,rot_seq)*mmd_rot([-90,-90,0],single_seq,rot_seq)*mmd_rot([-90,0,0],single_seq,rot_seq)
                        origin_pose_4=axis_4*mmd_rot([0,0,0],single_seq,rot_seq)    
                        #atama
                        out_data_5=[]
                        axis_5=mmd_rot([0,90,0],single_seq,rot_seq)*mmd_rot([0,0,-90],single_seq,rot_seq)*mmd_rot([0,0,0],single_seq,rot_seq)
                        origin_pose_5=axis_5*mmd_rot([90,0,-90],single_seq,rot_seq)    
                                            
                
                        target_pose_0=axis_0*unity_rot([1.6418651,0.38942495,-88.09556],single_seq_u,rot_seq_u)
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose_0*origin_pose_0.inv(),rot_seq_o)
                        out_rot_0=[single_seq_o[0]*x_rot,single_seq_o[1]*y_rot,single_seq_o[2]*z_rot]
                        if ( out_rot_0 != [np.float64(1.9037), np.float64(-0.3348), np.float64(1.6428)]):
                            #print(out_rot_0)
                            #print("mune1 yes")
                                            flag=0
                            
                        target_pose_1=axis_1*unity_rot([-0.8976578,4.232046,3.5085754],single_seq_u,rot_seq_u)
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose_1*origin_pose_1.inv(),rot_seq_o)
                        out_rot_1=[single_seq_o[0]*x_rot,single_seq_o[1]*y_rot,single_seq_o[2]*z_rot]
                        if ( out_rot_1 != [np.float64(3.5652), np.float64(-0.636), np.float64(4.2397)]):
                            #print(out_rot_1)
                            #print("mune2 yes")
                                            flag=0
                        
                    
                        target_pose_2=axis_2*unity_rot([-88.78447,175.93073,-90],single_seq_u,rot_seq_u)
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose_2*origin_pose_2.inv(),rot_seq_o)
                        out_rot_2=[single_seq_o[0]*x_rot,single_seq_o[1]*y_rot,single_seq_o[2]*z_rot]
                        if ( out_rot_2 != [np.float64(-0.0863), np.float64(-1.2125), np.float64(-4.0684)]):
                            #print(out_rot_2)
                            #print("shoulder yes")
                                            flag=0
                    
                        target_pose_3=axis_3*unity_rot([-7.7261405,-17.946653,20.864456],single_seq_u,rot_seq_u)
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose_3*origin_pose_3.inv(),rot_seq_o)
                        out_rot_3=[single_seq_o[0]*x_rot,single_seq_o[1]*y_rot,single_seq_o[2]*z_rot]
                        if ( out_rot_3 != [np.float64(-67.811), np.float64(-52.6248), np.float64(69.1469)]):
                            #print(out_rot_3)
                            #print("wrist yes")
                                            flag=0
                            
                        target_pose_4=axis_4*unity_rot([0,0,123.146835],single_seq_u,rot_seq_u)
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose_4*origin_pose_4.inv(),rot_seq_o)
                        out_rot_4=[single_seq_o[0]*x_rot,single_seq_o[1]*y_rot,single_seq_o[2]*z_rot]
                        if ( out_rot_4 != [np.float64(0), np.float64(-123.1468), np.float64(0)]):
                            #print(out_rot_4)
                            #print("bishi yes")
                                            flag=0
            
                        target_pose_5=axis_5*unity_rot([-5.7044616,-89.27333,-110.22813],single_seq_u,rot_seq_u)
                        x_rot,y_rot,z_rot=quaternion_to_euler(target_pose_5*origin_pose_5.inv(),rot_seq_o)
                        out_rot_5=[single_seq_o[0]*x_rot,single_seq_o[1]*y_rot,single_seq_o[2]*z_rot]
                        if ( out_rot_5 != [np.float64(-5.6035), np.float64(20.2552), np.float64(-1.2934)]):
                        #print(out_rot_5)
                            #print("bishi yes")
                                            flag=0
            
                        if (flag==1):
                                            print("base seq:",single_seq,"unity seq:",single_seq_u,"mmd seq:",single_seq_o)
                                            print("rot seq:",rot_seq,"unity rot seq:",rot_seq_u,"mmd rot seq:",rot_seq_o)
            

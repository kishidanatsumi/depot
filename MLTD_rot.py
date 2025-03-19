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


np.set_printoptions(suppress=True, precision=3)

base=[-1.1893551,-62.912117,-0.191290110]
base_2=[-0.191290110,27.087883,-1.1893551]

mune1=[0.8619723,-3.0989368,-80.454346]
mune2=[5.3078885,-8.749775,-1.3530082]
basic_rot=[0,0,0]


base_pos=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,12.14063,0,1]])
mune1_pos=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,12.14063,0,1]])
mune2_pos=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,15.20313,0,1]])
basic_pos=np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])




base_ma=np.zeros((4, 4))
mune1_ma=np.zeros((4, 4))
mune2_ma=np.zeros((4, 4))


base1=rot.from_euler('xyz',base, degrees=True)
base2=rot.from_euler('xyz',base_2, degrees=True)
print(base1.as_matrix())
print(base2.as_matrix())

#扩至空间变换矩阵
def conv_mat(in_mat):
    o_mat=np.vstack((np.hstack((in_mat,[[0],[0],[0]])),[0,0,0,1]))
    return o_mat

#unity到MMD变换
def conv(in_rot):
    inv_rot=[]
    inv_rot=in_rot.as_quat()
    o_rot=rot.from_quat([inv_rot[0],inv_rot[1],-inv_rot[2],-inv_rot[3]])
    return o_rot
    
'''
def (name,in_mat,pos=[0,0,0],in_ang):
    o_ang=[0,0,0]
    #A1*A2*......*当前骨骼
    o_mat=in_mat*
    return o_ang,o_mat
'''



#试试只算第一级
#Mbp(t)*Mb(t)*[Mbw(0)−1]=Map(t)×Ma(t)×[Maw(0)−1]
#Mb(t)=Mbp(t)−1×Map(t)×Ma(t)×[Maw(0)−1]×Mbw(0)

A1 = rot.from_euler('xyz',base, degrees=True)
A2 = rot.from_euler('xyz',mune1, degrees=True)
A3 = rot.from_euler('xyz',mune2, degrees=True)
basic = rot.from_euler('xyz',basic_rot, degrees=True)

B1=conv(A1)
B2=conv(A2)
B3=conv(A3)
basic_i=conv(basic)

ap=A1*A2
bp=B1*B2



m_ap=conv_mat(ap.as_matrix())
m_bp=conv_mat(bp.as_matrix())

print("A3",A3.as_quat())
print("B3",B3.as_quat())





print("m_ap",m_ap)
print("m_bp",m_bp)

m_p=np.linalg.inv(m_bp)@m_ap
print("m_p\n",m_p)
m_a3=conv_mat(A3.as_matrix())
print("m_a3\n",m_a3)



#Mb(t)=Mbp(t)−1×Map(t)×Ma(t)×[Maw(0)−1]×Mbw(0)
m_o=m_p@m_a3@np.linalg.inv(mune2_pos)@mune2_pos
m_o=np.delete(m_o,-1,axis=0)
m_o=np.delete(m_o,-1,axis=1)

print("m_o\n",np.array(m_o))
m_o=rot.from_matrix(m_o)
print("output_rotation:",m_o.as_euler('xyz', degrees=True))



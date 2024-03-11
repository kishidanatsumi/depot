import json 
import sys
import os
input_json = sys.argv[1]
infile =open(input_json)
print("Input file:",os.path.basename(input_json))

data = json.load(infile)
x_value = data["pos_x"]["m_Curve"]
z_value = data["pos_z"]["m_Curve"]
#result_array = [{"time": entry["time"], "value": entry["value"]} for entry in curve_data]
time_x = [entry["time"] for entry in x_value]
array_x = [entry["value"] for entry in x_value]
time_z = [entry["time"] for entry in z_value]
array_z = [entry["value"] for entry in z_value]
print("time_x:",len(time_x),"value_x:",len(array_x),"\ntime_z:",len(time_z),"value_z:",len(array_z))


i = 0
z_pointer = 0

#fix
while (i < len(time_x)):
    if (time_x[i] != time_z[i-z_pointer]):
        z_pointer=z_pointer+1
        fix_value=(array_z[i-1]+array_z[i-1])/2
        array_z.insert(i-1,fix_value)
        print("Frame",i,"is unequal, insert fix_value",fix_value)
        i=i+1
    else:
        #print (time_x[i],time_z[i - z_pointer])
        i=i+1

i = 0

with open(os.path.basename(input_json)+".txt", "w",encoding='utf-8') as outfile:
    outfile.write('version:,2\n')
    outfile.write('modelname:,foobar\n')
    outfile.write('boneframe_ct:,'+str(len(time_x))+'\n')
    outfile.write('bone_name,frame_num,Xpos,Ypos,Zpos,Xrot,Yrot,Zrot,phys_disable,interp_x_ax,interp_x_ay,interp_x_bx,interp_x_by,interp_y_ax,interp_y_ay,interp_y_bx,interp_y_by,interp_z_ax,interp_z_ay,interp_z_bx,interp_z_by,interp_r_ax,interp_r_ay,interp_r_bx,interp_r_by\n')
    while (i < len(time_x)):
        outfile.write('センター,'+str(i)+','+str(-(array_x[i])*10)+',0.0,'+str(array_z[i]*10)+',0.0,0.0,0.0,False,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127\n')
        i=i+1
    outfile.write('morphframe_ct:,0\n')
    outfile.write('camframe_ct:,0\n')
    outfile.write('lightframe_ct:,0\n')
    outfile.write('shadowframe_ct:,0\n')
    outfile.write('ik/dispframe_ct:,0\n')

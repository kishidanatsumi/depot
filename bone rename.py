import bpy
import re
import datetime
print("=== Start at",datetime.datetime.now().strftime('%X'),"===")

def rename_test(str_in):
    rename=""
#    print(str_in)
    if (str_in == "Neck"):
        rename="首"
        
    elif (str_in == "Head"):
        rename="頭"
      
    if (rename != ""):
        bpy.context.active_object.data.bones[str_in].name = rename
        print("bone",str_in,"has been renamed to",rename)
        
obj=bpy.context.active_object
print("Armature selected:",obj.name)
print("The current armature has",len(obj.data.bones),"Bones")

for single_bone in obj.data.bones:
    rename_test(single_bone.name)

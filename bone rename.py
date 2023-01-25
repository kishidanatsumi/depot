import bpy
import re
import datetime
print("=== Start at",datetime.datetime.now().strftime('%X'),"===")
 
def rename_cgss(str_in):
    rename=""
#    print(str_in)
    if (str_in == "Root"):
        rename="全ての親"
        
    elif (str_in == "Neck"):
        rename="首"
        
    elif (str_in == "Head"):
        rename="頭"
        
    elif (str_in == "Waist"):
        rename="上半身1"
        
    elif (str_in == "Chest"):
        rename="上半身2"
        
    elif (str_in == "Shoulder_L"):
        rename="左肩"
        
    elif (str_in == "Arm_L"):
        rename="左腕"
        
    elif (str_in == "Elbow_L"):
        rename="左ひじ"
        
    elif (str_in == "Wrist_L"):
        rename="左手首"
        
    elif (str_in == "Thigh_L"):
        rename="左足"
        
    elif (str_in == "Knee_L"):
        rename="左ひざ"
        
    elif (str_in == "Ankle_L"):
        rename="左足首"
        
    elif (str_in == "Toe_L"):
        rename="左つま先"
        
    elif (str_in == "Thumb_01_L"):
        rename="左親指０"
        
    elif (str_in == "Thumb_02_L"):
        rename="左親指１"
        
    elif (str_in == "Thumb_03_L"):
        rename="左親指２"
        
    elif (str_in == "Iindex_01_L"):
        rename="左人指１"
        
    elif (str_in == "Index_02_L"):
        rename="左人指２"
        
    elif (str_in == "Index_03_L"):
        rename="左人指３"
        
    elif (str_in == "Middle_01_L"):
        rename="左中指１"
        
    elif (str_in == "Middle_02_L"):
        rename="左中指２"
        
    elif (str_in == "Middle_03_L"):
        rename="左中指３"
        
    elif (str_in == "Ring_01_L"):
        rename="左薬指１"
        
    elif (str_in == "Ring_02_L"):
        rename="左薬指２"
        
    elif (str_in == "Ring_03_L"):
        rename="左薬指３"
        
    elif (str_in == "Pinky_01_L"):
        rename="左小指１"
        
    elif (str_in == "Pinky_02_L"):
        rename="左小指２"
        
    elif (str_in == "Pinky_03_L"):
        rename="左小指３"
        
    elif (str_in == "Shoulder_R"):
        rename="右肩"
        
    elif (str_in == "Arm_R"):
        rename="右腕"
        
    elif (str_in == "Elbow_R"):
        rename="右ひじ"
        
    elif (str_in == "Wrist_R"):
        rename="右手首"
        
    elif (str_in == "Thigh_R"):
        rename="右足"
        
    elif (str_in == "Knee_R"):
        rename="右ひざ"
        
    elif (str_in == "Ankle_R"):
        rename="右足首"
        
    elif (str_in == "Toe_R"):
        rename="右つま先"
        
    elif (str_in == "Thumb_01_R"):
        rename="右親指０"
        
    elif (str_in == "Thumb_02_R"):
        rename="右親指１"
        
    elif (str_in == "Thumb_03_R"):
        rename="右親指２"
        
    elif (str_in == "Iindex_01_R"):
        rename="右人指１"
        
    elif (str_in == "Index_02_R"):
        rename="右人指２"
        
    elif (str_in == "Index_03_R"):
        rename="右人指３"
        
    elif (str_in == "Middle_01_R"):
        rename="右中指１"
        
    elif (str_in == "Middle_02_R"):
        rename="右中指２"
        
    elif (str_in == "Middle_03_R"):
        rename="右中指３"
        
    elif (str_in == "Ring_01_R"):
        rename="右薬指１"
        
    elif (str_in == "Ring_02_R"):
        rename="右薬指２"
        
    elif (str_in == "Ring_03_R"):
        rename="右薬指３"
        
    elif (str_in == "Pinky_01_R"):
        rename="右小指１"
        
    elif (str_in == "Pinky_02_R"):
        rename="右小指２"
        
    elif (str_in == "Pinky_03_R"):
        rename="右小指３"
       
    else:
        rename=""
    
    if (rename != ""):
        bpy.context.active_object.data.bones[str_in].name = rename
        print("bone",str_in,"has been renamed to",rename)
        
obj=bpy.context.active_object
print("Armature selected:",obj.name)
print("The current armature has",len(obj.data.bones),"Bones")

for single_bone in obj.data.bones:
    rename_cgss(single_bone.name)

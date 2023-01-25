import bpy
import re
import datetime
print("=== Start at",datetime.datetime.now().strftime('%X'),"===")

dic_cgss = {
"Position":"全ての親",
"Hip":"下半身","Root":"上半身0","Neck":"首","Head":"頭","Waist":"上半身1","Chest":"上半身2",

"Shoulder_L":"左肩","Arm_L":"左腕","Elbow_L":"左ひじ","Wrist_L":"左手首",
"Thigh_L":"左足","Knee_L":"左ひざ","Ankle_L":"左足首","Toe_L":"左つま先",

"Thumb_01_L":"左親指０","Thumb_02_L":"左親指１","Thumb_03_L":"左親指２",
"Iindex_01_L":"左人指１","Index_02_L":"左人指２","Index_03_L":"左人指３",
"Middle_01_L":"左中指１","Middle_02_L":"左中指２","Middle_03_L":"左中指３",
"Ring_01_L":"左薬指１","Ring_02_L":"左薬指２","Ring_03_L":"左薬指３",
"Pinky_01_L":"左小指１","Pinky_02_L":"左小指２","Pinky_03_L":"左小指３",

"Shoulder_R":"右肩","Arm_R":"右腕","Elbow_R":"右ひじ","Wrist_R":"右手首",
"Thigh_R":"右足","Knee_R":"右ひざ","Ankle_R":"右足首","Toe_R":"右つま先",

"Thumb_01_R":"右親指０","Thumb_02_R":"右親指１","Thumb_03_R":"右親指２",
"Iindex_01_R":"右人指１","Index_02_R":"右人指２","Index_03_R":"右人指３",
"Middle_01_R":"右中指１","Middle_02_R":"右中指２","Middle_03_R":"右中指３",
"Ring_01_R":"右薬指１","Ring_02_R":"右薬指２","Ring_03_R":"右薬指３",
"Pinky_01_R":"右小指１","Pinky_02_R":"右小指２","Pinky_03_R":"右小指３"
}

obj=bpy.context.active_object
print("Armature selected:",obj.name)
print("The current armature has",len(obj.data.bones),"Bones")

for single_bone in obj.data.bones:
    rename=""
    name_in=single_bone.name
    
    if name_in not in dic_cgss.keys():
        continue
    
    else:
        rename=dic_cgss[name_in]
        bpy.context.active_object.data.bones[name_in].name = rename
        print("bone",name_in,"has been renamed to",rename)
        
print("=== Done. ===")

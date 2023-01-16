import bpy
import re
print("Start")
#get object name
for object in bpy.context.selectable_objects:
    print("Selected:",object.name)
    if re.search(r"md_chr.*_.*", object.name):
     object_sel=object.name
     break

#set active to armature
bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_sel]

bpy.context.object.data.display_type = 'WIRE'

#get all animations
action = bpy.data.actions

for act in action:
   bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_sel]
   bpy.context.object.animation_data.action = bpy.data.actions.get(act.name)
   print("Apply:",act)
   bpy.context.view_layer.objects.active = bpy.context.scene.objects["M_Head"]
   bpy.ops.object.modifier_apply_as_shapekey(keep_modifier = True, modifier = object_sel, report = True)
   
   bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_sel]
   bpy.ops.object.mode_set(mode = 'POSE')
   bpy.ops.pose.select_all(action='SELECT')
   bpy.ops.pose.transforms_clear()
   bpy.ops.object.mode_set(mode = 'OBJECT')


#rename
bpy.context.view_layer.objects.active = bpy.context.scene.objects["M_Head"]
length=len(action)

for num in range(0,length):
 act_str=str(action[num])
 match=re.search("(face.*?)\|", act_str)
 result=match.group(1)
 bpy.context.object.active_shape_key_index = num + 1
 bpy.context.object.active_shape_key.name = result
 
print("Done")

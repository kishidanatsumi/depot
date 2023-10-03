#跟着专栏重构了一遍
import bpy
import re
print("Start")

error_flag=0

for object in bpy.context.selected_objects:
    print("Selected:",object.name)
    if re.search(r"md_chr.*_.*", object.name):
        object_sel=object.name
    break

def convert(input_object):
    action = bpy.data.actions
    for act in action:
        bpy.context.object.animation_data.action = bpy.data.actions.get(act.name)
        print("Apply:",act.name)
        bpy.context.view_layer.objects.active = bpy.context.scene.objects["M_Head"]
        modifier_name = re.search("face[^|]*",act.name).group()
        bpy.context.object.modifiers[0].name = modifier_name
        bpy.ops.object.modifier_apply_as_shapekey(keep_modifier = True, modifier = modifier_name, report = True)
        bpy.context.view_layer.objects.active = bpy.context.scene.objects[input_object]
        bpy.ops.object.mode_set(mode = 'POSE')
        bpy.ops.pose.select_all(action='SELECT')
        bpy.ops.pose.transforms_clear()
        bpy.ops.object.mode_set(mode = 'OBJECT')

def clean_action(input_object):
    global error_flag
    if len(bpy.data.actions) > 0:
       for act_single in bpy.data.actions:
           if not re.search(input_object, act_single.name):
                act_single.use_fake_user = False
                print ('Action:',act_single.name,'not match, removed')
                error_flag=1

bpy.context.view_layer.objects.active = bpy.context.scene.objects[object_sel]
clean_action(object_sel)

if ('object_sel' in locals()) and (error_flag == 0):
    print('Target object:',object_sel)
    convert(object_sel)
elif (error_flag == 1):
    print('Error:Action unmatch')
else:
    print('Error:Target does not exist')

print("End")

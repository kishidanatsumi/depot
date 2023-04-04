import bpy
import re

#合并mesh上的口部表情
bpy.ops.object.join_shapes()

#将各帧形变应用为形态键
for i in range (0, 105):
    bpy.context.scene.frame_current = i*5
    modifier_name=bpy.context.active_object.modifiers[0].name
    bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier=modifier_name, report=True)

#重命名
bpy.ops.object.shape_key_clear()
for i in range (33, 137): ## 33 = index of shape key 'armature' + 1; 137 = 33 + number of the shape keys from the armature animation
    obj = bpy.context.active_object #### new shapekey from mix
    obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index(modifier_name) ##set active key for calibration
    obj.active_shape_key.slider_min = -1 ##set key range_min
    obj.active_shape_key.value = -1 ##set key value
    obj.active_shape_key_index = 33 ##set active key
    obj.active_shape_key.value = 1 ##set key value
    obj.shape_key_add(name=str("Expression" + str(i)), from_mix=True) ##new shape from mix
    obj.active_shape_key_index = 33 ##delete active key
    bpy.ops.object.shape_key_remove()
    obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index(modifier_name)
    obj.active_shape_key.slider_min = 0 ##reset range
    bpy.ops.object.shape_key_clear()

#删除多余mesh
for single_obj in bpy.context.selectable_objects:
    matched = e.search("(Morph.*)", single_obj.name)
 #exceptions if action name do not contain "|"
    if not matched:
        continue
    print(single_obj.name)
    bpy.data.objects.remove(single_obj)

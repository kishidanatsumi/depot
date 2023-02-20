
## modifier to shapekey
for i in range (0, 105):
    bpy.context.scene.frame_current = i*5
    bpy.ops.object.modifier_apply_as_shapekey(keep_modifier=True, modifier='Armature', report=True)




bpy.ops.object.shape_key_clear()
for i in range (33, 137): ## 33 = index of shape key 'armature' + 1; 137 = 33 + number of the shape keys from the armature animation
    obj = bpy.context.active_object #### new shapekey from mix
    obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index("Armature") ##set active key for calibration
    obj.active_shape_key.slider_min = -1 ##set key range_min
    obj.active_shape_key.value = -1 ##set key value
    obj.active_shape_key_index = 33 ##set active key
    obj.active_shape_key.value = 1 ##set key value
    obj.shape_key_add(name=str("Expression" + str(i)), from_mix=True) ##new shape from mix
    obj.active_shape_key_index = 33 ##delete active key
    bpy.ops.object.shape_key_remove()
    obj.active_shape_key_index = obj.data.shape_keys.key_blocks.keys().index("Armature")
    obj.active_shape_key.slider_min = 0 ##reset range
    bpy.ops.object.shape_key_clear()





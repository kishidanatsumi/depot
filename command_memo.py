#一些命令的备忘录

#现在的窗口
bpy.context.space_data
#物体计数
len(bpy.context.selectable_objects)

#当前选择物体
bpy.context.selected_objects

#全部可选物体
bpy.context.selectable_objects
#全部动画合集
bpy.data.actions
#打开视图显示：
bpy.context.object.data.show_names = True
bpy.context.object.data.display_type = 'STICK'

#形态键数值/登录关键帧
bpy.data.shape_keys['Key'].key_blocks["M_a"].value =1
bpy.data.shape_keys['Key'].key_blocks["M_a"].keyframe_insert(data_path="value",frame=100)

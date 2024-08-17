import json
import sys
import re

input_json = sys.argv[1]
if not re.search("\.json$",input_json):
    print ('Input is not json file')
    input()
    exit
else:
    input_name=input_json.replace(".json","")

    
#输入json记录表情的项，提取每项的帧
def takeSecond(elem):
    return elem["frame"]

#输入文件名转换到30帧
def to30(filename):
    #读取文件
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.readlines()

    #写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        recorder = []
        for i in data:
            a = i.split(',')
            #让帧数除于2就到30帧了
            frame = round(float(a[1])/2)
            #记录“表情名+帧数”到recorder, 防止因转30帧造成的重复
            if a[0]+str(frame) not in recorder:
                a[1] = str(frame)
                recorder.append(a[0]+str(frame))
            #如果发现重复，在其下一未占用帧加入表情
            else:
                count = 1
                while True:
                    if a[0]+str(frame+count) not in recorder:
                        a[1] = str(frame+count)
                        recorder.append(a[0]+str(frame+count))
                        break
                    else:
                        count += 1
            #整理好后，写入文件
            f.write(','.join(a))

#大概是加入csv的头尾格式，其实出来的文件虽然后缀是txt，但本质上是csv
def makefile(filename):
    #先根据文件名读取文件，a列表，一行一段
    with open(filename, 'r', encoding='utf-8') as f:
        a = f.readlines()

    f = open(filename, 'w', encoding='utf-8')
    #num表示一共有几行，接下来就是构造了
    num = len(a)
    f.write('version:,2\n')
    f.write('modelname:,justforfun\n')
    f.write('boneframe_ct:,0\n')
    f.write('morphframe_ct:,'+str(num)+'\n')
    f.write('morph_name,frame_num,value\n')
    for i in a:
        f.write(i)
    f.write('camframe_ct:,0\n')
    f.write('lightframe_ct:,0\n')
    f.write('shadowframe_ct:,0\n')
    f.write('ik/dispframe_ct:,0\n')
    #然后保存关闭
    f.close()

#这一步是压缩，可能同一个表情在同一个帧有记录多个数据，这时候就吧权重加起来
def compress(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        a = f.readlines()

    f = open(filename, 'w', encoding='utf-8')

    data = {}
    recorder = []
    former = ''

    for i in a:
        name = i.split(',')[0]
        if name not in recorder:
            recorder.append(name)
        
        temp = i.rsplit(',', 1)
        if temp[0] not in data:
            data[temp[0]] = float(temp[1])
        else:
            if data[temp[0]] != float(temp[1]):
                data[temp[0]] += float(temp[1])



    for i in data:
        f.write(i+','+str(data[i])+'\n')

    f.close()

#这里表示的是json上每个数字对应的表情
facial_dic = {1: 'あ', 2: 'い', 3: 'う', 4: 'え', 5: 'お', 6: 'にやり', 7: 'にやり', 8: 'ワ', 10: 'ワ'}
eye_l_dict = {10: 'ウィンク２', 11: 'ウィンク', 2: 'ウィンク', 3: 'ウィンク２'}
eye_r_dict = {10: 'ウィンク２右', 11: 'ウィンク右', 2: 'ウィンク右', 3: 'ウィンク２右'}

#打开文件
with open(input_json, 'r') as f:
    a = f.read()
b = json.loads(a)




motion_id = int(input("请输入要提取的表情编号(从1开始):"))

if motion_id == 1:
    dataset = b["facial1Set"]
else:
    dataset = b["other4FacialArray"][motion_id-2]    

#口型        
lipsync = dataset["mouthKeys"]["thisList"]
for i in range(len(lipsync)):
    lipsync[i]['vowel'] = lipsync[i]['mouthFlag']

#打开输出文件
output_file = input_name+"_"+str(motion_id)+".txt"
print(output_file)
f = open(output_file, 'w', encoding='utf-8')

#注释掉的是Json中Lipsync处的表情，结果不是很理想所以注释掉了，也许哪天兴致来了会处理

'''
mouthsync = b["ripSyncKeys"]["thisList"]
for i in range(len(mouthsync)):
    mouthsync[i]['vowel'] = mouthsync[i]['mouthFlag']
lipsync.extend(mouthsync)

lipsync.sort(key=takeSecond)

delete = []
for i in range(len(lipsync)-1):
    if lipsync[i]['frame'] == lipsync[i+1]['frame']:
        print(lipsync[i]['frame'])
    
        if 'mouthFlag' not in lipsync[i]:
            delete.append(i)
        else:
            delete.append(i+1)

for i in range(len(delete)):
    lipsync.pop(delete[i]-i)

'''

#眼部数据储存位置
eyesync = dataset["eyeKeys"]["thisList"]
recorder = {}

#开始对口型的处理，先分别读取每一项
for i in range(len(lipsync)):
    #第几帧
    frame = lipsync[i]["frame"]
    #权重到1的速度，通常为0和10，因为明显表情不可能在0帧之内从一个变到另一个，所以猜测要总体+1
    time = lipsync[i]["mouthSpeed"]+1
    #读取下一项的帧与速度，若没有下一项了，为-1
    if i != len(lipsync)-1 :
        next_frame = lipsync[i+1]["frame"]
        next_time = lipsync[i]["mouthSpeed"]+1
    else:
        next_frame = -1
        next_time = -1

    #如果有下一项（可以先跳到读取表情那边，知道recorder装的是什么再回来看这里）
    if next_frame != -1:
        print(recorder)
        #对于recoder中的每一项
        for j in recorder:
            #step表示下一帧与当前帧差多少
            step = next_frame-frame
            #当前帧权重到1要花的时间
            temp_time = time
            #如果说到下一帧花的时间比当前帧权重到1要花的时间小
            if step < temp_time:
                #直接在下一帧的地方把recoder记录的前一帧表情归0
                f.write(j+','+str(next_frame)+','+'0'+'\n')
            else:
                #否则在当前帧权重到1的地方将前一帧表情归0
                f.write(j+','+str(round(frame+time))+','+'0'+'\n')
    else:
        for j in recorder:
            f.write(j+','+str(round(frame+time))+','+'0'+'\n')
    #清空recorder
    recorder = {}

    #读取表情
    id = facial_dic[lipsync[i]["vowel"]]
    #默认权重为1
    wight = 1

    #记录表情，帧，权重为0（必须先定义为0）
    f.write(id+','+str(frame)+','+'0'+'\n')
    if next_frame != -1:
        #如果本项帧+花的时间小于下一项的帧
        if round(frame+time) < next_frame:
            #本项帧+花的时间处权重为1
            f.write(id+','+str(round(frame+time))+','+str(wight)+'\n')
            #到下一项的帧权重一直为1
            f.write(id+','+str(next_frame)+','+str(wight)+'\n')                    
        #如果不是的话
        else:
            #到下一项的帧此表情权重为1
            f.write(id+','+str(next_frame)+','+str(wight)+'\n')  
    else:
        f.write(id+','+str(round(frame+time))+','+str(wight)+'\n')
    #记录表情ID到recorder,因为此项表情目前并没有变为0，何时变为0要根据下一项的帧考虑
    recorder[id] = wight

#眼睛是相同逻辑的代码，不过多解释
for i in range(len(eyesync)):
    frame = eyesync[i]["frame"]
    time = eyesync[i]["eyeSpeed"]+1
    if i != len(eyesync)-1 :
        next_frame = eyesync[i+1]["frame"]
        next_time = eyesync[i+1]["eyeSpeed"]+1
    else:
        next_frame = -1
        next_time = -1

    if next_frame != -1:
        print(recorder)
        for j in recorder:
            step = next_frame-frame
            temp_time = time
            if step < temp_time:
                f.write(j+','+str(next_frame)+','+'0'+'\n')
            else:
                f.write(j+','+str(round(frame+time))+','+'0'+'\n')
    else:
        for j in recorder:
            f.write(j+','+str(round(frame+time))+','+'0'+'\n')
    recorder = {}

    eye_l = -1
    eye_r = -1
    eye_l_id = eyesync[i]["eyeLFlag"]
    eye_r_id = eyesync[i]["eyeRFlag"]
    if eye_l_id in eye_l_dict:
        eye_l = eye_l_dict[eye_l_id]
    if eye_r_id in eye_r_dict:
        eye_r = eye_r_dict[eye_r_id]    
    wight = 1

    if eye_l != -1:
        f.write(eye_l+','+str(frame)+','+'0'+'\n')
        if next_frame != -1:
            if round(frame+time) < next_frame:
                f.write(eye_l+','+str(round(frame+time))+','+str(wight)+'\n')
                f.write(eye_l+','+str(next_frame)+','+str(wight)+'\n')                    
            else:
                real_wight = wight
                f.write(eye_l+','+str(next_frame)+','+str(wight)+'\n')
        else:
            f.write(eye_l+','+str(round(frame+time))+','+str(wight)+'\n')
        recorder[eye_l] = wight

    if eye_r != -1:
        f.write(eye_r+','+str(frame)+','+'0'+'\n')
        if next_frame != -1:
            if round(frame+time) < next_frame:
                f.write(eye_r+','+str(round(frame+time))+','+str(wight)+'\n')
                f.write(eye_r+','+str(next_frame)+','+str(wight)+'\n')                    
            else:
                f.write(eye_r+','+str(next_frame)+','+str(wight)+'\n')  
        else:
            f.write(eye_r+','+str(round(frame+time))+','+str(wight)+'\n')
        recorder[eye_r] = wight

#保存关闭
f.close()
#先压缩，把重复的加起来
compress(output_file)
#转30帧
to30(output_file)
#转到那个工具可以变到vmd的形式
makefile(output_file)


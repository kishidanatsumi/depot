import json
import re
import sys

input_name = sys.argv[1]
input_file = input_name
output_file = input_name + '.txt'

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
        f.write(i+','+str(min(data[i], 1))+'\n')

    f.close()

#表情字典
facial_dic = {'Close': 'まばたき',
              'Closish': '笑い',
              'WinkL': 'ウィンク２'
              }

#打开文件
with open(input_file, 'r') as f:
    a = f.read()

#json转字典
b = json.loads(a)

#新建文件
f = open(input_name + '.txt', 'w', encoding='utf-8')

#开始处理口型
for i in b['m_Clips']:
    #接受相关信息
    start = round(i['m_Start']*30)
    duration = round(i['m_Duration']*30)
    easein = round(i['m_EaseInDuration']*30)
    easeout = round(i['m_EaseOutDuration']*30)
    if easein == 0:
        easein = 1
    if easeout == 0:
        easeout = 1

    #处理必要信息
    end = start + duration
    maxin = start + easein
    maxout = end - easeout
    

    #处理表情
    org_emotion = i['m_DisplayName'] 
    if org_emotion in facial_dic:
        emotion = facial_dic[i['m_DisplayName']]
    else:
        emotion = 'にやり'

    #将结论写入文件
    f.write(emotion+','+str(start)+','+str(0)+'\n')
    if maxin>=maxout:
        peaktime = round((duration/((1/easein)+(1/easeout)))*(1/easeout))
        if peaktime>=duration:
            peaktime = duration - 1
        elif peaktime == 0:
            peaktime = 1
        f.write(emotion+','+str(start+peaktime)+','+str((1/easein)*peaktime)+'\n')
    else: 
        f.write(emotion+','+str(maxin)+','+str(1)+'\n')
        f.write(emotion+','+str(maxout)+','+str(1)+'\n')
    f.write(emotion+','+str(end)+','+str(0)+'\n')
    
#保存关闭
f.close()
#先压缩，把重复的加起来
compress(output_file)
#转到那个工具可以变到vmd的形式
makefile(output_file)

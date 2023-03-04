#Prototype by LC_ilmlp
import json

def takeSecond(elem):
    return elem["frame"]

def cal(frame, next_frame, time, wight):
    real_wight = (next_frame - frame)/(time/5*3)*wight
    return real_wight

def to30(filename):
    with open(filename, 'r') as f:
        data = f.readlines()

    with open(filename, 'w') as f:    
        for i in data:
            a = i.split(',')
            a[1] = str(round(float(a[1])/2))
            f.write(','.join(a))

def makefile(filename):
    with open(filename, 'r') as f:
        a = f.readlines()

    f = open(filename, 'w', encoding='utf-8')

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
    f.close()


def compress(filename):
    with open(filename, 'r') as f:
        a = f.readlines()

    f = open(filename, 'w')

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

eye_changer = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:12, 14:21, 16:16, 17:18, 18:19, 19:20, 23:23, 28:28}

with open('son1001_Camera.json', 'r') as f:
    a = f.read()
b = json.loads(a)

f = open('all.txt', 'w')
#for lip

lipsync = b["ripSyncKeys"]["thisList"]
mouthsync = b["facial1Set"]["mouthKeys"]["thisList"]
lipsync.extend(mouthsync)


lipsync.sort(key=takeSecond)

delete = []
for i in range(len(lipsync)-1):
    if lipsync[i]['frame'] == lipsync[i+1]['frame']:
        print(lipsync[i]['frame'])
        '''
        if lipsync[i]["facialPartsDataArray"][0]["FacialPartsId"] == 0:
            delete.append(i)
        elif lipsync[i+1]["facialPartsDataArray"][0]["FacialPartsId"] == 0:
            delete.append(i+1)
        '''    
        if 'type' in lipsync[i]:
            delete.append(i)
        else:
            delete.append(i+1)

for i in range(len(delete)):
    lipsync.pop(delete[i]-i)            

used = []
record = []
base = False

for i in lipsync:
    print(i)
    frame = i["frame"]
    o_time = i["time"]
    if len(record) != 0:
        for each in record:
            f.write('Mouth_'+str(each[0])+','+str(frame)+','+str(each[1])+'\n')
            f.write('Mouth_'+str(each[0])+','+str(round(frame+(o_time/5*3)))+','+'0'+'\n')
        record = []
    for j in i["facialPartsDataArray"]:
        if 's_time' in j:
            time = j['s_time']
        else:
            time = o_time
        id = j["FacialPartsId"]
        wight = j["WeightPer"]*0.01
        if id != 0:
            base_trigger = False
            f.write('Mouth_'+str(id)+','+str(frame)+','+'0'+'\n')
            f.write('Mouth_'+str(id)+','+str(round(frame+(time/5*3)))+','+str(wight)+'\n')
            record.append([id,wight])
        else:
            base_trigger = True
            

    if base_trigger:
        base = True
        used = []
    else:
        base = False

#for eyes and eyebrows
        
temp_dic = {'Eye_':"eyeKeys", 'Ebrow_':'eyebrowKeys'}
for use in ('Eye_', 'Ebrow_'):
        
    eyesync = b["facial1Set"][temp_dic[use]]["thisList"]
            
    for point in ('L', 'R'):
        test = []    
        del_list = []
        recorder = {}
        used = []
        base = False

        for i in range(len(eyesync)):
            #print(i)
            frame = eyesync[i]["frame"]
            time = eyesync[i]["time"]
            if i != len(eyesync)-1 :
                next_frame = eyesync[i+1]["frame"]
                next_time = eyesync[i+1]["time"]
            else:
                next_frame = -1
                next_time = -1
            
            
            
            if next_frame != -1:
                for j in recorder:
                    step = next_frame-frame
                    temp_time = time/5*3
                    if step < temp_time:
                        f.write(j+','+str(next_frame)+','+'0'+'\n')
                    else:
                        f.write(j+','+str(round(frame+(time/5*3)))+','+'0'+'\n')
            else:
                for j in recorder:
                    f.write(j+','+str(round(frame+(time/5*3)))+','+'0'+'\n')
                recorder = {}
                    

            for j in eyesync[i]["facialPartsDataArray"+point]:
                id = j["FacialPartsId"]
                wight = j["WeightPer"]*0.01
                if id != 0:
                    if id not in test:
                        test.append(id)
                    if use == 'Eye_':
                        id = str(eye_changer[id])
                    else:
                        id = str(id)
                    base_trigger = False
                    f.write(use+id+'_'+point+','+str(frame)+','+'0'+'\n')
                    if next_frame != -1:
                        if round(frame+(time/5*3)) < next_frame:
                            real_wight = wight
                            f.write(use+id+'_'+point+','+str(round(frame+(time/5*3)))+','+str(real_wight)+'\n')
                            f.write(use+id+'_'+point+','+str(next_frame)+','+str(real_wight)+'\n')                    
                        else:
                            real_wight = wight
                            f.write(use+id+'_'+point+','+str(next_frame)+','+str(real_wight)+'\n')
                        if real_wight != 0:
                            recorder[use+id+'_'+point] = real_wight   
                    else:
                        f.write(use+id+'_'+point+','+str(round(frame+(time/5*3)))+','+str(wight)+'\n')
                        recorder[use+id+'_'+point] = wight
                else:
                    base_trigger = True
                    

            if base_trigger:
                base = True
                used = []
            else:
                base = False

compress('all.txt')
print ("txt made")
#input()
to30('all.txt')
print ("txt to 30")
makefile('all.txt')
print ("txt output")
input()

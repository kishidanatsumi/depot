import os
import re
#快速文件替换重命名
name="^.* - "
def file_rename():
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    for file in files:
        if re.search(name,file):
            ret=re.search(name,file)
            new_filename = file.replace(str(ret.group()),"")
            print(file,"has been renamed to",new_filename)
            #os.rename(file, new_filename)
            
file_rename()

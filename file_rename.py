import os
#快速文件替换/重命名

def file_rename():
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    for file in files:
        if '[1]' in file:
            new_filename = file.replace('[1]', '')
            os.rename(file, new_filename)
            
file_rename()
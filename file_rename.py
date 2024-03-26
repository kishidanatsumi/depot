import os
#快速文件替换/重命名
name="foo"
def file_rename():
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    for file in files:
        if name in file:
            new_filename = file.replace(name, '')
            os.rename(file, new_filename)
            
file_rename()

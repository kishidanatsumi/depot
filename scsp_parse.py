import sys
import os
import re


input_path=os.listdir("./")
print(input_path)
for input_file in input_path:
    if ( os.path.isfile(input_file)  ):
        output_file="out_"+input_file+".unity3d"
        with open(input_file,'rb') as f:
            if ( f.read(4) == b'\xba\x01\x00\x00'):
                print("Read:",input_file)
                f.seek(0)
                data=f.read()[4:]
                f.close()
                with open(output_file,'w+b') as o:
                    o.write(data)
                    o.close()
            else:
                print(input_file,"not match")
                f.close()
                next
    else:
        print(input_file,"is not a file")
        next


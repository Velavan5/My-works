import os

def movefileTo_folder(cur_path,file_name):
    fol_name=file_name.split(".")[-1]+"_Files"
    os.chdir(cur_path)
    if not os.path.exists(fol_name):
        os.mkdir(fol_name)
    os.rename(file_name,fol_name+r"/"+file_name)
    print(f"## successfully added file name {file_name} to dir {fol_name}")
        
        
        
# User section
path=input("Enter the path of the folder here : ")
if os.path.isfile(path):
    exit("You cann't give a file\n")
elif not os.path.exists(path):
    exit("Invaild path or Path doesn't exists\nerror code:453545\n")
    
#taking each file
count=0
for file in os.listdir(path):
    loc=os.path.join(path,file)
    if not os.path.isdir(loc):
        movefileTo_folder(path,file)
        count+=1

print(f"{count} Files have been moved")

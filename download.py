import datetime
import requests
import shutil
from pathlib import Path
from zipfile import ZipFile, ZipInfo
import os, re
import traceback

def download(start, end, loc):
    months = []
    for i in range(1,13):
        months.append((datetime.datetime.strptime(str(i), '%m')).strftime('%b').lower())
    # print(months)
    for i in range(start, end+1):
        for j in months:
            url = "https://www1.nseindia.com/content/indices/mcwb_"+str(j)+str(i)+".zip"
            try:
                r = requests.get(url, stream=True)
                filename = url.split('/')[-1] # this will take only -1 splitted part of the url(ie. filename)
                with open(loc+'/'+filename,'wb') as output_file:
                    output_file.write(r.content)
    
            except Exception as err:
                traceback.print_tb(err.__traceback__)
                continue
    print('Download Completed!!!')

def extract(start, end, loc):
    download(start, end, loc)
    folderpath = loc
    filepaths  = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    
    for path in filepaths:
        try:
            with ZipFile(path, 'r') as zipObj:
                listOfFileNames = zipObj.namelist()
                for fileName in listOfFileNames:
                    if re.search(r"(^nifty50)|(^niftymcwb)|([A-Za-z0-9]\/nifty50)|([A-Za-z0-9]\/niftymcwb)", fileName, flags=re.IGNORECASE):
                        if r"/" in fileName :
                            zipObj.extract(fileName, 'extracted')
                        else:
                            final_path = path.split('\\')[-1]
                            zipObj.extract(fileName, 'extracted\\'+ final_path)
                    else:
                        continue
            os.remove(path)
        except Exception as err:
            # traceback.print_tb(err.__traceback__)
            continue
        
def move_files():
    curr_dir = os.getcwd()
    src_dir = curr_dir+'\extracted'
    os.listdir()
    dest_dir = r'.\csv_files'

    for root, dirs, files in os.walk((os.path.normpath(src_dir)), topdown=False):
        f = root.split("\\")[-1]
        f1 = f.split('_')[-1]
        filename = f1[0:5]

        for name in files:
            if name.endswith('.csv'):
                os.rename((os.path.join(root, name)), os.path.join(root, filename+'.csv'))
                # print ("Found")
                SourceFolder = os.path.join(root,filename+'.csv')
                shutil.copy2(SourceFolder, dest_dir) #copies csv to new folder

if __name__ == "__main__":
    print("Input start, end year and location where u want to download ")
    s_year = input()
    e_year = input()
    path = input()
    extract(s_year, e_year, path)
    move_files()
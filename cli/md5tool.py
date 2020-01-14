#!/usr/bin/env python3
# 
# Command line script to generate a file that contains the 
# MD5 hash of all the files in a subdirectory.
# 
# https://github.com/Smithsonian/MD5_tool/
# 
# 23 Dec 2019
# 
# Digitization Program Office, 
# Office of the Chief Information Officer,
# Smithsonian Institution
# https://dpo.si.edu
#
#Import modules
import urllib.request
from time import localtime, strftime
import hashlib, locale, sys, logging, os, glob
from functools import partial
from tqdm import tqdm
from pyfiglet import Figlet
from pathlib import Path



#Script variables
script_title = "MD5 Tool"
subtitle = "Digitization Program Office\nOffice of the Chief Information Officer\nSmithsonian Institution\nhttps://dpo.si.edu"
ver = "0.1.2"
vercheck = "https://raw.githubusercontent.com/Smithsonian/MD5_tool/master/md5toolversion.txt"
repo = "https://github.com/Smithsonian/MD5_tool/"
lic = "Available under the Apache 2.0 License"


# Set locale to UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#Get current time
current_time = strftime("%Y%m%d_%H%M%S", localtime())


#Check for updates to the script
with urllib.request.urlopen(vercheck) as response:
   current_ver = response.read()

cur_ver = current_ver.decode('ascii').replace('\n','')
if cur_ver != ver:
    msg_text = "{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}\nThis version is outdated. Current version is {cur_ver}.\nPlease download the updated version at: {repo}"
else:
    msg_text = "{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}"




#Info window
f = Figlet(font='slant')
print("\n")
print (f.renderText(script_title))
print(msg_text.format(subtitle = subtitle, ver = ver, repo = repo, lic = lic, cur_ver = cur_ver))


folder_md5 = sys.argv[1]
hash_format = 'md5 filename'



def md5sum(filepath, filename):
    #https://stackoverflow.com/a/7829658
    with open("{}/{}".format(filepath, filename), mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return d.hexdigest()



def write_hash(directory, filename, file_md5hash, hash_format, current_time):
    file_path = os.path.join(directory, filename)
    basename = os.path.basename(os.path.dirname(file_path))
    md5_file = "{}/{}_{}.md5".format(directory, basename, current_time)
    md5f = open(md5_file, 'a')
    if hash_format == 'md5 filename':
        md5hash_formatted = "{} {}\n".format(file_md5hash, filename)
    elif hash_format == 'md5,filename':
        md5hash_formatted = "{},{}\n".format(file_md5hash, filename)
    elif hash_format == 'filename md5':
        md5hash_formatted = "{} {}\n".format(filename, file_md5hash)
    elif hash_format == 'filename,md5':
        md5hash_formatted = "{},{}\n".format(filename, file_md5hash)
    md5f.write(md5hash_formatted)
    md5f.close()
    return True


files = glob.glob("{}/*".format(folder_md5))
for file in tqdm(files):
    filename = Path(file).name
    file_md5hash = md5sum(folder_md5, filename)
    write_hash(folder_md5, filename, file_md5hash, hash_format, current_time)
    


sys.exit(0)

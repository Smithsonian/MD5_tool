#!/usr/bin/env python3
# 
# Command line script to generate a file that contains the 
# MD5 hash of all the files in a subdirectory.
# Works in parallel.
# 
# https://github.com/Smithsonian/MD5_tool/
# 
# 19 Sep 2022
# 
# Digitization Program Office, 
# Office of the Chief Information Officer,
# Smithsonian Institution
# https://dpo.si.edu
#
# Import modules
# import urllib.request
import hashlib
import locale
import sys
import os
import glob
from functools import partial
from pyfiglet import Figlet
from pathlib import Path
from time import localtime, strftime

# Parallel
from multiprocessing import Pool
from tqdm.auto import tqdm
from p_tqdm import p_map


# Script variables
script_title = "MD5 Tool - Parallel"
subtitle = "Digitization Program Office\nOffice of the Chief Information Officer\nSmithsonian Institution\nhttps://dpo.si.edu"
ver = "0.2.0"
#vercheck = "https://raw.githubusercontent.com/Smithsonian/MD5_tool/master/md5toolversion.txt"
repo = "https://github.com/Smithsonian/MD5_tool/"
lic = "Available under the Apache 2.0 License"

# Set locale to UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# Get current time
current_time = strftime("%Y%m%d_%H%M%S", localtime())

# Check for updates to the script
# with urllib.request.urlopen(vercheck) as response:
#     current_ver = response.read()
#
# cur_ver = current_ver.decode('ascii').replace('\n', '')
# if cur_ver != ver:
#     msg_text = "{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}\nThis version is outdated. Current version is {cur_ver}.\nPlease download the updated version at: {repo}"
# else:
#     msg_text = "{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}"

msg_text = "{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}"

# Info window
f = Figlet(font='slant')
print("\n")
print(f.renderText(script_title))
print(msg_text.format(subtitle=subtitle, ver=ver, repo=repo, lic=lic))

folder_md5 = sys.argv[1]
no_workers = sys.argv[2]

# Get current time
current_time = strftime("%Y%m%d_%H%M%S", localtime())


def md5sum(filename):
    # https://stackoverflow.com/a/7829658
    with open("{}".format(filename), mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return "{} {}".format(d.hexdigest(), os.path.basename(filename))


files = glob.glob("{}/*".format(folder_md5))

if len(glob.glob("{}/*.md5".format(folder_md5))) > 0:
    print("md5 file exists, exiting.")
    sys.exit(9)
else:
    results = p_map(md5sum, files, **{"num_cpus": int(no_workers)})
    with open("{}/{}_{}.md5".format(folder_md5, os.path.basename(os.path.dirname(folder_md5)), current_time), 'w') as fp:
        fp.write('\n'.join(results))


sys.exit(0)

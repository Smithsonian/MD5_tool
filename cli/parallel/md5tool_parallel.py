#!/usr/bin/env python3
#
# Command line script to generate a file that contains the
# MD5 hash of all the files in a subdirectory.
# Works in parallel.
#
# https://github.com/Smithsonian/MD5_tool/
#
# 14 Mar 2023
#
#  - New:
#       * Automatically runs in all subfolders that have files
#       * If no_workers is not given, set to (number of cores - 1)
#
# Digitization Program Office,
# Office of the Chief Information Officer,
# Smithsonian Institution
# https://dpo.si.edu
#
# Import modules
import hashlib
import locale
import sys
import os
import glob
from functools import partial
import subprocess

# from pathlib import Path
from time import localtime, strftime


def check_package(package):
    try:
        __import__(package)
    except ImportError:
        p = subprocess.run(['python3', '-m', 'pip', 'install', '--user', '--upgrade', 'pip'])
        p = subprocess.run(['python3', '-m', 'pip', 'install', '--user', package])


check_package('pyfiglet')
check_package('p_tqdm')


from pyfiglet import Figlet

# Parallel
import multiprocessing
from p_tqdm import p_map


# Script variables
script_title = "MD5 Tool - Parallel"
subtitle = "Digitization Program Office\nOffice of the Chief Information Officer\nSmithsonian Institution\nhttps://dpo.si.edu"
ver = "0.3.0"
repo = "https://github.com/Smithsonian/MD5_tool/"
lic = "Available under the Apache 2.0 License"

# Set locale to UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# Get current time
current_time = strftime("%Y%m%d_%H%M%S", localtime())

msg_text = "{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}"

# Info window
f = Figlet(font='slant')
print("\n")
print(f.renderText(script_title))
print(msg_text.format(subtitle=subtitle, ver=ver, repo=repo, lic=lic))


if len(sys.argv) == 3:
    folder_md5 = sys.argv[1]
    no_workers = int(sys.argv[2])
    if multiprocessing.cpu_count() < no_workers:
        no_workers = (multiprocessing.cpu_count()) - 1
elif len(sys.argv) == 2:
    folder_md5 = sys.argv[1]
    no_workers = (multiprocessing.cpu_count()) - 1
else:
    sys.exit("Missing folder and/or no_workers arguments.\n Usage: ./md5toolparallel.py [FOLDER] [NO_WORKERS]")


# Get current time
current_time = strftime("%Y%m%d_%H%M%S", localtime())


def md5sum(filename):
    # https://stackoverflow.com/a/7829658
    with open("{}".format(filename), mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    return "{} {}".format(d.hexdigest(), os.path.basename(filename))


for root, dirs, files_indir in os.walk(folder_md5):
    for folder_check in dirs:
        print("\n Running on folder {} using {} workers".format(folder_check, no_workers))
        if len(glob.glob("{}/{}/*.md5".format(root, folder_check))) > 0:
            print("\n   md5 file exists, skipping...")
            continue
        files = glob.glob("{}/{}/*".format(root, folder_check))
        if len(files) > 0:
            results = p_map(md5sum, files, **{"num_cpus": int(no_workers)})
            with open("{}/{}/{}_{}.md5".format(root, folder_check, folder_check, current_time),
                      'w') as fp:
                fp.write('\n'.join(results))


sys.exit(0)

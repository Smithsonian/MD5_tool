#!/usr/bin/env python3
#
# Verify MD5 hashes in file
#
# 31 Aug 2023
# 
# Digitization Program Office, 
# Office of the Chief Information Officer,
# Smithsonian Institution
# https://dpo.si.edu
#

import glob
import hashlib
import locale
import os
import sys
from pathlib import Path
from time import localtime, strftime

import pandas as pd
from pyfiglet import Figlet
from tqdm import tqdm

# Script variables
script_title = "Verify MD5 Tool"
subtitle = "Digitization Program Office\nOffice of the Chief Information Officer\nSmithsonian Institution\nhttps://dpo.si.edu"
ver = "0.2.0"
repo = "https://github.com/Smithsonian/MD5_tool/"
lic = "Available under the Apache 2.0 License"

# Set locale to UTF-8
locale.setlocale(locale.LC_ALL, 'en_US.utf8')

# Get current time
current_time = strftime("%Y%m%d_%H%M%S", localtime())

# Check args
if len(sys.argv) == 1:
    sys.exit("Missing path")

if len(sys.argv) > 2:
    sys.exit("Script takes a single argument")

# Check for updates to the script
msg_text = "{subtitle}\n\n{repo}\n{lic}\n\nver. {ver}"
cur_ver = ver

fig = Figlet(font='slant')
print("\n")
print(fig.renderText(script_title))
# print(script_title)
print(msg_text.format(subtitle=subtitle, ver=ver, repo=repo, lic=lic, cur_ver=cur_ver))

folder_to_check = sys.argv[1]


# Compare hashes between files and what the md5 file says
def check_md5(md5_file, files):
    bad_files = pd.DataFrame(data=None, columns=['filename', 'file_md5', 'md5_from_file'])
    for file in tqdm(files):
        filename = Path(file).name
        md5_hash = hashlib.md5()
        with open(file, "rb") as f:
            # Read and update hash in chunks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        file_md5 = md5_hash.hexdigest()
        md5_from_file = md5_file[md5_file.file == filename]['md5'].to_string(index=False).strip()
        if file_md5 == md5_from_file:
            continue
        elif md5_from_file == 'Series([], )':
            bad_files = bad_files.append({'filename': filename, 'file_md5': file_md5, 'md5_from_file': 'NA'},
                                         ignore_index=True)
        else:
            bad_files = bad_files.append({'filename': filename, 'file_md5': file_md5, 'md5_from_file': md5_from_file},
                                         ignore_index=True)
    if len(bad_files) > 0:
        return 1, bad_files
    else:
        return 0, None


def main():
    print("\nWorking...\n")
    if not os.path.isdir(folder_to_check):
        print("Path not found: {}".format(folder_to_check))
        sys.exit(1)
    md5_file = glob.glob("{}/*.md5".format(folder_to_check))
    if len(md5_file) == 0:
        exit_msg = "ERROR: .md5 file not found"
        print(exit_msg)
        sys.exit(1)
    if len(md5_file) > 1:
        exit_msg = "ERROR: Multiple .md5 files found"
        print(exit_msg)
        sys.exit(2)
    else:
        # Read md5 file
        md5_file = pd.read_csv(md5_file[0], sep=' ', header=None, names=['md5', 'file'])
    # Get list of files
    files = glob.glob("{}/*".format(folder_to_check))
    # Exclude md5 file
    files = [x for x in files if '.md5' not in x]
    # Compare list of files with length of md5 file
    if len(files) != md5_file.shape[0]:
        print("\n\n ERROR: The number of files ({}) does not match the number of lines in the md5 file ({})\n\n".format(
            len(files), md5_file.shape[0]))
        sys.exit(1)
    # Check if hashes match
    res, results = check_md5(md5_file, files)
    error_filename = "md5_report_{}.csv".format(current_time)
    if res == 0:
        exit_msg = "\n\nSUCCESS: Files match md5\n\n"
        print(exit_msg)
    else:
        exit_msg = "\n\nERROR: {} files do not match md5. Report in file {}\n\n".format(results.shape[0], error_filename)
        print(exit_msg)
        results.to_csv(error_filename, index=False, encoding="UTF-8", mode="w")
        sys.exit(1)


if __name__ == "__main__":
    main()


sys.exit(0)

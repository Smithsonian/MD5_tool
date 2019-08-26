#!/usr/bin/env python3
# 
# Script to generate a file that contains the MD5 hash of all
# the files in each subdirectory.
# 
# https://github.com/Smithsonian/MD5_tool/
# 
# 26 Aug 2019
# 
# Digitization Program Office, 
# Office of the Chief Information Officer,
# Smithsonian Institution
# https://dpo.si.edu
#
#Import modules
import urllib.request
import PySimpleGUI as sg
from time import localtime, strftime
import hashlib, locale, sys, logging, os, glob
from functools import partial
import webbrowser
from dpologo import dpologo


#Script variables
script_title = "DPO MD5 Tool"
subtitle = "Digitization Program Office\nOffice of the Chief Information Officer\nSmithsonian Institution\nhttps://dpo.si.edu"
ver = "0.1.1"
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
    msg_text = "{script_title}\n\n{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}\nThis version is outdated. Current version is {cur_ver}.\nPlease download the updated version at: {repo}"
else:
    msg_text = "{script_title}\n\n{subtitle}\n\n{repo}\n\n{lic}\n\nver. {ver}"




#GUI info window
github_text = "Go to Github"
layout = [
            [sg.Image(data = dpologo)],
            [sg.Text(msg_text.format(script_title = script_title, subtitle = subtitle, ver = ver, repo = repo, lic = lic, cur_ver = cur_ver))],
            [sg.Submit("OK"), sg.Cancel(github_text)]]
window = sg.Window("Info", layout)
event, values = window.Read()
window.Close()

# Open browser to Github repo if user clicked the "Go to Github" button
if event == github_text:
    webbrowser.open_new_tab(repo)
    raise SystemExit("Cancelling: going to repo")

if event == None:
    #User closed window, leave program
    raise SystemExit("Leaving program")


#Ask for the top folder
layout = [[sg.Text('Select the top folder to generate the MD5 files')],
         [sg.InputText(), sg.FolderBrowse()],
         [sg.Checkbox('Save log to file', default = False)],
         [sg.Submit(), sg.Cancel()]]

window = sg.Window('Select folder', layout)
event, values = window.Read()
window.Close()

#User clicked cancel, exit program
if event == 'Cancel':
    raise SystemExit("User pressed Cancel")


folder_to_browse = values[0]
save_to_log = values[1]

if save_to_log:
    # Logging
    logfile_name = '{}.log'.format(current_time)
    # from http://stackoverflow.com/a/9321890
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=logfile_name,
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger1 = logging.getLogger("md5tool")
    logger1.info("folder_to_browse: {}".format(folder_to_browse))



#Excluded extensions
layout = [[sg.Text('OPTIONAL: Enter file extensions to skip (e.g.: \'xml\' or \'tmp\'), separated by commas. Leave empty to list all files.')],
                 [sg.InputText("tmp,md5")],
                 [sg.Submit()]]
window = sg.Window('File extensions to skip', layout)
event, values = window.Read()
window.Close()

extensions_to_skip = values[0].replace(" ", "")
if save_to_log:
    logger1.info("extensions_to_skip: {}".format(extensions_to_skip))




#Select output format
layout = [[sg.Text('Select the format of the MD5 file:')], [sg.Listbox(values=('md5 filename', 'md5,filename', 'filename md5', 'filename,md5'), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=(30,4), default_values = 'md5 filename')], [sg.OK()]]
window = sg.Window('Select the output format', layout)
event, values = window.Read()
window.Close()
hash_format = values[0][0]
if save_to_log:
    logger1.info("hash_format: {}".format(hash_format))



def md5sum(filepath, filename):
    #https://stackoverflow.com/a/7829658
    with open("{}/{}".format(filepath, filename), mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    if save_to_log:
        logger1.info("filename md5: {}/{} {}".format(filepath, filename, d.hexdigest()))
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
    if save_to_log:
        logger1.info("md5_file: {}".format(md5_file))
    return True



layout = [[sg.Text('Working...')], [sg.Quit(button_color=('black', 'orange'))]]
window = sg.Window('Generating files', layout, auto_size_text=True)



res = ""

# This is the code that reads and updates your window      
event, values = window.Read(timeout=1)      
# Recursively browse the directories
for root, dirs, files in os.walk(folder_to_browse):
    #logger1.info("Running on folder {}".format(root))
    for file in files:
        if event is not None:
            ext = os.path.splitext(file)[-1].lower()[1:]
            if ext not in extensions_to_skip:
                file_md5hash = md5sum(root, file)
                if save_to_log:
                    logger1.info("Getting MD5 hash for file file {}/{}".format(root, file))
                write_hash(root, file, file_md5hash, hash_format, current_time)
                res = res + root + "/" + file + " with MD5 hash: " + file_md5hash + "\n"
        if event == 'Quit'  or values is None:
            break





#GUI info window
sg.PopupScrolled(res, title = 'Done!', size=(100, 20))

sys.exit(0)

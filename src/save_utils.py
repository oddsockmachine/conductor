from glob import glob
from re import fullmatch
from constants import logging, save_location, save_extension
from json import load, dump

def get_next_filename():
    files = glob(save_location+'*'+save_extension)
    # print(files)
    files = [f for f in files if fullmatch(save_location+'\d+\.json', f)]
    files = [f.replace(save_location,'').replace(save_extension,'') for f in files if fullmatch(save_location+'\d+'+save_extension, f)]
    files = sorted([int(f) for f in files])
    # print(files)
    next_num = 0
    for num in files:
        if int(num)+1 not in files:
            next_num = int(num)+1
            break
    next_file = save_location + str(next_num) + save_extension
    # print(next_file)
    return next_file

def get_all_set_file_numbers():
    files = glob(save_location+'*'+save_extension)
    # print(files)
    files = [f for f in files if fullmatch(save_location+'\d+\.json', f)]
    files = [f.replace(save_location,'').replace(save_extension,'') for f in files if fullmatch(save_location+'\d+'+save_extension, f)]
    files = sorted([int(f) for f in files])
    return files

ALL_FILE_NAMES = get_all_set_file_numbers()
# logging.info(str(ALL_FILE_NAMES))

def filenum_from_touch(x, y):
    num = str(255 - (y * 16 + (15 - x)))
    # filenum = save_location + num + save_extension
    return num

def validate_filenum(num):
    return int(num) in ALL_FILE_NAMES

def load_filenum(filenum):
    filename = save_location + filenum + save_extension
    with open(filename, 'r') as saved_file:
        saved_data = load(saved_file)
    return saved_data

def save_filenum(data, filenum=None):
    if not filenum:
        filename = get_next_filename()
    else:
        filename = save_location + filenum + save_extension
    with open(filename, 'w') as savefile:
        dump(data, savefile)
    return

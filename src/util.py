from glob import glob
from re import fullmatch
from constants import logging, save_location, save_extension
from json import load

def get_next_filename(saved_location, extension):
    files = glob(saved_location+'*'+extension)
    # print(files)
    files = [f for f in files if fullmatch(saved_location+'\d+\.json', f)]
    files = [f.replace(saved_location,'').replace(extension,'') for f in files if fullmatch(saved_location+'\d+'+extension, f)]
    files = sorted([int(f) for f in files])
    # print(files)
    next_num = 0
    for num in files:
        if int(num)+1 not in files:
            next_num = int(num)+1
            break
    next_file = saved_location + str(next_num) + extension
    # print(next_file)
    return next_file

def get_all_set_file_numbers(saved_location, extension):
    files = glob(saved_location+'*'+extension)
    # print(files)
    files = [f for f in files if fullmatch(saved_location+'\d+\.json', f)]
    files = [f.replace(saved_location,'').replace(extension,'') for f in files if fullmatch(saved_location+'\d+'+extension, f)]
    files = sorted([int(f) for f in files])
    return files


def load_from_touch(x, y):
    num = str(255 - (y * 16 + (15 - x)))
    # logging.info("touched ", num)
    filename = save_location + num + save_extension
    # logging.info("opening ", filename)
    with open(filename, 'r') as saved_file:
        saved_data = load(saved_file)
    return saved_data

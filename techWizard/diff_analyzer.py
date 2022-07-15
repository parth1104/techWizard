#!/usr/bin/env python
# coding: utf-8

import os
from diff_browser import get_diff_patch


# extensions          = ['.c', '.h', '.make']
# extension2changes = {'.c':{}, '.h':{}, '.make':{}}


extension2changes ={}
extension2numchanges ={}
status2numchanges ={}

def init_dicts(ext_list):
    global extension2changes
    global extension2numchanges
    global status2numchanges
    for ext in ext_list:
        extension2changes[ext]      = {'a':[],'m':[],'r':[]}
        extension2numchanges[ext]   = {'a':[],'m':[],'r':[]}
    status2numchanges ={'a':0,'m':0,'r':0}

def find_funcs(diff,file1_name,file2_name):
    func_list = []
    lines = diff.split('\n')
    for line in lines:
        if '#define' in line:
            continue
        elif '(' not in line:
            continue
        else:
            func_list.append((line.split('(')[0].strip().split(' ')[-1], line[0], file1_name, file2_name))
    return func_list


def analyze_diff(complete_path1,complete_path2):
    global extension2changes
    global extension2numchanges
    global status2numchanges

    changes_str = get_diff_patch(complete_path1,complete_path2,"-qrbBX excludefiles.txt")

    changes = changes_str.split('\n')

    for change in changes:
        if 'differ' in change:
            status = 'm'
        elif complete_path2 in change:
            status = 'a'
        else:
            status = 'r'
        status2numchanges[status] += 1

        for ext in extension2changes:
            if ext in change:
                extension2changes[ext][status].append(change)
                break
    for ext in extension2changes:
        for status in extension2changes[ext]:
            extension2numchanges[ext][status] = len(extension2changes[ext][status])



def get_stats(complete_path1,complete_path2,ext_list):
    global extension2changes
    global extension2numchanges
    global status2numchanges

    init_dicts(ext_list)
    
    analyze_diff(complete_path1,complete_path2)

    # function change list from header files:
    func_list = []
    for status in extension2changes['.h']:
        for change in extension2changes['.h'][status]:
            words = change.split(' ')
            file1_name = ''
            file2_name = ''
            if 'differ' in change:
                file1_name = words[1]
                file2_name = words[3]

            if 'Only' in change:
                if VERSION2 in change:
                    file1_name = 'dummy_file'
                    file2_name = words[-2].strip(':') + '/' + words[-1]
                else:
                    file1_name = words[-2].strip(':') + '/' + words[-1]
                    file2_name = 'dummy_file'
            
            file_diff_patch = get_diff_patch(file1_name,file2_name,"-bBN")
            func_list.extend(find_funcs(file_diff_patch,file1_name,file2_name))
    
    return status2numchanges, extension2numchanges, func_list

    


### ============================================================================================ ###

if __name__ == "__main__":
    # MAIN STARTS HERE
    SOC="j721e"
    OS="linux"
    VERSION1="08_01_00_07"
    VERSION2="08_02_00_03"
    # OS="rtos"
    # VERSION1="08_01_00_13"
    # VERSION2="08_02_00_05"

    base_path = '/home/tanmay/inspire/sdk/'
    SDK1_PATH = base_path + SOC + '/'+ OS + '/' + VERSION1
    SDK2_PATH = base_path + SOC + '/'+ OS + '/' + VERSION2

    relative_path = '/board-support/k3-respart-tool'
    # relative_path = ''
    # relative_path += '/' + 'vision_apps'
    # relative_path += '/' + 'platform'
    # relative_path += '/' + 'apps/basic_demos/app_multi_cam/main.c'
    my_type = 'd'
    # my_type = 'f'

    complete_path1 = SDK1_PATH + relative_path
    complete_path2 = SDK2_PATH + relative_path
    extensions  = ['.c', '.h', '.make', '.Makefile', '.makefile', '.mk', '.mak', '.Mk', '.cfg', '.lds']
    # extensions  = ['.h']

    status2numchanges, extension2numchanges_t, func_list = get_stats(complete_path1,complete_path2,extensions)

    print(status2numchanges)
    print(extension2numchanges_t)
    print(len(func_list))

        # if change in adds or change in subtracts:
        #     do_domething

### ============================================================================================ ###

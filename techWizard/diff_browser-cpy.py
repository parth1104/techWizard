#!/usr/bin/env python
# coding: utf-8

import sys
import os
from diff_analyzer import *


# versioned_components = {'rtos':['pdk_jacinto'],'linux':['linux','u-boot']}
versioned_components = ['pdk_jacinto', 'pdk_j7200', 'linux', 'u-boot', 'cg_xml', 'dsplib_c66', 'mathlib_c66', 'mmalib', 'ti-cgt-armllvm', 'ti-cgt-c6000', 'ti-cgt-c7000', 'tidl_j7', 'uia', 'xdais', 'k3-image-gen']
g_back_map = [{},{}]

def short_dir_names(real_list,idx):
    global g_back_map
    new_list = []
    for real_item in real_list:
        changed=False
        for short_item in versioned_components:
            if short_item in real_item:
                new_list.append(short_item)
                g_back_map[idx][short_item] = real_item
                changed=True
                break
        if not changed:
            new_list.append(real_item)
    return new_list


# inputs:
#     path1     if exists, must be directory
#     path2     if exists, must be directory
# outputs:
#     characterized union of contents with change status : 'r' 'a' 'm' 'u'
def browse_diff_dir(path1,path2,relative_path):
    lst1,lst2 = [],[]
    if (os.path.exists(path1)):
        lst1 = sorted(os.listdir(path1))
    if (os.path.exists(path2)):
        lst2 = sorted(os.listdir(path2))

    lst1 = short_dir_names(lst1,0)
    lst2 = short_dir_names(lst2,1)

    union_list = sorted(list(set(lst1) | set(lst2)))
    intersection_list = sorted(list(set(lst1) & set(lst2)))
    lst1 = [item for item in lst1 if item not in intersection_list]
    lst2 = [item for item in lst2 if item not in intersection_list]

    diff_map = []

    changes_str = get_diff_patch(path1,path2,"-qrbBX excludefiles.txt")
    changes = changes_str.split('\n')
    print(len(changes))

    for item in union_list:
        if item.startswith('.') :
            continue
        if item in versioned_components:
            complete_path1 = path1 + '/' + g_back_map[0][item]
            complete_path2 = path2 + '/' + g_back_map[1][item]
            changes_str += '\n' + get_diff_patch(complete_path1,complete_path2,"-qrbBX excludefiles.txt")
        else:
            complete_path1 = path1 + '/' + item
            complete_path2 = path2 + '/' + item
        item_relative_path = relative_path + '/' + item

        itemtype = ''
        if os.path.isdir(complete_path1) or os.path.isdir(complete_path2):
            itemtype = 'd'
        elif os.path.isfile(complete_path1) or os.path.isfile(complete_path2):
            itemtype = 'f'

        if item in lst1:
            status = '#b42626'

        if item in lst2:
            status = '#259f31'

        if item in intersection_list:
            if item in changes_str:
                status = '#5d35d4'
            else:
                status = '#1f1f1f'

        diff_map.append((item, itemtype , status, complete_path1, complete_path2, item_relative_path))

    changes = changes_str.split('\n')
    print(len(changes))

    return diff_map

#
# inputs:
#     path1     if exists, must be a file
#     path2     if exists, must be a file
# outputs:
#     string that has the diff content
def get_diff_patch(path1,path2, opt = ''):
    command = "diff " + opt + " " + path1 + " " + path2
    return os.popen(command).read()

def get_gitdiff_patch(path1,path2, opt = ''):
    command = "git diff " + opt + " " + path1 + " " + path2
    return os.popen(command).read()



def browse_diff(complete_path1, complete_path2 ,relative_path, my_type):
    while True:
        print("\nYou are at: ." + relative_path)
        if my_type == 'd':
            diff_map = browse_diff_dir(complete_path1, complete_path2, relative_path)
            for item in diff_map:
                print(str(item))

            goto = input("\ngo to: ")

            if goto == 'x':
                break
            elif goto == 'p':
                print(get_diff_patch(complete_path1,complete_path2,"-qrbBX excludefiles.txt"))
            # if goto == '^':
                # back one folder
            elif goto not in diff_map:
                print("{" + goto + "} Not found!\n")
            else:
                # from here...
                complete_path1 = diff_map[goto][3]
                complete_path2 = diff_map[goto][4]
                relative_path  = diff_map[goto][5]
                my_type        = diff_map[goto][1]
        elif my_type == 'f':
            file_contents = get_diff_patch(complete_path1, complete_path2, "-NbBu")
            print(file_contents)
            break



if __name__ == "__main__":
    # MAIN STARTS HERE
    SOC="j721e"
    OS="rtos"
    VERSION1="08_01_00_13"
    VERSION2="08_02_00_05"


    base_path = '/home/tanmay/inspire/sdk/'
    SDK1_PATH = base_path + SOC + '/'+ OS + '/' + VERSION1
    SDK2_PATH = base_path + SOC + '/'+ OS + '/' + VERSION2

    relative_path = ''
    # relative_path += '/' + 'vision_apps'
    # relative_path += '/' + 'platform'
    # relative_path += '/' + 'apps/basic_demos/app_multi_cam/main.c'
    my_type = 'd'
    # my_type = 'f'
    complete_path1 = SDK1_PATH + relative_path
    complete_path2 = SDK2_PATH + relative_path
    
    browse_diff(complete_path1, complete_path2 ,relative_path, my_type)
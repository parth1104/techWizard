from django.shortcuts import render
from django.views.generic import TemplateView
import os
import json
from django.http import HttpResponse
from diff_browser import *
from diff_analyzer import *

RTOS=1
LINUX=2

gbase_path_perm = "/home/tanmay/inspire/sdk/"
gbase_path = "/home/tanmay/inspire/sdk/"
global_base1 = gbase_path_perm
global_base2 = gbase_path_perm
gsdk_type = 0


SS_IS_UNKNOWN=0
SS_IS_IF=1
SS_IS_FUNC=2
SS_IS_STRUCT=3
SS_IS_MACRO=4
SS_IS_VAR=5

# For functions : [ss_type, ss, [(file, line, func_defn)] [(file, func_called, line)] [(file, calling_func, line)]]
# For others : [ss_type, ss, [(file, line)] [(file, line)] ]
# For Variable : [ss_type, ss, [(file, in_function, line)] ]


def get_cscope_cmd(level, search_string):
    return "cscope -q -L" + str(level) + " " + search_string + " > temp_sr_file.txt"

def get_search_results_standard(search_string):
    ret = list()
    ss_type = SS_IS_UNKNOWN
    os.system(get_cscope_cmd(7, search_string))
    if os.stat('temp_sr_file.txt').st_size != 0 :
        ss_type = SS_IS_IF
        ret.append(ss_type)
        ret.append(search_string)
        def_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ')
                def_files.append((tl[0], -1))
        os.system(get_cscope_cmd(8, search_string))
        ref_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ')
                ref_files.append((tl[0], int(tl[2])))
        ret.append(def_files)
        ret.append(ref_files)
        return ret

    os.system(get_cscope_cmd(2, search_string))
    if os.stat('temp_sr_file.txt').st_size != 0 :
        ss_type = SS_IS_FUNC
        ret.append(ss_type)
        ret.append(search_string)
        called_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ')
                called_files.append((tl[0], tl[1], int(tl[2])))
        os.system(get_cscope_cmd(1, search_string))
        def_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ', 3)
                def_files.append((tl[0], int(tl[2]), tl[3][:-1]))
        os.system(get_cscope_cmd(3, search_string))
        calling_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ')
                calling_files.append((tl[0], tl[1], int(tl[2])))
        ret.append(def_files)
        ret.append(called_files)
        ret.append(calling_files)
        return ret

    os.system(get_cscope_cmd(1, search_string))
    if os.stat('temp_sr_file.txt').st_size != 0 :
        def_files = list()
        with open('temp_sr_file.txt') as srf:
            for i,line in enumerate(srf):
                if i == 0 :
                    tl = line.split(' ')
                    ss_type = SS_IS_STRUCT if line.find('#define') == -1 else SS_IS_MACRO
                    def_files.append((tl[0], int(tl[2])))
                else :    
                    tl = line.split(' ')
                    def_files.append((tl[0], int(tl[2])))
        ret.append(ss_type)
        ret.append(search_string)
        ret.append(def_files)
        os.system(get_cscope_cmd(0, search_string))
        ref_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ')
                ref_files.append((tl[0], int(tl[2])))
        ret.append(ref_files)
        return ret

    os.system(get_cscope_cmd(0, search_string))
    if os.stat('temp_sr_file.txt').st_size != 0 :
        ss_type = SS_IS_VAR
        ref_files = list()
        with open('temp_sr_file.txt') as srf:
            for line in srf:
                tl = line.split(' ')
                ref_files.append((tl[0], tl[1] ,int(tl[2])))
        ret.append(ss_type)
        ret.append(search_string)
        ret.append((-1,-1))
        ret.append(ref_files)       
        return ret

    return ret



class Test(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)

class Test2(TemplateView):
    def get(self, request, path_name=''):
        fileText = ""
        print(gbase_path)
        if path_name:
            base_path = gbase_path + path_name + "/"
        else:
            base_path = gbase_path_perm           
        if (os.path.isdir(base_path) == False):
            tl=[i for i in base_path.split('/') if i]
            base_path = '/' + '/'.join(tl[:-1]) + '/'
            scriptFile = open(base_path + tl[-1], "r")
            num_lines = sum(1 for line in scriptFile)
            scriptFile = open(base_path + tl[-1], "r")
            digits = len(str(num_lines))
            i = 1
            for fullLine in scriptFile:
                fileText = str(fileText) + str(i).ljust(digits+1, ' ') + str(fullLine)
                i = i + 1
        dir_list = os.listdir(base_path)
        dir_tuple = list()
        for item in dir_list:
            if item.startswith('.'):
                continue
            complete_path = base_path+"/"+item
            ref_path = "/browser/" + os.path.relpath(complete_path, gbase_path)
            if os.path.isdir(complete_path):
                dir_tuple.append((item, 'd', ref_path, 0))
            else:
                dir_tuple.append((item, 'f', ref_path, 0))

        isSearch = 0
        return render(request, 'browser.html', {'dir_tuple' : dir_tuple, 'fileTest' : fileText, 'isSearch' : isSearch })


class Test3(TemplateView):
    def get(self, request, **kwargs):
        fileText = ""
        sdktype = request.GET["sdktype"]
        soc = request.GET["soc"] 
        sdk = request.GET["sdk"]
        global gbase_path
        global gsdk_type
        gsdk_type = RTOS if sdktype == "rtos" else LINUX
        gbase_path = gbase_path_perm + soc + '/' + sdktype + '/' + sdk + '/'
        print(gbase_path)
        dir_list = ["Success"]
        return HttpResponse(json.dumps(dir_list))

class Test4(TemplateView):
    def get(self, request, **kwargs):
        sdk_list = []

        return render(request, 'builder.html', context=None)

class Test5(TemplateView):
    def get(self, request, **kwargs):
        sdktype = request.GET["sdktype"]
        soc = request.GET["soc"] 
        folderpath = gbase_path_perm+soc+"/"+sdktype     
        dir_list = os.listdir(folderpath)

        return HttpResponse(json.dumps(dir_list))


class Test6(TemplateView):
    def get(self, request, **kwargs):
        print("hello**************************")
        sdktype = request.GET["sdktype"]
        soc = request.GET["soc"] 
        sdk = request.GET["sdk"]
        core = request.GET["core"]
        appname = request.GET["appname"]
        build = request.GET["build"]
        folderpath=""
        make = ""
        if sdktype=="linux":
            folderpath = gbase_path_perm+soc+"/"+sdktype+"/"+sdk 
            make = "make -s "+appname
        else:
            folderpath = gbase_path_perm+soc+"/"+sdktype+"/"+sdk+"/pdk*/packages/ti/build"
            make = "make -s CORE="+core+" -C " + folderpath + " BUILD_PROFILE="+ build + " " + appname + " > output.txt"
        print(folderpath + " " + make)
        # print(1)
        # os.system('pwd')
        os.system(make)
        # print(os.getcwd())
        fileText = ""
        scriptFile = open('output.txt', "r")
        for fullLine in scriptFile:
            fileText = str(fileText) + "" + str(fullLine)
        
        print(fileText)
        temp = render(request, 'builder.html', {'fileText': fileText})
        # temp = HttpResponse(json.dumps("success"))
        # return render(request, 'builder.html', {'fileText': fileText})
        resp = []
        resp.append('success')
        resp.append(fileText)
        return HttpResponse(json.dumps(resp))







class Test7(TemplateView):
    def post(self, request, path_name=""):
        if request.method == "POST":
            searchtext = request.POST.get('searchtext', False)
        base_path = gbase_path
        dir_list = os.listdir(base_path)
        dir_tuple = list()

        if not searchtext:
            isSearch = 0
        else : 
            isSearch = 1

        for item in dir_list:
            if item.startswith('.'):
                continue
            complete_path = base_path+item
            ref_path = "/browser/" + os.path.relpath(complete_path, gbase_path)
            if os.path.isdir(complete_path):
                dir_tuple.append((item, 'd', ref_path, isSearch))
            else:
                dir_tuple.append((item, 'f', ref_path, isSearch))
            srch_res = []

        if isSearch : 
            if gsdk_type == RTOS :
                search_base_dir = base_path
            else :
                search_base_dir = base_path + "board-support/"
                for items in os.listdir(search_base_dir) : 
                    if 'linux' in items :
                        search_base_dir = search_base_dir + items + '/'
                        break
            os.chdir(search_base_dir)
            search_rel_path = os.path.relpath(search_base_dir, gbase_path) + '/'
            mylst = get_search_results_standard(searchtext)
            tt = []

            if mylst[0] == SS_IS_UNKNOWN :
                srch_res.append((0, "Cannot find any reference for " + searchtext))
            
            if mylst[0] == SS_IS_IF or mylst[0] == SS_IS_STRUCT or mylst[0] == SS_IS_MACRO:
                ts = 'file' if mylst[0] == SS_IS_IF else 'Structure' if mylst[0] == SS_IS_STRUCT else 'MACRO'
                srch_res.append((1, searchtext + " is a " + ts + "."))
                srch_res.append((1, "Defination(s) of " + searchtext + " :"))
                for item in mylst[2] :
                    tt.append((item[0]+'@'+str(item[1]), '/browser/' + search_rel_path + item[0], ''))
                srch_res.append((0, tt))
                tt=[]
                srch_res.append((1, "References for " + searchtext + " :"))
                for item in mylst[3] :
                    tt.append((item[0]+'@'+str(item[1]), '/browser/' + search_rel_path + item[0], ''))
                srch_res.append((0, tt))
                tt=[]

            if mylst[0] == SS_IS_FUNC :
                srch_res.append((1, searchtext + " is a Function."))
                srch_res.append((1, "Defination(s) of " + searchtext + " :"))
                for item in mylst[2] :
                    tt.append((item[0]+'@'+str(item[1]), '/browser/' + search_rel_path + item[0], ' ( ' + item[2] + ' )'))
                srch_res.append((0, tt))
                tt=[]
                srch_res.append((1, "Funtions called in " + searchtext + " :"))
                for item in mylst[3] :
                    tt.append((item[0]+'@'+str(item[2]), '/browser/' + search_rel_path + item[0], ' ( ' + item[1] + ' )'))
                srch_res.append((0, tt))
                tt=[]
                srch_res.append((1, "Funtions calling " + searchtext + " :"))
                for item in mylst[4] :
                    tt.append((item[0]+'@'+str(item[2]), '/browser/' + search_rel_path + item[0], ' ( ' + item[1] + ' )'))
                srch_res.append((0, tt))
                tt=[]

            if mylst[0] == SS_IS_VAR :
                srch_res.append((1, searchtext + " is a Variable."))
                srch_res.append((1, "References of " + searchtext + " :"))
                for item in mylst[2] :
                    tt.append((item[0]+'@'+str(item[2]), '/browser/' + search_rel_path + item[0], ' ( ' + item[1] + ' )'))
                srch_res.append((0, tt))
                tt=[]


        return render(request, 'browser.html', {'dir_tuple' : dir_tuple, 'fileTest' : '' , 'isSearch' : isSearch , 'srch_res' : srch_res})

class Test8(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'diff.html', context=None)

class Test9(TemplateView):
    def get(self, request, **kwargs):
        sdktype = request.GET["sdktype"]
        soc = request.GET["soc"]
        sdk1 = request.GET["sdk1"]
        sdk2 = request.GET["sdk2"]
        global gbase_path1
        global gbase_path2
        gbase_path1 = gbase_path_perm + soc + '/' + sdktype + '/' + sdk1 + '/'
        gbase_path2 = gbase_path_perm + soc + '/' + sdktype + '/' + sdk2 + '/'
        print(gbase_path1, gbase_path2)
        resp = ["Success"]
        return HttpResponse(json.dumps(resp))

    def post(self, request, **kwargs):
        if request.method == "POST":
            searchtext = request.POST.get('searchtext', False)
        base_path = gbase_path1
        lst = browse_diff_dir(gbase_path1, gbase_path2, '')
        parent = "/"
        return render(request, 'diff.html', {'parent' : parent, 'dir_tuple' : lst})

class Test10(TemplateView):
    def get(self, request, path_name):
        fileText = ""
        print(path_name)

        if path_name:
            tl = path_name.split('&')
            if tl[1] == "abs_ref/" :
                path1 = tl[2]
                path2 = tl[3]
                relpath = tl[4]
                parent = relpath.split('/')[-1]
        else:
            path1 = gbase_path1
            path2 = gbase_path2
            parent = "/"
        
        lst = browse_diff_dir(path1, path2, relpath)
        ppath = ('/'.join(lst[0][3].split('/')[:-1]), '/'.join(lst[0][4].split('/')[:-1]))

        # changes_str = get_diff_patch(path1, path2,"-qrbBX excludefiles.txt")



        # status2numchanges, extension2numchanges, func_list = get_stats(changes_str)

        stats = [('.c', 23, 45, 67), ('.lds', 23, 45, 67), ('.cfg', 23, 45, 67), ('Makefiles', 23, 45, 67), ('afddf', 45,576,47)]
        pstats = [('top_lvl', 35, 67, 65)]

        return render(request, 'diff.html', {'parent' : parent, 'dir_tuple' : lst, 'stats' : stats, 'pstats' : pstats, 'ppath' : ppath})

class Test11(TemplateView):
    def get(self, request, path_name):
        tl = path_name.split('&')
        Textfile = get_gitdiff_patch(tl[-2], tl[-1])
        if not Textfile :
            Textfile = "No changes for this file"
        return render(request, 'display_file.html', {'Textfile' : Textfile})

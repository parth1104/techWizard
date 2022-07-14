from django.shortcuts import render
from django.views.generic import TemplateView
import os
import json
from django.http import HttpResponse

gbase_path = "/home/tanmay/inspire/sdk/"

class Test(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)

class Test2(TemplateView):
    def get(self, request, path_name=''):
        fileText = ""
        if path_name:
            base_path = gbase_path + path_name + "/"
        else:
            base_path = gbase_path           
        if (os.path.isdir(base_path) == False):
            base_path = gbase_path + path_name
            scriptFile = open(base_path, "r")
            for fullLine in scriptFile:
                fileText = str(fileText) + str(fullLine)

            tl=[i for i in base_path.split('/') if i]
            base_path = '/'.join(tl[:-1]) + '/'
            print(base_path)

        dir_list = os.listdir(base_path)
        dir_tuple = list()
        for item in dir_list:
            if item.startswith('.'):
                continue
            complete_path = base_path+"/"+item
            if os.path.isdir(complete_path):
                dir_tuple.append((item, 'd'))
            else:
                dir_tuple.append((item, 'f'))
        return render(request, 'browser.html', {'dir_tuple' : dir_tuple, 'fileTest' : fileText })


class Test3(TemplateView):
    def get(self, request, path_name):
        base_path = gbase_path + path_name
        fileText = ""
        if (os.path.isfile(base_path) == True):
            scriptFile = open(base_path, "r")
            for fullLine in scriptFile:
                fileText = str(fileText) + str(fullLine)
        return render(request, 'browser.html', {'fileTest' : fileText})

class Test4(TemplateView):
    def get(self, request, **kwargs):
        sdk_list = []

        return render(request, 'builder.html', context=None)

class Test5(TemplateView):
    def get(self, request, **kwargs):
        sdktype = request.GET["sdktype"]
        soc = request.GET["soc"] 
        folderpath = gbase_path+soc+"/"+sdktype     
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
            folderpath = gbase_path+soc+"/"+sdktype+"/"+sdk 
            make = "make -s "+appname
        else:
            folderpath = gbase_path+soc+"/"+sdktype+"/"+sdk+"/pdk*/packages/ti/build"
            make = "make -s CORE="+core+" -C " + folderpath + " BUILD_PROFILE="+ build + " " + appname
        print(folderpath + " " + make)

        os.system("cd " + folderpath)
        print(1)
        os.system('pwd')
        osresponse = os.system(make)
        print(os.getcwd())
        return HttpResponse(json.dumps(osresponse))







class Test7(TemplateView):
    def get(self, request, **kwargs):
        ipst = request.GET["ipst"]
        mylst=[3, CpswAle, [('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 202)], [('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 123), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 135), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw.h', 208), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw.h', 286), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 202), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 229), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 243), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 252), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 261), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 273), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 283), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 294), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 306), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 327), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 345), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 369), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 389), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 405), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 417), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 428), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/include/cpsw/Cpsw_Ale.h', 439), ('mcusw/mcal_drv/mcal/Eth/src/Eth_Priv.c', 377), ('mcusw/mcal_drv/mcal/Eth/src/Eth_Priv.c', 1323), ('mcusw/mcal_drv/mcal/Eth/src/Eth_Priv.c', 1340), ('mcusw/mcal_drv/mcal/Eth/src/Eth_Priv.c', 1386), ('mcusw/mcal_drv/mcal/Eth/src/Eth_Priv.c', 1406), ('mcusw/mcal_drv/mcal/Eth/src/Eth_Priv.c', 1432), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 148), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 168), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 206), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 255), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 269), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 275), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 281), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 295), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 300), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 312), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 322), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 375), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 382), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 444), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 496), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 517), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 540), ('mcusw/mcal_drv/mcal/Eth/src/cpsw/Cpsw_Ale.c', 563)]]
        print(mylst)
        return HttpResponse(json.dumps(mylst))

class Test8(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'c4key.html', context=None)

class Test9(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'circuit.html', context=None)

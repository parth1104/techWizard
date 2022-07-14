from django.shortcuts import render
from django.views.generic import TemplateView
import os

gbase_path = "C:/ti/ti-processor-sdk-rtos-j7200-evm-08_01_00_11/"

class Test(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)

class Test2(TemplateView):
    def get(self, request, path_name=''):
        #global base_path
        if path_name:
            base_path = gbase_path + path_name + "/"
        else:
            base_path = gbase_path
        print(base_path)
        dir_list = os.listdir(base_path)
        dir_tuple = list()
        for item in dir_list:
            complete_path = base_path+"/"+item
            if os.path.isdir(complete_path):
                dir_tuple.append((item, 'd'))
            else:
                dir_tuple.append((item, 'f'))
        return render(request, 'browser.html', {'dir_tuple' : dir_tuple, 'testname' : base_path})


class Test3(TemplateView):
    def get(self, request, path_name):
        base_path = gbase_path + path_name
        if (os.path.isfile(base_path) == True):
            scriptFile = open(base_path, "r")
            for fullLine in scriptFile:
                fileText = str(fileText) + str(fullLine)
        return render(request, 'clue2.html', {'fileTest' : fileText})

class Test4(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'clue2.html', context=None)

class Test5(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'c2key.html', context=None)

class Test6(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'clue3.html', context=None)

class Test7(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'clue4.html', context=None)

class Test8(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'c4key.html', context=None)

class Test9(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'circuit.html', context=None)

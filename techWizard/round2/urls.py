from django.urls import re_path,path,include
from round2 import views


urlpatterns = [
    path('', views.Test.as_view()),
    path('login', views.Test.as_view()),
    re_path(r'^browser/$', views.Test2.as_view()),
    re_path(r'^browser/(?P<path_name>\S+)/$', views.Test2.as_view()),
    re_path(r'^diffbrowse/(?P<path_name>\S+)/$', views.Test10.as_view()),
    re_path(r'^builderdata/$', views.Test5.as_view()),
    re_path(r'^diffdata/$', views.Test5.as_view()),
    re_path(r'^diffsubmit/$', views.Test9.as_view()),
    path('diffpath', views.Test9.as_view(), name='diffpath'),
    re_path(r'^buildersubmit/$', views.Test6.as_view()),
    re_path(r'^bpchangesubmit/$', views.Test3.as_view()),
    path('searchString', views.Test7.as_view(), name='searchString'),
    path('builder.html', views.Test4.as_view()),
    re_path(r'^showdiff/(?P<path_name>\S+)/$', views.Test11.as_view()),
    re_path(r'^detailed_summary/(?P<path_name>\S+)/$', views.Test12.as_view()),
    re_path(r'^showverdiff/(?P<path_name>\S+)/$', views.Test13.as_view()),
    path('diff.html', views.Test8.as_view()),

]

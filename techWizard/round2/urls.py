from django.urls import re_path,path,include
from round2 import views


urlpatterns = [
    path('', views.Test.as_view()),
    path('login', views.Test.as_view()),
    re_path(r'^browser/$', views.Test2.as_view()),
    re_path(r'^browser/(?P<path_name>\S+)/$', views.Test2.as_view()),
    re_path(r'^browser/(?P<ss>\S+)$', views.Test7.as_view()),
    #re_path(r'^read/browser/(?P<path_name>\S+)/$', views.Test3.as_view()),
    path('clue2.html', views.Test4.as_view()),
    path('c2key.html', views.Test5.as_view()),
    path('clue3.html', views.Test6.as_view()),
    path('clue4.html', views.Test7.as_view()),
    path('c4key.html', views.Test8.as_view()),
    path('circuit.html', views.Test9.as_view()),

]

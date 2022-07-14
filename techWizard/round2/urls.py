from django.urls import re_path,path,include
from round2 import views


urlpatterns = [
    path('', views.Test.as_view()),
    path('login', views.Test.as_view()),
    re_path(r'^browser/$', views.Test2.as_view()),
    re_path(r'^browser/(?P<path_name>\S+)/$', views.Test2.as_view()),
    re_path(r'^read/browser/(?P<path_name>\S+)/$', views.Test3.as_view()),
    re_path(r'^builderdata/$', views.Test5.as_view()),
    re_path(r'^buildersubmit/$', views.Test6.as_view()),
    path('searchString', views.Test7.as_view(), name='searchString'),
    path('builder.html', views.Test4.as_view()),
    # re_path(r'^browser/(?P<ss>\S+)$', views.Test7.as_view()),
    path('c4key.html', views.Test8.as_view()),
    path('circuit.html', views.Test9.as_view()),

]

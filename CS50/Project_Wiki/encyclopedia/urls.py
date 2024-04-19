from django.urls import path
# .的意思是当前文件夹
from . import views, util

# 当一个项目里有多个app时为了避免文件重名，加入下列然后在引用的文件前加上appname:filename
# app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("CreateNewPage", views.CreateNewPage, name="CreateNewPage"),
    path('WikiTour', views.WikiTour, name='WikiTour'),
    path('search/', views.search, name="search_results"),
    path('<str:title>/edit/', views.Edit, name="edit"),
    path('<str:title>/save/', views.Save, name="save"),
    path('<str:title>/', views.entry, name="entry")
    
]






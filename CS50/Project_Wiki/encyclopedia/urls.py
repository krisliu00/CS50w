from django.urls import path
# .的意思是当前文件夹
from . import views

urlpatterns = [
    path("", views.index, name="index")
]


from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'network'

urlpatterns = [
    path("", views.index, name="index"),
    path('posts/<int:post_id>/like/', views.likes_api, name='like_post'),
    path('posts/<int:post_id>/edit/', views.edit_post_api, name='edit_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

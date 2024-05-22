from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("upload", views.userProfilePhoto_api, name="uploadphoto"),
    path("<str:username>", views.UserProfile_view, name="userprofile"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
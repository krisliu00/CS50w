from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
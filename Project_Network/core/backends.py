from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:

            return None

class RedirectAuthenticatedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:

            if request.path == reverse('core:login') or request.path == reverse('core:register'):
                return HttpResponseRedirect(reverse('network:index'))
        
        response = self.get_response(request)
        return response

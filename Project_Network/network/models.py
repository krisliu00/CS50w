from django.db import models
from core.models import CustomUser


class Posts(models.Model):

    text = models.TextField(max_length=1000)
    create_time = models.DateField(auto_now_add=True)
    likes = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE, related_name='network_user')

    def is_creator(self, user):
        return self.user == user
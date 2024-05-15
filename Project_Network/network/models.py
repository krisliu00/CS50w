from django.db import models
from core.models import CustomUser


class Post(models.Model):

    text = models.TextField(max_length=1000)
    create_time = models.DateField()
    likes = models.IntegerField()
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE, related_name='network_user')

    def is_creator(self, user):
        return self.user == user
from django.db import models
from core.models import CustomUser


class Posts(models.Model):
    class Meta:
        verbose_name_plural = "Posts"

    text = models.TextField(max_length=1000)
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE, related_name='network_user')

    def is_creator(self, user):
        return self.user == user
    
    def like_count(self):
        return self.postlike_set.count()
    
class PostLike(models.Model):
    user = models.ForeignKey(CustomUser, db_constraint=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
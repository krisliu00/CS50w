from django.contrib import admin
from .models import Posts

class PostsAdmin(admin.ModelAdmin):
    model = Posts
    list_display = ('text', 'user_id', 'create_time')
    list_filter = ('user_id', 'create_time')
    search_fields = ('user_id', 'create_time')

    actions = ['delete_selected']

    def delete_selected_posts(self, request, queryset):
 
        for post in queryset:
            post.delete()
        self.message_user(request, "Selected posts have been deleted successfully.")

    delete_selected_posts.short_description = "Delete selected posts"




admin.site.register(Posts, PostsAdmin)


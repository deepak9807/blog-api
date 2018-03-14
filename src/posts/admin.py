# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from posts.models import Post

# this class coustmised the Post model in Admin panel.
class PostModelAdmin(admin.ModelAdmin):
    #  We can display the more fild in admin panel  like display the fild and li
    #link the display attribut for update or edit same as Filter the based on given attribute

    list_display = ["title", "update", "timestamp"]
    list_display_links = ["title", "update"]
    list_filter = ["update", "timestamp"]
    search_fields = ["title"] # search fild 
    class Meta:
        model = Post
# Register your models here.
admin.site.register(Post, PostModelAdmin)

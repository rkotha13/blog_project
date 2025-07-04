from django.contrib import admin
from .models import User, Category, BlogPost
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(BlogPost)

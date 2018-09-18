from django.contrib import admin
from WebUser.models import WebUser
# Register your models here.


@admin.register(WebUser)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id',)



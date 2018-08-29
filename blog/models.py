from django.db import models
from django.contrib.auth.models import User  # 使用Django自带的用户模型
# Create your models here.
class Category(models.Model): #文章类别
    Category=models.CharField(maxlength=20,primary_key=True)
    def __str__(self):
        return self.Category

class Tag(models.Model) #标签
    Tag = models.CharField(maxlength=20, primary_key=True)
    def __str__(self):
        return self.Tag


class Article(models.Model):  # 文章
    id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=48,primary_key=True)
    author = models.ForeignKey(User,on_delete=)
    def __str__(self):
        return self.Art_name


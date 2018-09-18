from django.db import models
#from blog.models import Tag
# Create your models here.


class WebUser (models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    psw_md5 = models.CharField(max_length=32)
    salt = models.CharField(max_length=6)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=11,  blank=True)
    #FollowTag = models.ManyToManyField(Tag, verbose_name='所关注标签')
    FollowUser = models.ManyToManyField('self', verbose_name='所关注用户')
   # avatar = models.ImageField()
    sessionid = models.CharField(max_length=43,blank=True)
    sessionid_time = models.DateTimeField()


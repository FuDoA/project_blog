from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *

# Create your views here.

class Index(ListView):
    model = Article
    template_name = 'index.html'
    queryset = Article.objects.all().order_by('-id')  # 获取到全部文章并按编号降序排列。
    paginate_by = 5

def Detail (request,Articleid):
    return (request,'detail.html')

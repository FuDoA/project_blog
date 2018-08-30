from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import *
from django.db.models import Q

# Create your views here.

class Index(ListView):
    model = Article
    template_name = 'index.html'
    queryset = Article.objects.all().order_by('-id')  # 获取到全部文章并按编号降序排列。
    paginate_by = 5

def Detail (request,Articleid):
    return (request,'detail.html')

class Search(ListView):
    template_name = 'search.html'
    paginate_by = 5
    context_object_name = 'article'
    def get_queryset(self):
        key = self.request.GET.get('key')  # 获取查询关键字
        if key != None:
            return Article.objects.filter(Q(title__icontains=key) | Q(content__icontains=key)).order_by('-id')
            # 查询标题或者内容包含关键字的数据对象
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.request.GET.get('key')  # 获取关键字存入传入模板的数据中
        return context



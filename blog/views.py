from django.shortcuts import render
from django.shortcuts import HttpResponse
from .forms import CommentForm
# Create your views here.
from django.views.generic import ListView ,DetailView
from .models import *
from django.db.models import Q
from .forms import CommentForm
# Create your views here.

class Index(ListView):
    model = Article
    template_name = 'index.html'
    queryset = Article.objects.all().order_by('-id')  # 获取到全部文章并按编号降序排列。
    paginate_by = 5



class Search(ListView):
    template_name = 'search.html'
    paginate_by = 5
    context_object_name = 'article'
    def get_queryset(self):
        key = self.request.GET.get('key')  # 获取查询关键字
        if key !=None:
            return Article.objects.filter(Q(title__icontains=key) | Q(content__icontains=key)).order_by('-id')
            # 查询标题或者内容包含关键字的数据对象
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.request.GET.get('key')  # 获取关键字存入传入模板的数据中
        return context


class ArticleDetail(DetailView):

    context_object_name='article'
    template_name = 'detail.html'

    def get_queryset(self,*args,**kwargs):
        pk= self.kwargs['pk']
        if pk !=None:
            return Article.objects.filter(id= pk)
            # 查询标题或者内容包含关键字的数据对象
        else:
            return None

    def format_show(self, top_comment):  # 递归函数
        self.comment_list.append(top_comment)  # 将参数评论存入列表
        try:
            self.kids = self.sub_level[top_comment.id]  # 获取参数评论的所有回复评论
        except KeyError:  # 如果不存在回复评论
            pass  # 结束递归
        else:  # 否则
            for kid in self.kids:  # 遍历回复评论
                self.format_show(kid)  # 进行下一层递归

    def comment_sort(self, comments):  # 评论排序函数
        self.comment_list = []  # 排序后的评论列表
        self.top_level = []  # 存储顶级评论
        self.sub_level = {}  # 存储回复评论
        for comment in comments:  # 遍历所有评论
            if comment.reply == None:  # 如果没有回复目标
                self.top_level.append(comment)  # 存入顶级评论列表
            else:  # 否则
                self.sub_level.setdefault(comment.reply.id, []).append(comment)  # 以回复目标（父级评论）id为键存入字典
        for top_comment in self.top_level:  # 遍历顶级评论
            self.format_show(top_comment)  # 通过递归函数进行评论归类
        return self.comment_list  # 返回最终的评论列表

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(article=self.kwargs['pk'])  # 通过文章id查询评论内容
        context['comment_list'] = self.comment_sort(comments)  # 将排序归类后的文章列表存入传送到模板的数据中
        return context

def pub_comment(request):  # 发布评论函数
    if request.method == 'POST':  # 如果是post请求
        comment = Comment()  # 创建评论对象
        comment.article = Article.objects.get(id=request.POST.get('article'))  # 设置评论所属的文章
        if request.POST.get('reply') != '0':  # 如果回复的不是文章而是他人评论
            comment.reply = Comment.objects.get(id=request.POST.get('reply'))  # 设置回复的目标评论
        form = CommentForm(request.POST, instance=comment)  # 将用户的输入和评论对象结合为完整的表单数据对象
        if form.is_valid():  # 如果表单数据校验有效
            try:
                form.save()  # 将表单数据存入数据库
                result = '200'  # 提交结果为成功编码
            except:  # 如果发生异常
                result = '100'  # 提交结果为失败编码

        else:  # 如果表单数据校验无效
            result = '100'  # 提交结果为失败编码
        return HttpResponse(result)  # 返回提交结果到页面
    else:  # 如果不是post请求
        return HttpResponse('非法请求！')  # 返回提交结果到页面
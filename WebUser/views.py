from django.shortcuts import render
from WebUser.models import  WebUser
# Create your views here.
from django.shortcuts import HttpResponse
def Login (request):
    pass



def Reg (request):
    if request.method == 'GET':
        return render(request, 'reg.html')
    elif request.method == 'POST':
        webuser_id = request.POST.get('user_id')
        webuser_salt = request.POST.get('user_salt')
        webuser_pswmd5 = request.POST.get('user_pswmd5')
        if WebUser.objects.filter(id=webuser_id):
            return HttpResponse(400)  #返回数字400标识已存在该用户
        else:
            try:
                newuser = WebUser(id=webuser_id,salt=webuser_salt,psw_md5=webuser_pswmd5)
                newuser.save()
                return HttpResponse(100)  #返回数字100标识注册成功
            except:
                return HttpResponse(401) #返回数字401标识意外错误




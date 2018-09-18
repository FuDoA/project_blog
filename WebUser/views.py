from django.shortcuts import render
from WebUser.models import  WebUser
import datetime,random
# Create your views here.
from django.shortcuts import HttpResponse


def Login (request):
    if request.method == 'GET':
        if request.COOKIES.get('SessionId'):         #有session信息
            sessionid=request.COOKIES.get('SessionId')
            user=WebUser.objects.filter(SessionId=sessionid).first()
            if user.SessionId_time < datetime.datetime.now():       #若session过期
                return render(request, 'login.html',{'logined': False})
            else:           #session未过期
                return render(request,'login.html',{'logined':True,'user':user})

        else:               #无session信息
            return render(request, 'login.html', {'logined': False})

    elif request.method == 'POST':
        if not request.POST.get('user_pswmd5'):     #查询salt
            if request.POST.get('user_id'):
                user_id = request.POST.get('user_id')
                if WebUser.objects.filter(id=user_id).first():
                    user = WebUser.objects.filter(id=user_id).first()
                    return HttpResponse(user.salt)
                else:
                    return HttpResponse('401')
            else:
                return HttpResponse('401')

        else:                                        #检验加盐密码
            user_id = request.POST.get('user_id')
            if user_id:
                user = WebUser.objects.filter(id=user_id).first()
            user_pswmd5 = request.POST.get('user_pswmd5')
            if user_pswmd5 == user.pswmd5:          #密码检验成功
                user.sessionid = str(random.randint(1, 9999999999999999999999))
                user.sessionid_time = datetime.datetime.now()+datetime.timedelta(day=7)
                user.save()
                response = render(request, 'login.html', {'logined': True, 'user': user})
                response.set_cookie('tempid', user.sessionid)
                return response
            else:
                return HttpResponse('401')  #密码错误






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
            #try:
            newuser = WebUser(id=webuser_id, salt=webuser_salt,psw_md5=webuser_pswmd5,sessionid_time=datetime.datetime.now())
            newuser.save()
            return HttpResponse(100)  #返回数字100标识注册成功
            #except:
                #return HttpResponse(401) #返回数字401标识意外错误




from WebUser.models import WebUser
import datetime
def islogined (request):
    if request.COOKIES.get('tempid'):  # 有session信息
        tempid = request.COOKIES.get('tempid')
        if WebUser.objects.filter(sessionid=tempid):
            user = WebUser.objects.filter(sessionid=tempid).first()
            tempid_life = user.sessionid_time.replace(tzinfo=None)
            if tempid_life < datetime.datetime.now():  # 若session过期
                return {'logined': False}
            else:  # session未过期
                return {'logined': True, 'user': user}
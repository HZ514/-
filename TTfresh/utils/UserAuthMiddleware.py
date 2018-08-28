from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import User, UserStatus


class MyMiddle(MiddlewareMixin):

    def process_request(self,request):
        # 获取的地址不包含？后的参数
        path = request.path
        fg_list = ['/home/index/','/users/login/','/users/register/','/admin/','/backweb/login/',
                   '/backweb/logout/','/home/list/','/home/detail/']
        if path in fg_list:
            return None
        # 获取ticket，如果没有则说明没有登录，让其跳转至登录页面
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user = UserStatus.objects.filter(ticket=ticket).first()

        if not user:
            return HttpResponseRedirect(reverse('user:login'))
        # 将当前的用户给django自带的用户
        request.user = user.user

        return None

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from user.models import User, UserStatus


class MyMiddle(MiddlewareMixin):

    def process_request(self,request):
        # 获取的地址不包含？后的参数
        path = request.path
        fg_list = ['/users/login/','/users/register/','/admin/','/backweb/login/',
                   '/backweb/logout/',]

        if path in fg_list :
            return None

        # 获取ticket，如果没有则说明没有登录，让其跳转至登录页面
        f_list = ['/home/index/','/home/list/','/home/detail/']
        ticket = request.COOKIES.get('ticket')
        if not ticket and path not in f_list:
            return HttpResponseRedirect(reverse('user:login'))

        user = UserStatus.objects.filter(ticket=ticket).first()

        if not user and path not in f_list:
            return HttpResponseRedirect(reverse('user:login'))
        # 将当前的用户给django自带的用户
        if user:
            request.user = user.user




        return None

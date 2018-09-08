import random
from datetime import datetime,timedelta
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from user.models import User, UserStatus


def register(request):
    if request.method == 'GET':
        return render(request,'web/register.html')

    if request.method == 'POST':
        if request.method == 'POST':
            username = request.POST.get('user_name')
            email = request.POST.get('email')
            password1 = request.POST.get('pwd')
            password2 = request.POST.get('cpwd')
            if not all([username, password1,password2, email]):
                error = {'msg': '不能有空'}
                return render(request, 'web/register.html', error)
            user = User.objects.filter(u_name=username)
            if user:
                error = {'msg': '该用户名已被注册'}
                return render(request, 'web/register.html', error)
            if password2 != password1:
                error = {'msg':'两次输入的密码不一致'}
                return render(request,'web/register.html',error)
            User.objects.create(u_name=username,
                                u_password=make_password(password1),
                                u_email=email,
                                     )
            return HttpResponseRedirect(reverse('user:login'))


def login(request):
    if request.method == 'GET':
        return render(request,'web/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        if not all([username,password]):
            error = {'msg': '请输入完整'}
            return render(request,'web/login.html',error)
        user = User.objects.filter(u_name=username).first()
        if not user:
            error = {'msg': '用户不存在'}
            return render(request,'web/login.html',error)
        if not check_password(password,user.u_password):
            error = {'msg': '密码错误'}
            return render(request,'web/login.html',error)
        # 创建用户状态
        # 1、在服务器中添加
        res = HttpResponseRedirect(reverse('home:index'))
        s = 'sdfkshfksakfasfdsfasdkjhs'
        ticket = ''
        for i in range(20):
            ticket += random.choice(s)
        out_time = datetime.now() + timedelta(days=1)

        # 检查状态表中是否已经有状态，如果已经有则替换原来的状态
        userticket = user.userstatus_set.all().first()

        # request.session['cart'] = {'id':1,'home':2}
        # request.session['cart1'] = {'id':1,'home':2}
        #
        # print(request.session)

        if userticket:
            userticket.ticket = ticket
            userticket.out_time = out_time
            userticket.save()
            res.set_cookie('ticket', ticket, expires=out_time)
            return res
        UserStatus.objects.create(user_id=user.id,ticket=ticket,out_time=out_time)

        # 2、在本地存储ticket
        res.set_cookie('ticket',ticket,expires=out_time)
        return res


# 退出
def logout(request):
    if request.method == 'GET':
        # 删除服务端的ticket值
        user = request.user
        user.userstatus_set.all().delete()
        # 删除cookie中的ticket
        res = HttpResponseRedirect(reverse('user:login'))
        res.delete_cookie('ticket')
        return res

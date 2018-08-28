import random
from datetime import datetime,timedelta
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from backweb.models import MainSide, FoodType, Goods
from user.models import User, UserStatus



def login(request):
    if request.method == 'GET':
        return render(request,'backweb/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username,password]):
            error = {'msg': '请输入完整'}
            return render(request,'backweb/login.html',error)
        user = User.objects.filter(u_name=username).first()
        if not user:
            error = {'msg': '用户不存在'}
            return render(request,'backweb/login.html',error)
        if not check_password(password,user.u_password):
            error = {'msg': '密码错误'}
            return render(request,'backweb/login.html',error)
        # 创建用户状态
        # 1、在服务器中添加
        res = HttpResponseRedirect(reverse('backweb:index'))
        s = 'sdfkshfksakfasfdsfasdkjhs'
        ticket = ''
        for i in range(20):
            ticket += random.choice(s)
        out_time = datetime.now() + timedelta(days=1)

        # 检查状态表中是否已经有状态，如果已经有则替换原来的状态
        userticket = user.userstatus_set.all().first()
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


def logout(request):
    def logout(request):
        if request.method == 'GET':
            # 删除服务端的ticket值
            user = request.user
            user.delete()
            # 删除cookie中的ticket
            res = HttpResponseRedirect(reverse('backweb:login'))
            res.delete_cookie('ticket')
            return res


def index(request):
    if request.method == 'GET':

        return render(request,'backweb/index.html')


def update_postwd(request):
    if request.method == 'GET':
        return render(request, 'backweb/updatePostwd.html')
    if request.method == 'POST':
        user = request.user
        password = user.password
        new_password = request.POST.get('new_password')
        sure_password = request.POST.get('sure_password')
        if new_password == password:
            error = '新密码不能与旧密码一样'
            return render(request, 'backweb/updatePostwd.html', {'error': error})
        if new_password == sure_password:
            user = request.user
            user.password = new_password
            user.save()
            return HttpResponseRedirect(reverse('backweb:index'))
        else:
            error = '密码不一致'
            return render(request,'backweb/updatePostwd.html',{'error':error})

def listUser(request):
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'backweb/users_list.html', {'users': users})


def add_side(request):
    if request.method == 'GET':
        return render(request,'backweb/add_side.html')
    if request.method == 'POST':
        side_name = request.POST.get('side_name')
        img = request.FILES.get('img')
        MainSide.objects.create(name=side_name,img=img)
        return HttpResponseRedirect(reverse('backweb:add_side'))

def add_type(request):
    if request.method == 'GET':
        return render(request,'backweb/add_type.html')

    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        type_name = request.POST.get('type_name')
        type_img = request.FILES.get('img')
        FoodType.objects.create(typeid=type_id,typename=type_name,type_img=type_img)
        return HttpResponseRedirect(reverse('backweb:add_type'))


def type_manage(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        types = FoodType.objects.all()
        paginator = Paginator(types,5)
        page = paginator.page(page_num)
        data = {
            'page':page,
        }
        return render(request,'backweb/type_manage.html',data)


def product_delete(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('backweb:index'))


def editor_type(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        type = FoodType.objects.filter(id=id).first()
        data = {
            'type':type,
        }
        return render(request,'backweb/editor_type.html', data)

    if request.method == 'POST':
        id = request.POST.get('id')
        type_id = request.POST.get('type_id')
        type_name = request.POST.get('type_name')
        img = request.FILES.get('img')
        if not img:
            img = FoodType.objects.get(id=id).type_img
        FoodType.objects.filter(id=id).update(typeid=type_id,typename=type_name,type_img=img)

        return HttpResponseRedirect(reverse('backweb:type_manage'))


def add_product(request):
    if request.method == 'GET':
        types = FoodType.objects.all()
        data = {
            'types':types,
        }
        return render(request,'backweb/add_product.html',data)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        one_weight = request.POST.get('one_weight')
        img = request.FILES.get('img')
        type = request.POST.get('type')
        introduction = request.POST.get('introduction')
        detail = request.POST.get('detail')
        goods_type = request.POST.get('goods_type')
        food_type = FoodType.objects.get(typename=goods_type)
        data = {}
        # if not all([product_id,product_name,price,one_weight,img,type,int,detail,introduction]):
        #     data['msg'] = '不能有空'
        #     return render(request,'backweb/add_product.html',data)
        type = 0 if type == 'no' else 1
        Goods.objects.create(productid=product_id,productimg=img,productname=product_name,
                             pmdesc=introduction,is_new=type,price=price,one_weight=one_weight,
                             detail=detail,goods_type=food_type)

        return HttpResponseRedirect(reverse('backweb:add_product'))


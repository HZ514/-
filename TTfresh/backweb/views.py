import random
from datetime import datetime,timedelta
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backweb.models import MainSide, FoodType, Goods
from user.models import User, UserStatus


# 登录
def login(request):
    if request.method == 'GET':
        return render(request,'backweb/user/login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username,password]):
            error = {'msg': '请输入完整'}
            return render(request,'backweb/user/login.html',error)
        user = User.objects.filter(u_name=username).first()
        if not user:
            error = {'msg': '用户不存在'}
            return render(request,'backweb/user/login.html',error)
        if not check_password(password,user.u_password):
            error = {'msg': '密码错误'}
            return render(request,'backweb/user/login.html',error)
        if not user.is_superuser:
            error = {'msg':'你没有权限登录'}
            return render(request, 'backweb/user/login.html', error)
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


# 退出
def logout(request):
    if request.method == 'GET':
        # 删除服务端的ticket值
        user = request.user
        user_status = user.userstatus_set.all().delete()
        # 删除cookie中的ticket
        res = HttpResponseRedirect(reverse('backweb:login'))
        res.delete_cookie('ticket')
        return res


# 主页
@csrf_exempt
def index(request):
    if request.method == 'GET':

        return render(request,'backweb/index/index.html')


# 商品展示
def good_list(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        type = request.GET.get('type',0)
        context = request.GET.get('context','')
        # 如果拿不到分类则将type_id设置为0
        if not type:
            type_id = int(type)
        else:
            type_id = int(type)
        # 所有的分类
        type_list = FoodType.objects.all()
        # 根据相应的分类查找相应的商品
        # 如果type_id不为0则获取相应分类的商品
        if not type_id:
            goods = Goods.objects.all()
        else:
            goods = Goods.objects.filter(goods_type_id=type_id)

        # 如果有搜索条件则按照搜索条件模糊查询
        if context:
            goods = Goods.objects.filter(goods_type_id=type_id,productname__contains=context)
            if not goods:
                goods = Goods.objects.filter(goods_type_id=type_id,productname__contains=context[-1])





        paginator = Paginator(goods, 3)
        page = paginator.page(page_num)

        data = {
            'page': page,
            'type_list': type_list,
            'type_id': type_id,
            'context':context,
        }

        return render(request, 'backweb/good/good_list.html',data)

    if request.method == 'POST':
        data = {}
        data['code'] = 200
        data['msg'] = '请求成功'
        id = int(request.POST.get('id'))
        ta = request.POST.get('ta')
        data['ta'] = ta

        good = Goods.objects.filter(id=id)
        if ta == '推荐':
            good.update(is_new=0)
        elif ta == '不推荐':
            good.update(is_new=1)

        return JsonResponse(data)


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


# 添加幻灯片图片
def add_side(request):
    if request.method == 'GET':
        return render(request,'backweb/side/add_side.html')
    if request.method == 'POST':
        side_name = request.POST.get('side_name')
        img = request.FILES.get('img')
        MainSide.objects.create(name=side_name,img=img)
        return HttpResponseRedirect(reverse('backweb:add_side'))


# 添加分类
def add_type(request):
    if request.method == 'GET':
        return render(request,'backweb/type/add_type.html')

    if request.method == 'POST':
        type_id = request.POST.get('type_id')
        type_name = request.POST.get('type_name')
        type_img = request.FILES.get('img')
        FoodType.objects.create(typeid=type_id,typename=type_name,type_img=type_img)
        return HttpResponseRedirect(reverse('backweb:add_type'))


# 分类分页管理
def manage_type(request):
    if request.method == 'GET':
        page_num = int(request.GET.get('page', 1))
        types = FoodType.objects.all()
        paginator = Paginator(types,5)
        page = paginator.page(page_num)
        data = {
            'page':page,
        }
        return render(request,'backweb/type/type_list.html',data)


# 删除商品
def good_delete(request, id):
    if request.method == 'GET':

        Goods.objects.filter(id=int(id)).delete()
        return HttpResponseRedirect(reverse('backweb:index'))


# 编辑分类
def editor_type(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        type = FoodType.objects.filter(id=id).first()
        data = {
            'type':type,
        }
        return render(request,'backweb/type/editor_type.html', data)

    if request.method == 'POST':
        id = request.POST.get('id')
        type_id = request.POST.get('type_id')
        type_name = request.POST.get('type_name')
        img = request.FILES.get('img')
        if not img:
            img = FoodType.objects.get(id=id).type_img
        FoodType.objects.filter(id=id).update(typeid=type_id,typename=type_name,type_img=img)

        return HttpResponseRedirect(reverse('backweb:manage_type'))

# 添加商品
def add_product(request):
    if request.method == 'GET':
        types = FoodType.objects.all()
        data = {
            'types':types,
        }
        return render(request,'backweb/good/add_product.html',data)

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


# 编辑商品
def good_editor(request, id):
    if request.method == 'GET':
        good = Goods.objects.filter(id=id).first()
        types = FoodType.objects.all()
        data = {
            'good': good,
            'types':types
        }
        return render(request,'backweb/good/editor_product.html', data)

    if request.method == 'POST':
        id = request.POST.get('id')
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        price = float(request.POST.get('price'))
        one_weight = request.POST.get('one_weight')
        img = request.FILES.get('img')
        type = request.POST.get('type')
        goods_type = request.POST.get('goods_type')
        food_type = FoodType.objects.filter(typename=goods_type).first()
        introduction = request.POST.get('introduction')
        detail = request.POST.get('detail')

        if not img:
            img = Goods.objects.get(id=id).productimg

        type = 0 if type == 'no' else 1
        Goods.objects.filter(id=int(id)).update(productid=product_id, productimg=img, productname=product_name,
                             pmdesc=introduction, is_new=type, price=price, one_weight=one_weight,
                             detail=detail, goods_type=food_type)

        return HttpResponseRedirect(reverse('backweb:index'))


# 幻灯片展示
def slide_list(request):
    if request.method == 'GET':
        sides = MainSide.objects.all()
        data = {
            'sides':sides
        }
        return render(request,'backweb/side/slide_list.html',data)


# 幻灯片删除
def del_side(request,id):
    if request.method == 'GET':
        MainSide.objects.filter(id=int(id)).delete()
        return HttpResponseRedirect(reverse('backweb:slide_list'))


# 幻灯片编辑
def editor_side(request):
    if request.method == 'GET':
        id = int(request.GET.get('id'))
        side = MainSide.objects.filter(id=id).first()
        return render(request,'backweb/side/editor_side.html',{'side':side})

    if request.method == 'POST':
        id = request.POST.get('id')
        side_name = request.POST.get('side_name')
        img = request.FILES.get('img')
        side = MainSide.objects.filter(id=id)
        if not img:
            side.update(name=side_name)
        else:
            side.update(name=side_name,img=img)
        return HttpResponseRedirect(reverse('backweb:slide_list'))

# 删除分类
def delete_type(request, id):
    if request.method == 'GET':
        FoodType.objects.filter(id=int(id)).delete()
        return HttpResponseRedirect(reverse('backweb:manage_type'))


# 查询商品
def select_goods(request):
    if request.method == 'GET':
        data={}
        type_id = request.GET.get('type')
        context = request.GET.get('context')
        return render(request,'backweb/index/index.html')

    if request.method == 'POST':
        data = {}
        return JsonResponse(data)
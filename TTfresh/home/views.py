from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from user.models import UserReceivInfo
from utils.functions import get_order_number

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backweb.models import MainSide, FoodType, Goods, Cart, Order, OrderGoodsModel, UserBrowse


def index(request):
    if request.method == 'GET':
        sides = MainSide.objects.all()
        types = FoodType.objects.all()
        data = {
            'sides': sides,
            'types':types,
        }
        return render(request,'web/index.html',data)


def list(request):
    if request.method == 'GET':
        type_name = request.GET.get('type')
        sort = request.GET.get('sort', 0)
        page_num = request.GET.get('page',1)
        types = FoodType.objects.all()
        type = FoodType.objects.filter(typename=type_name).first()
        goods = type.goods_set.all()
        c_count = Cart.objects.all().count
        if sort == 1:
            goods = type.goods_set.all().order_by('price')
        paginator = Paginator(goods,15)
        page = paginator.page(page_num)

        # 类型的新品
        new_foods = Goods.objects.filter(goods_type=type,is_new=1)
        data = {
            'types':types,
            'type':type,
            'page': page,
            'new_foods':new_foods,
            'c_count':c_count,
        }
        return render(request, 'web/list.html',data)
        # return HttpResponseRedirect(reverse('home:list_show',kwargs={'typename':typeid}))


def detail(request):
    if request.method == 'GET':
        user = request.user
        typename = request.GET.get('type')
        product_id = request.GET.get('product_id')
        food_type = FoodType.objects.filter(typename=typename)
        new_goods = Goods.objects.filter(goods_type=food_type, is_new=1)
        good = Goods.objects.filter(id=product_id).first()
        c_count = Cart.objects.all().count()
        data = {
            'typename': typename,
            'good': good,
            'new_goods': new_goods,
            'c_count': c_count,
        }
        if user.id:
            # 如果浏览的商品已经存在，则修改浏览时间，不存在则创建新的浏览商品信息
            if UserBrowse.objects.filter(good=good).exists():
                userrrowse = UserBrowse.objects.get(good=good)
                userrrowse.browse_time = datetime.now()
                userrrowse.save()
            else:
                UserBrowse.objects.create(user=user,good=good)

            return render(request,'web/detail.html',data)
        else:
            return render(request, 'web/detail.html',data)


def add_product(request):
    if request.method == 'POST':
        user = request.user
        if user.id:
            good_id = request.POST.get('goods_id')
            num = int(request.POST.get('num'))
            num += 1
            prices = Goods.objects.get(id=good_id).price * num
            prices = round(prices,3)
            c_data = {'c_num': num,'prices':prices}
            data = {
                'code': 200,
                'msg': '请求成功',
                'data': c_data
            }
            return JsonResponse(data)
        else:
            data = {
                'code': 1001,
                'msg': '用户没有登录',
                'data': ''
            }
            # 以json格式返回
            return JsonResponse(data)


def reduce_Cart(request):

    if request.method == 'POST':
        user = request.user
        if user.id:
            data = {}
        data['code'] =200
        data['mas'] ='请求成功'
        if user:
            num = int(request.POST.get('num'))
            good_id = request.POST.get('goods_id')
            if num > 1:
                num -= 1
                prices = Goods.objects.get(id=good_id).price * num
                prices = round(prices, 3)
                data['c_num'] = num
                data['prices'] = prices
            else:
                data['code'] = 1001

            return JsonResponse(data)
        else:
            data = {
                'code': 200,
                'msg': '用户没有登录',
                'data': ''
            }
            # 以json格式返回
            return JsonResponse(data)


def add_cart(request):
    if request.method == 'POST':
        user = request.user
        data = {}
        data['code'] = 200
        data['msg'] = '请求成功'
        if user.id:
            goods_id = request.POST.get('goods_id')
            num = int(request.POST.get('num'))

            prices = Goods.objects.get(id=goods_id).price * num
            prices = round(prices, 3)
            if num > 0:
                Cart.objects.create(user=user,
                                    goods_id=goods_id, c_num=num,c_prices=prices)

                c_count = Cart.objects.all().count()
                data['c_count'] = c_count
            else:
                data['code'] = 1001

            return JsonResponse(data)
        else:
            data = {
                'code': 200,
                'msg': '用户没有登录',
                'data': ''
            }
            # 以json格式返回
            return JsonResponse(data)


# 我的购物车
def my_cart(request):
    if request.method == 'GET':
        user = request.user
        if user:
            carts = Cart.objects.all()
            count = carts.count

            carts = Cart.objects.all()
            moneys = 0
            for cart in carts:
                moneys += cart.c_prices
            data = {
                'carts': carts,
                'count': count,
                'moneys':round(moneys,3)
            }
            return render(request,'web/cart.html',data)
        else:
            return render(request,'web/cart.html')


# 我的订单
def my_order(request):
    if request.method == 'GET':
        user = request.user
        if user:
            carts = Cart.objects.all()
            count = carts.count
            data = {
                'carts':carts,
                'count':count
            }
            return render(request,'web/cart.html',data)
        else:
            return render(request,'web/cart.html')


@csrf_exempt
# 购物车选择
def is_select(request):
    if request.method == 'POST':
        data = {}
        cart_id = request.POST.get('cart_id')
        # cart_id = int(request.POST.get('select'))
        cart = Cart.objects.get(id=cart_id)
        if cart.is_select:
            cart.is_select = 0
            cart.save()
        else:
            cart.is_select = 1
            cart.save()
        if Cart.objects.filter(is_select=0).exists():
            all_select = 0
        else:
            all_select = 1

        data['all_select'] = all_select

        return JsonResponse(data)


# 是否全选
@csrf_exempt
def all_select(request):
    if request.method == 'POST':
        data = {}
        is_all = request.POST.get('is_all')
        if is_all == 'true':
            Cart.objects.update(is_select=1)
            f_is_all = 1
        else:
            Cart.objects.update(is_select=0)
            f_is_all = 0
        data['f_is_all'] =f_is_all
        # 返回全部的购物车数据
        carts_id = []
        for cart in Cart.objects.all():
            carts_id.append(cart.id)
        data['carts_id'] = carts_id
        return JsonResponse(data)


# 刚进页面的全选状态
def is_all_o(request):
    if request.method == 'GET':
        user = request.user
        if Cart.objects.filter(user=user,is_select=0).exists():
            status = 0
        else:
            status = 1
        data = {
            'code': 200,
            'msg': '请求成功',
            'status': status
        }
        return JsonResponse(data)


# 添加购物车商品
def add_goods_num(request):
    if request.method == 'POST':
        user = request.user
        if user:
            data = {}
            cart_id = int(request.POST.get('cart_id'))
            # 将购物车的商品增加1
            cart = Cart.objects.filter(id=cart_id,user=user).first()
            cart.c_num = cart.c_num + 1
            cart.save()
            # 获取商品增加后的数量
            data['c_num'] = cart.c_num
            # 获取商品增加后的金额
            cart = Cart.objects.filter(id=cart_id).first()
            cart.c_prices = cart.c_num * cart.goods.price
            cart.save()
            cart = Cart.objects.filter(id=cart_id).first()
            data['c_prices'] = round(cart.c_prices,3)
            # 获取增加后所有购物车商品的总金额
            moneys = 0
            carts = Cart.objects.all()
            for cart in carts:
                moneys += cart.c_prices
            data['moneys'] = round(moneys,3)

            return JsonResponse(data)


# 减少购物车商品
def reduct_good_num(request):
    if request.method == 'POST':
        user = request.user
        data = {}
        data['code'] = 200
        data['msg'] = '请求成功'
        if user:
            cart_id = int(request.POST.get('cart_id'))
            num = int(request.POST.get('num'))
            if num > 1:
                cart = Cart.objects.filter(id=cart_id,user=user).first()
                # 将购物车的商品减1
                c_num = cart.c_num - 1
                cart.c_num = c_num
                cart.save()
                # 获取商品减少后的数量
                data['c_num'] = c_num
                # 获取商品减少后的金额
                cart.c_prices = c_num * cart.goods.price
                cart.save()
                cart = Cart.objects.filter(id=cart_id).first()
                data['c_prices'] = round(cart.c_prices, 3)
                # 获取增加后所有购物车商品的总金额
                moneys = 0
                carts = Cart.objects.all()
                for cart in carts:
                    moneys += cart.c_prices
                data['moneys'] = round(moneys, 3)
                return JsonResponse(data)
            else:
                data['code'] = 1001
                return JsonResponse(data)
        else:
            data = {
                'code': 200,
                'msg': '用户没有登录',
                'data': ''
            }
            # 以json格式返回
            return JsonResponse(data)


# 删除需要删除的购物车信息
def delete_cart(request):
    if request.method == 'POST':
        data = {}
        data['code'] = 200
        data['msg'] = '请求成功'
        cart_id = request.POST.get('cart_id')
        Cart.objects.filter(id=cart_id).delete()
        return JsonResponse(data)


# 选择订单
def place_order(request):
    if request.method == "GET":
        user = request.user
        if user:
            c_list = []
            carts = Cart.objects.filter(is_select=1,user=user)
            i = 1
            for cart in carts:
                c_list.append([cart,i])
                i += 1
            c_count = Cart.objects.all().count()
            moneys = 0
            for cart in carts:
                moneys += cart.c_prices

            data = {
                'c_list': c_list,
                'c_count': c_count,
                'moneys':round(moneys,3)

            }

            return render(request, 'web/place_order.html',data)


# 添加订单
def add_order(request):
    if request.method == 'POST':
        user = request.user

        if user:
            zt = int(request.POST.get('zt'))
            userinfo = user.userreceivinfo_set.all()[0]
            # 生成订单编号
            order_id = get_order_number()

            # 获取购物车中选中的商品
            carts = Cart.objects.filter(user=user, is_select=1)
            # 获取选中的物品的总金额
            moneys = 0
            for cart in carts:
                moneys += cart.c_prices
            o_prices = round(moneys,3)

            if zt:
                # 生成支付订单
                order = Order.objects.create(order_id=order_id,user=user,
                                             order_status=1,userinfo=userinfo, o_prices=o_prices)
            else:
                # 生成待支付订单
                order = Order.objects.create(order_id=order_id,
                                             user=user, order_status=0,userinfo=userinfo,o_prices=o_prices)

            # 创建订单物品表
            for cart in carts:
                OrderGoodsModel.objects.create(order=order,goods=cart.goods,goods_num=cart.c_num,goods_price=cart.c_prices)

            # 删除购物车中被选中的物品
            carts.delete()

            data = {
            }
            return JsonResponse(data)


# 订单展示
def order_show(request):
    if request.method == 'GET':
        user = request.user
        if user:
            num_page = request.GET.get('page',1)
            orders = Order.objects.filter(user=user)
            paginator = Paginator(orders,3)
            page = paginator.page(num_page)
            data = {
                'page':page,
            }
            return render(request,'web/user_center_order.html',data)


# 用户信息
def userInfo(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            userbrowses = UserBrowse.objects.filter(user=user).order_by('-browse_time')[0:5]
            data = {
                'userbrowses':userbrowses,
            }
            return render(request,'web/user_center_info.html',data)


def user_site(request):
    if request.method == 'GET':
        return render(request,'web/user_center_site.html')

    if request.method == 'POST':
        return HttpResponseRedirect(reverse('home:user_site'))
from datetime import datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from home.models import SessionCart
from user.models import UserReceivInfo, User, UserInfo
from utils.functions import get_order_number

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from backweb.models import MainSide, FoodType, Goods, Cart, Order, OrderGoodsModel, UserBrowse

# 主页
def index(request):
    if request.method == 'GET':
        user = request.user
        sides = MainSide.objects.all()
        types = FoodType.objects.all()
        c_count = Cart.objects.all().count()
        data = {
            'c_count': c_count,
            'sides': sides,
            'types': types,
        }
        if user.id:
            # 当用户登录成功后，将sessino中的数据同步到用户的购物车中
            all_key = request.session.keys()
            for key in all_key:
                s_cart = request.session.get(key)
                # 商品数量
                c_num = int(s_cart.get('num'))
                # 商品id
                good_id = s_cart.get('good_id')
                # 单价
                price = Goods.objects.get(id=good_id).price
                # 总价
                c_peices = round(price * c_num)
                # 选中状态
                is_select = s_cart.get('is_select')
                cart = Cart.objects.filter(user=user,goods_id=good_id).first()
                if not cart:
                    Cart.objects.create(user=user,
                                        goods_id=good_id, c_num=c_num, c_prices=c_peices,is_select=is_select)
                else:
                    cart.c_num += c_num
                    cart.c_prices += c_peices
                    cart.save()
            # 删除session
            request.session.flush()

            return render(request,'web/index.html',data)
        else:
            c_count = len(request.session.keys())
            data['c_count'] = c_count
            return render(request,'web/index.html',data)


# 商品列表
def list(request):
    if request.method == 'GET':
        user = request.user
        type_name = request.GET.get('type')
        sort = request.GET.get('sort', 0)
        page_num = int(request.GET.get('page', 1))
        types = FoodType.objects.all()
        type = FoodType.objects.filter(typename=type_name).first()
        goods = type.goods_set.all()
        c_count = Cart.objects.all().count
        if sort == 1:
            goods = type.goods_set.all().order_by('price')
        paginator = Paginator(goods, 15)
        page = paginator.page(page_num)
        # 类型的新品
        new_foods = Goods.objects.filter(goods_type=type, is_new=1)
        data = {
            'types': types,
            'type': type,
            'page': page,
            'new_foods': new_foods,
            'c_count': c_count,
        }
        if user.id:
            return render(request, 'web/list.html',data)
        # return HttpResponseRedirect(reverse('home:list_show',kwargs={'typename':typeid}))
        else:
            c_count = len(request.session.keys())
            data['c_count'] = c_count
            return render(request, 'web/index.html', data)


# 详情
def detail(request):
    if request.method == 'GET':
        user = request.user
        typename = request.GET.get('type')
        product_id = request.GET.get('product_id')
        food_type = FoodType.objects.filter(typename=typename)
        new_goods = Goods.objects.filter(goods_type=food_type, is_new=1)
        good = Goods.objects.filter(id=product_id).first()
        c_count = Cart.objects.all().count()
        data = {}
        data['typename'] = typename
        data['good'] = good
        data['new_goods'] = new_goods
        data['c_count'] = c_count
        if user.id:
            # 如果浏览的商品已经存在，则修改浏览时间，不存在则创建新的浏览商品信息
            if UserBrowse.objects.filter(good=good).exists():
                userrrowse = UserBrowse.objects.get(good_id=good.id)
                userrrowse.browse_time = datetime.now()
                userrrowse.save()
            else:
                UserBrowse.objects.create(user=user,good=good)

            return render(request,'web/detail.html',data)
        else:
            c_count = len(request.session.keys())
            data['c_count'] = c_count

            return render(request, 'web/detail.html',data)

# 添加商品
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
            good_id = request.POST.get('goods_id')
            num = int(request.POST.get('num'))
            num += 1
            prices = Goods.objects.get(id=good_id).price * num
            prices = round(prices, 3)
            c_data = {'c_num': num, 'prices': prices}

            data = {
                'code': 1001,
                'msg': '用户没有登录',
                'data': c_data
            }
            # 以json格式返回
            return JsonResponse(data)


#减少商品
def reduce_Cart(request):

    if request.method == 'POST':
        user = request.user
        data = {}
        if user.id:
            data['code'] =200
            data['mas'] ='请求成功'
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
            data['code'] = 200
            data['mas'] = '请求成功'
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
            # 以json格式返回
            return JsonResponse(data)

# 添加购物车
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
                cart = Cart.objects.filter(user=user,goods_id=goods_id).first()
                if not cart:
                    Cart.objects.create(user=user,
                                        goods_id=goods_id, c_num=num,c_prices=prices)

                else:
                    c_num = cart.c_num + num
                    prices = Goods.objects.get(id=goods_id).price * c_num
                    prices = round(prices, 3)
                    # 将相同的订单整合
                    cart.c_num = c_num
                    cart.c_prices = prices
                    cart.save()

            else:
                data['code'] = 1001

            c_count = Cart.objects.all().count()
            data['c_count'] = c_count
            return JsonResponse(data)
        else:
            goods_id = request.POST.get('goods_id')
            num = int(request.POST.get('num'))
            if num > 0:
                # 如果用户未登录，则将数据存放在session中。
                c_id = datetime.now().strftime('%Y%m%d%H%M%S')
                all_keys = request.session.keys()
                if not all_keys:
                    request.session[c_id] = {'good_id': goods_id, 'num': num, 'is_select': 1}
                else:
                    all_count = len(request.session.keys())
                    count = 0
                    for key in all_keys:
                        s_c = request.session.get(key)
                        if s_c.get('good_id') == goods_id:
                            s_c['num'] = s_c['num'] + num
                            request.session[key] = s_c
                            break
                        else:
                            count += 1
                    if count == all_count:
                        request.session[c_id] = {'good_id': goods_id,'num': num,'is_select':1}

                c_count = len(request.session.keys())
                data['c_count'] = c_count
            else:
                data['code'] = 1001
            # 以json格式返回
            return JsonResponse(data)


# 我的购物车
def my_cart(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            is_select_carts = Cart.objects.filter(is_select=1)
            count = is_select_carts.count

            carts = Cart.objects.all()
            moneys = 0
            for cart in is_select_carts:
                moneys += cart.c_prices
            data = {
                'carts': carts,
                'count': count,
                'moneys':round(moneys,3)
            }
            return render(request,'web/cart.html',data)
        else:

            all_key = request.session.keys()
            count = 0
            moneys = 0
            carts = []
            for key in all_key:
                count += 1
                s_cart = request.session.get(key)
                goods = Goods.objects.filter(id=s_cart.get('good_id')).first()
                price = goods.price
                is_select = s_cart.get('is_select')
                c_prices = round(s_cart.get('num') * price, 3)
                moneys += round(s_cart.get('num') * price, 3)
                session_cart = SessionCart(c_id=key, c_num=s_cart.get('num'),goods=goods,
                                           c_prices=c_prices, is_select=is_select)
                carts.append(session_cart)

            data = {
                'moneys': round(moneys),
                'count': count,
                'carts':carts
            }
            return render(request,'web/cart.html', data)



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

# 购物车选择
@csrf_exempt
def is_select(request):
    if request.method == 'POST':
        data = {}
        user = request.user
        # 获取购物车的id
        cart_id = request.POST.get('cart_id')
        if user.id:
            # cart_id = int(request.POST.get('select'))
            cart = Cart.objects.get(id=cart_id)
            # 如果返回的商品的is_select为1,则将其修改为0，如果为0.则将其修改为1，并且将修改后的购物车的总金额统计
            if cart.is_select:
                cart.is_select = 0
                cart.save()
                carts = Cart.objects.filter(is_select=1)
                all_count = carts.count()
                moneys = 0
                for cart in carts:
                    moneys += cart.c_prices
            else:
                cart.is_select = 1
                cart.save()
                # 获取所有被选中的购物车的数量
                carts = Cart.objects.filter(is_select=1)
                all_count = carts.count()
                # 获取所有购物车的总价格
                moneys = 0
                for cart in carts:
                    moneys += cart.c_prices

            data['moneys'] = round(moneys,3)
            data['all_count'] = all_count

            if Cart.objects.filter(is_select=0).exists():
                is_all_select = 0
            else:
                is_all_select = 1

            data['all_select'] = is_all_select

            return JsonResponse(data)
        else:
            is_select_count = 0
            moneys = 0
            # 获取当前点击的购物车
            s_c_cart = request.session.get(cart_id)
            is_select = s_c_cart['is_select']
            # 判断当前购物车的状态，并将其状态修改

            if is_select:
                s_c_cart['is_select'] = 0
                request.session[cart_id] = s_c_cart
            else:
                s_c_cart['is_select'] = 1
                request.session[cart_id] = s_c_cart
            all_keys = request.session.keys()
            all_count = len(all_keys)
            for key in all_keys:
                s_cart = request.session.get(key)
                s_cart_select = s_cart.get('is_select')
                if s_cart_select:
                    price = Goods.objects.filter(id=s_cart.get('good_id')).first().price
                    moneys += price * (s_cart.get('num'))
                    is_select_count += 1
            # 获取所有订单的总价
            data['moneys'] = round(moneys,3)
            # 被选中的全部的数量
            data['all_count'] = is_select_count

            # 判断是否是全部选中状态
            is_all_select = 0
            if is_select_count == all_count:
                is_all_select = 1
            data['all_select'] = is_all_select

            return JsonResponse(data)


# 是否全选
@csrf_exempt
def all_select(request):
    if request.method == 'POST':
        data = {}
        is_all = request.POST.get('is_all')
        moneys = 0
        all_count = 0
        user = request.user
        carts_id = []
        if user.id:
            if is_all == 'true':
                Cart.objects.update(is_select=1)
                carts = Cart.objects.all()
                all_count = carts.count()
                for cart in carts:
                    moneys += cart.c_prices
                f_is_all = 1
            else:
                Cart.objects.update(is_select=0)
                f_is_all = 0
            data['f_is_all'] =f_is_all
            data['moneys'] = round(moneys,3)
            data['all_count'] = all_count

            # 返回全部的购物车数据
            for cart in Cart.objects.all():
                carts_id.append(cart.id)
            data['carts_id'] = carts_id
            return JsonResponse(data)
        else:
            all_key = request.session.keys()
            if is_all == 'true':
                f_is_all = 1
                for key in all_key:
                    s_cart = request.session.get(key)
                    s_cart['is_select'] = 1
                    all_count += 1
                    price = Goods.objects.filter(id=s_cart.get('good_id')).first().price
                    moneys += price * (s_cart.get('num'))
                    s_c_id = int(key)
                    carts_id.append(s_c_id)
                    request.session[key] = s_cart
            else:
                f_is_all = 0
                # 修改购物车选中状态，将所有购物车的id存储
                for key in all_key:
                    s_cart = request.session.get(key)
                    s_cart['is_select'] = 0
                    request.session[key] = s_cart
                    s_c_id = int(key)
                    carts_id.append(s_c_id)

            data['all_count'] = all_count
            data['moneys'] = round(moneys, 3)
            data['f_is_all'] = f_is_all
            data['carts_id'] = carts_id
            return JsonResponse(data)


# 刚进页面的全选状态
def is_all_o(request):
    if request.method == 'GET':
        user = request.user
        if user.id:
            if Cart.objects.filter(user=user, is_select=0).exists():
                status = 0
            else:
                status = 1
            data = {
                'code': 200,
                'msg': '请求成功',
                'status': status
            }
            return JsonResponse(data)
        else:
            is_select_count = 0
            all_keys = request.session.keys()
            all_count = len(all_keys)
            for key in all_keys:
                s_cart = request.session.get(key)
                s_cart_select = s_cart.get('is_select')
                if s_cart_select:
                    is_select_count += 1
            status = 0
            if is_select_count == all_count:
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
        cart_id = request.POST.get('cart_id')
        data = {}
        moneys = 0
        if user.id:
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
            carts = Cart.objects.all()
            for cart in carts:
                moneys += cart.c_prices
            data['moneys'] = round(moneys,3)
            return JsonResponse(data)
        else:
            # 将session中对应的数据的商品加1
            s_c_cart = request.session.get(cart_id)
            s_c_cart['num'] = s_c_cart['num'] + 1
            request.session[cart_id] = s_c_cart
            # 获取增加后的数量
            data['c_num'] = s_c_cart.get('num')
            # 获取商品增加后的金额
            price = Goods.objects.filter(id=s_c_cart.get('good_id')).first().price
            c_prices = price * (s_c_cart.get('num'))
            data['c_prices'] = round(c_prices, 3)
            # 获取增加后所有购物车的总金额

            all_keys = request.session.keys()
            for key in all_keys:
                s_cart = request.session.get(key)
                s_cart_select = s_cart.get('is_select')
                if s_cart_select:
                    price = Goods.objects.filter(id=s_cart.get('good_id')).first().price
                    moneys += price * (s_cart.get('num'))
            data['moneys'] = round(moneys, 3)
            return JsonResponse(data)



# 减少购物车商品
def reduct_good_num(request):
    if request.method == 'POST':
        user = request.user
        data = {}
        moneys = 0
        data['code'] = 200
        data['msg'] = '请求成功'
        cart_id = request.POST.get('cart_id')
        num = int(request.POST.get('num'))
        if user.id:
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

                carts = Cart.objects.all()
                for cart in carts:
                    moneys += cart.c_prices
                data['moneys'] = round(moneys, 3)
                return JsonResponse(data)
            else:
                data['code'] = 1001
                return JsonResponse(data)
        else:
            if num > 1:
                # 将购物车的商品减1
                s_c_cart = request.session.get(cart_id)
                s_c_cart['num'] = s_c_cart['num'] - 1
                request.session[cart_id] = s_c_cart
                # 获取减少后的数量
                data['c_num'] = s_c_cart.get('num')
                # 获取商品减少后的金额
                price = Goods.objects.filter(id=s_c_cart.get('good_id')).first().price
                c_prices = price * (s_c_cart.get('num'))
                data['c_prices'] = round(c_prices, 3)
                # 获取减少后所有购物车的总金额
                all_keys = request.session.keys()
                for key in all_keys:
                    s_cart = request.session.get(key)
                    s_cart_select = s_cart.get('is_select')
                    if s_cart_select:
                        price = Goods.objects.filter(id=s_cart.get('good_id')).first().price
                        moneys += price * (s_cart.get('num'))
                return JsonResponse(data)
            else:
                data['code'] = 1001
                return JsonResponse(data)



# 删除需要删除的购物车信息
def delete_cart(request):

    if request.method == 'POST':
        data = {}
        data['code'] = 200
        data['msg'] = '请求成功'
        cart_id = request.POST.get('cart_id')
        user = request.user
        if user.id:
            Cart.objects.filter(id=cart_id).delete()

            return JsonResponse(data)

        else:
            del request.session[cart_id]
            request.session.modified = True

            return JsonResponse(data)



# 选择订单
def place_order(request):
    if request.method == "GET":
        user = request.user
        if user:
            # 获取用户的购物车信息已经对应的下标
            c_list = []
            carts = Cart.objects.filter(is_select=1,user=user)
            i = 1
            for cart in carts:
                c_list.append([cart, i])
                i += 1
            c_count = Cart.objects.all().count()
            # 获取所有购物车的总金额
            moneys = 0
            for cart in carts:
                moneys += cart.c_prices
            # 获取用户地址
            userinfo = UserReceivInfo.objects.filter(is_select=1).order_by('-sel_time').first()
            if not userinfo:
                userinfo = UserReceivInfo.objects.filter(is_default=1).first()
            if not userinfo:
                userinfo = UserReceivInfo.objects.all().order_by('-add_time').first()

            data = {
                'c_list': c_list,
                'c_count': c_count,
                'moneys':round(moneys,3),
                'userinfo':userinfo

            }

            return render(request, 'web/place_order.html',data)


# 添加订单
def add_order(request):
    if request.method == 'POST':
        user = request.user

        if user:
            zt = int(request.POST.get('zt'))

            # 用户提交订单时选择的地址
            userinfo = UserReceivInfo.objects.filter(is_select=1).order_by('-add_time').first()
            if not userinfo:
                userinfo = UserReceivInfo.objects.filter(is_default=1).first()
            if not userinfo:
                userinfo = UserReceivInfo.objects.all().order_by('-add_time').first()

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

            # 添加订单成功时修改用户选择地址字段，重新让所有的is_select为0，并且让sel_time为空
            UserReceivInfo.objects.update(is_select=0,sel_time=None)

            data = {
                'code':200,
                'msg':'请求成功'
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
            is_count = Order.objects.filter(user=user).count()
            data = {
                'page':page,
                'is_count':is_count,
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


# 用户地址
def user_site(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        userinfos = UserReceivInfo.objects.filter(~Q(is_default=1),user=user).order_by('-add_time')
        if UserReceivInfo.objects.filter(is_default=1,user=user).exists():
            is_default_user = UserReceivInfo.objects.filter(is_default=1).first()
            data['userinfos'] = userinfos
            data['is_default_user'] = is_default_user
        else:
            is_default_user = userinfos.first()
            userinfos =userinfos[1:]

            data['userinfos'] = userinfos
            data['is_default_user'] = is_default_user

        return render(request,'web/user_center_site.html',data)
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('home:user_site'))


# 添加用户地址
def add_address(request):
    if request.method == 'GET':
        is_sel = request.GET.get('is_sel')
        data = {
            'is_sel':is_sel
        }
        return render(request,'web/add_address.html',data)

    if request.method == 'POST':
        user = request.user
        data = {}
        is_sel = request.POST.get('is_sel')
        recipients = request.POST.get('recipients')
        phone = request.POST.get('phone')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        town = request.POST.get('town')
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        is_default = request.POST.get('is_default')
        if len(phone) != 11:
            data['msg'] = '手机号长度有误！'
            return render(request, 'web/add_address.html', data)
        if is_default == 'yes':
            is_default = 1
        else:
            is_default = 0
        if not all([recipients, phone, province, city, county,
                town, address]):
            data['msg'] = '不能为空'
            return render(request,'web/add_address.html', data)
        if not is_default:
            UserReceivInfo.objects.create(name=recipients,phone=phone,province=province,
                                          city=city,county=county,town=town,detail_address=address,
                                          postcode=postcode, is_default=is_default, user=user)
        else:
            UserReceivInfo.objects.filter(is_default=1).update(is_default=0)
            UserReceivInfo.objects.create(name=recipients, phone=phone, province=province,
                                          city=city, county=county, town=town, detail_address=address,
                                          postcode=postcode, is_default=is_default, user=user)
        if is_sel:
            return HttpResponseRedirect(reverse('home:select_address'))
        else:
            return HttpResponseRedirect(reverse('home:user_site'))

# 删除用地址
def delete_address(request):
    if request.method == 'POST':
        data = {
            'code': 200,
            'msg': '请求成功',

        }
        userInfo_id = request.POST.get('userinfo_id')
        UserReceivInfo.objects.filter(id=userInfo_id).delete()
        return JsonResponse(data)


# 修改用户地址
def update_address(request):
    if request.method == 'GET':
        userInfo_id = request.GET.get('userinfo_id')
        userinfo = UserReceivInfo.objects.filter(id=userInfo_id).first()
        data = {
            'userinfo':userinfo
        }

        return render(request,'web/update_address.html',data)
    if request.method == 'POST':
        data = {}
        user = request.user
        is_sel = request.GET.get('is_sel')
        userInfo_id = request.POST.get('id')
        userinfo = UserReceivInfo.objects.filter(id=userInfo_id)
        recipients = request.POST.get('recipients')
        phone = request.POST.get('phone')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        town = request.POST.get('town')
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        is_default = request.POST.get('is_default')
        data['userinfo'] = userinfo.first()
        if len(phone) != 11:
            data['msg'] = '手机号长度有误！'

            return render(request, 'web/update_address.html', data)
        if is_default == 'yes':
            is_default = 1
        else:
            is_default = 0
        if not all([recipients, phone, province, city, county,
                    town, address]):
            data['msg'] = '不能为空'
            return render(request, 'web/update_address.html', data)
        if not is_default:
            userinfo.update(name=recipients, phone=phone, province=province,
                                          city=city, county=county, town=town, detail_address=address,
                                          postcode=postcode, is_default=is_default, user=user)
        else:
            UserReceivInfo.objects.filter(is_default=1).update(is_default=0)
            userinfo.update(name=recipients, phone=phone, province=province,
                                          city=city, county=county, town=town, detail_address=address,
                                          postcode=postcode, is_default=is_default, user=user)
        if is_sel:
            return HttpResponseRedirect(reverse('home:select_address'))
        else:
            return HttpResponseRedirect(reverse('home:user_site'))


# 修改用户信息
def edit_info(request):
    if request.method == 'GET':
        user = request.user
        data = {'user':user}
        return render(request,'web/edit_info.html',data)

    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        adress = request.POST.get('address')
        try:
            if user.userinfo:
                UserInfo.objects.update(user=user, username=name, userphone=phone, useraddress=adress)
        except:
            UserInfo.objects.create(user=user,username=name,userphone=phone,useraddress=adress)

        return HttpResponseRedirect(reverse('home:userInfo'))


# 用户地址选择
def select_address(request):
    if request.method == 'GET':
        user = request.user
        data = {}

        userinfos = UserReceivInfo.objects.filter(~Q(is_default=1), user=user).order_by('-add_time')
        if UserReceivInfo.objects.filter(is_default=1).exists():
            is_default_user = UserReceivInfo.objects.filter(is_default=1).first()
            data['userinfos'] = userinfos
            data['is_default_user'] = is_default_user
        else:
            is_default_user = UserReceivInfo.objects.all().first()
            userinfos = UserReceivInfo.objects.all()[1:]

            data['userinfos'] = userinfos
            data['is_default_user'] = is_default_user

        return render(request, 'web/select_address.html', data)

# 选择地址时修改字段
def update_is_sel_address(request):
    if request.method == 'GET':
        user = request.user
        userinfo_id = request.GET.get('userinfo_id')
        UserReceivInfo.objects.filter(user=user,id=userinfo_id).update(is_select=1,sel_time=datetime.now())

        return HttpResponseRedirect(reverse('home:place_order'))

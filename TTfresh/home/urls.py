from django.conf.urls import url, include

from home import views

urlpatterns = [
    # 主页
    url(r'^index/',views.index,name='index'),
    # 商品列表跳转
    url(r'^list/',views.list,name='list'),
    # 商品列表展示
    # url(r'^list_show/(?P<typeid>\d+)/',views.list_show,name='list_show'),
    # 商品详细信息
    url(r'^detail/',views.detail,name='detail'),
    # 添加商品
    url(r'^add_product/',views.add_product,name='add_product'),
    # 减少商品
    url(r'^reduce_Cart/',views.reduce_Cart,name='reduce_Cart'),
    # 添加订单
    url(r'^add_cart/',views.add_cart,name='add_cart'),
    # 购买
    # url(r'^buy/',views.buy,name='buy'),
    # 购物车
    url(r'^my_cart/',views.my_cart,name='my_cart'),
    # 订单
    url(r'^my_order/',views.my_order,name='my_order'),
    # 购物选择
    url(r'^is_select/',views.is_select,name='is_select'),
    # 是否全选
    url(r'^all_select/',views.all_select,name='all_select'),
    # 刚进页面是否全选
    url(r'^is_all_o/',views.is_all_o,name='is_all_o'),
    # 添加购物车商品
    url(r'^add_goods_num/',views.add_goods_num,name='add_goods_num'),
    # 减少购物车商品
    url(r'^reduct_good_num/',views.reduct_good_num,name='reduct_good_num'),
    # 删除购物车商品
    url(r'^delete_cart/',views.delete_cart,name='delete_cart'),
    # 提交订单
    url(r'^place_order/',views.place_order,name='place_order'),
    # 生成订单
    url(r'^add_order/',views.add_order,name='add_order'),
    # 订单展示
    url(r'^order_show/',views.order_show,name='order_show'),
    # 个人信息
    url(r'^userInfo/',views.userInfo,name='userInfo'),
    # 收货地址
    url(r'^user_site/',views.user_site,name='user_site'),
    # 添加地址
    url(r'^add_address/',views.add_address,name='add_address'),
    # 删除地址
    url(r'^delete_address/',views.delete_address,name='delete_address'),
    # 编辑地址
    url(r'^update_address/',views.update_address,name='update_address'),
    # 编辑用信息
    url(r'^edit_info/',views.edit_info,name='edit_info'),




]

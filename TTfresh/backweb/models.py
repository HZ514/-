from django.db import models

# Create your models here.

from user.models import User, UserReceivInfo


class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # 通用id

    class Meta:
        abstract = True


class MainSide(Main):
    # 幻灯片
    class Meta:
        db_table = 'tt_side'


# 商品分类
class FoodType(models.Model):
    type_img = models.CharField(max_length=200) # 分类图片
    typeid = models.CharField(max_length=16)  # 分类id
    typename = models.CharField(max_length=100,unique=True)  # 商品分类名称

    class Meta:
        db_table = "tt_foodtypes"


# 类型推荐
class TypeRecommend(models.Model):
    recommend_name = models.CharField(max_length=30)
    type_recommend = models.ForeignKey(FoodType)

    class Meta:
        db_table = 'tt_typerecommend'


# 商品
class Goods(models.Model):
    productid = models.CharField(max_length=16,unique=True)  # 商品的id
    productimg = models.CharField(max_length=200)  # 商品的图片
    productname = models.CharField(max_length=100)  # 商品的名称
    pmdesc = models.CharField(max_length=100)  # 商品简介
    is_new = models.BooleanField(default=False)  # 是否是新品
    price = models.FloatField(default=0)  # 价格
    one_weight = models.CharField(max_length=20)  # 商品重量
    detail = models.CharField(max_length=255)  # 商品详情
    goods_type = models.ForeignKey(FoodType)  # 关联类型

    class Meta:
        db_table = "tt_goods"

# # 支付方式
# class Payment(models.Model):
#
#     class Meta:
#          db_table = 'tt_payment'


# 购物车
class Cart(models.Model):
    user = models.ForeignKey(User)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品的个数
    c_prices = models.FloatField(default=0)  # 商品的金额
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'tt_cart'


# 订单
class Order(models.Model):
    userinfo = models.ForeignKey(UserReceivInfo)  # 订单用户信息
    user = models.ForeignKey(User) # 用户
    order_id = models.CharField(max_length=255)
    # 0代表已经下单但是未支付，1代表已经支付待发货，2已经发货
    order_status = models.IntegerField(default=0)  # 订单状态
    order_time = models.DateTimeField(auto_now=True)  # 下单时间
    o_prices = models.FloatField(default=0)  # 订单商品的总金额

    class Meta:
        db_table = 'tt_oder'


class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)  # 关联的商品
    order = models.ForeignKey(Order)  # 关联的订单
    goods_num = models.IntegerField(default=1)  # 商品的个数
    goods_price = models.FloatField(default=0)  # 一种商品的总金额

    class Meta:
        db_table = 'tt_order_goods'


# 用户浏览表
class UserBrowse(models.Model):
    user = models.ForeignKey(User)  # 关联用户
    good = models.ForeignKey(Goods,null=True)  # 关联商品
    browse_time = models.DateTimeField(auto_now=True)  # 浏览时间

    class Meta:
        db_table = 'tt_userbrowse'
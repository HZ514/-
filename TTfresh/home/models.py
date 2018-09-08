from django.db import models

# Create your models here.


# 创建session购物车类
class SessionCart(object):

    def __init__(self, c_id, c_num, goods, c_prices,is_select):
        self.id = c_id
        self.c_num = c_num
        self.goods = goods
        self.c_prices = c_prices
        self.is_select = is_select

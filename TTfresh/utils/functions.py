import random

from datetime import datetime


def get_order_number():
    s='1237979823423453'
    o_num = ''
    for i in range(10):
        o_num += random.choice(s)
    o_num += datetime.now().strftime('%Y%m%d%H%M%S')
    return o_num
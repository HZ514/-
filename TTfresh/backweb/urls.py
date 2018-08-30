from django.conf.urls import url, include

from backweb import views

urlpatterns = [
    url(r'^login/',views.login,name='login'),
    url(r'^logout/',views.logout,name='logout'),
    url(r'^index/',views.index,name='index'),
    url(r'^update_postwd/',views.update_postwd,name='update_postwd'),
    url(r'^listUser/',views.listUser,name='listUser'),
    url(r'^add_side/',views.add_side,name='add_side'),
    # 添加分类
    url(r'^add_type/',views.add_type,name='add_type'),
    # 分类管理
    url(r'^type_manage/',views.type_manage,name='type_manage'),
    # 删除商品
    url(r'^product_delete/',views.product_delete,name='product_delete'),
    # 编辑分类
    url(r'^editor_type/',views.editor_type,name='editor_type'),
    # 添加商品
    url(r'^add_product/',views.add_product,name='add_product'),
    # 编辑商品
    url(r'^editor_good/',views.editor_good,name='editor'),

]

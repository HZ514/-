from django.conf.urls import url, include

from backweb import views

urlpatterns = [
    url(r'^login/$',views.login,name='login'),
    url(r'^logout/$',views.logout,name='logout'),
    # 商品展示
    url(r'^index/$',views.index,name='index'),
    url(r'^update_postwd/$',views.update_postwd,name='update_postwd'),
    url(r'^listUser/$',views.listUser,name='listUser'),
    url(r'^add_side/$',views.add_side,name='add_side'),
    # 添加分类
    url(r'^add_type/$',views.add_type,name='add_type'),
    # 删除分类
    url(r'^delete_type/(\d+)', views.delete_type, name='delete_type'),
    # 编辑分类
    url(r'^editor_type/$', views.editor_type, name='editor_type'),
    # 分类分页展示
    url(r'^manage_type/$',views.manage_type,name='manage_type'),

    # 添加商品
    url(r'^add_product/$', views.add_product, name='add_product'),
    # 删除商品
    url(r'^good_delete/(\d+)/$',views.good_delete,name='good_delete'),
    # 编辑商品
    url(r'^good_editor/(\d+)/$',views.good_editor,name='good_editor'),
    # 商品查询

    # 幻灯片商品展示
    url(r'^slide_list/',views.slide_list,name='slide_list'),
    # 删除幻灯片
    url(r'^del_side/(\d+)',views.del_side,name='del_side'),
    # 编辑幻灯片
    url(r'^editor_side/',views.editor_side,name='editor_side'),




]

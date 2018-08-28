// 添加商品
function add_product(good_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    var num =  $('#num_'+good_id).val()
    $.ajax({
        url:'/home/add_product/',
        type:'POST',
        dataType:'json',
        data:{'goods_id':good_id,'num':num},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
        console.log(data)
            $('#num_'+good_id).val(data.data.c_num)
            $('.total').html('总价：<em>' + data.data.prices + '元</em>')
        },
        error:function(data){
            location.href = '/users/login/'
        }
    })
}

// 减少商品
function reduce_product(good_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    var num =  $('#num_'+good_id).val()
    $.ajax({
        url:'/home/reduce_Cart/',
        type:'POST',
        dataType:'json',
        data:{'goods_id':good_id,'num':num},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
           console.log(data)
            if(data.code == 200){
                $('#num_'+good_id).val(data.c_num)
                $('.total').html('总价：<em>' + data.prices + '元</em>')

                }
            },
        error:function(data){
            location.href = '/users/login/'
        }
    })
}

//添加购物车
function add_cart(good_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    var num =  $('#num_'+good_id).val()
    $.ajax({
        url:'/home/add_cart/',
        type:'POST',
        dataType:'json',
        data:{'goods_id':good_id,'num':num},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
           console.log(data)
            if(data.code == 200){
                $('#show_count').html(data.c_count);
                }
            },
        error:function(data){
            alert('请求失败')
        }
    })
}


// 是否选择
function is_selcet(cart_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    var cart_id =  $('.is_'+cart_id).val()
    console.log($('.is_'+cart_id).prop("checked"))
    if ($('.is_'+cart_id).prop("checked")){
        var select = 1
    }else{
        var select = 0
    }
    console.log(select)
    console.log(cart_id)
    $.ajax({
        url:'/home/is_select/',
        type:'POST',
        dataType:'json',
        data:{'cart_id':cart_id,'select':select},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
           console.log(data)
           if (data.all_select){
               $('.is_all')[0].checked = true
               $('#moneys').html(data.moneys)
               $('#all_count').text(data.all_count)
           }else{
               $('.is_all')[0].checked = false
               $('#moneys').html(data.moneys)
               $('#all_count').text(data.all_count)
           }

            },
        error:function(data){
            alert('请求失败')
        }
    })
}

// 是否全选
function all_select(){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    var is_all =  $('.is_all').prop("checked")
    console.log(is_all)
    $.ajax({
        url:'/home/all_select/',
        type:'POST',
        dataType:'json',
        data:{'is_all':is_all},
        headers:{'X-CSRFToken':csrf},
        success:function(data){

                if (data.f_is_all){
                    for (var i = 0; i < data.carts_id.length; i++){

                        $('.is_' + data.carts_id[i])[0].checked = true
                    }
                }else{
                    for (var i = 0; i < data.carts_id.length; i++){
                        $('.is_' + data.carts_id[i])[0].checked = false
                    }
                }
            },
        error:function(data){
            alert('请求失败')
        }
    })
}


// 添加购物车商品
function add_goods_num(cart_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        url:'/home/add_goods_num/',
        type:'POST',
        dataType:'json',
        data:{'cart_id':cart_id},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
        console.log(data)
             $('#c_d_' + cart_id).val(data.c_num)
             $('#moneys').html(data.moneys)
             $('#c_price_' + cart_id).html(data.c_prices + '元')
        },
        error:function(data){
            alert('请求失败')
        }
    })
}

// 减少购物车商品
function reduct_good_num(cart_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    var num =   $('#c_d_' + cart_id).val()
    $.ajax({
        url:'/home/reduct_good_num/',
        type:'POST',
        dataType:'json',
        data:{'cart_id':cart_id,'num':num},
        headers:{'X-CSRFToken':csrf},
        success:function(data){
            if (data.code == '200'){
                $('#c_d_' + cart_id).val(data.c_num)
                $('#moneys').html(data.moneys)
                $('#c_price_' + cart_id).html(data.c_prices + '元')
            }

            },
        error:function(data){
            alert('请求失败')
        }
    })
}


// 删除购物车商品
function delete_cart(cart_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/home/delete_cart/',
        type:'POST',
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        data:{'cart_id':cart_id},
        success:function(){
            console.log('请求成功')
        },
        error:function(){

        },
    })
    $('#cart_' + cart_id).remove()
}

//
//// 提交订单
//function place_oder(){
//
//    $.ajax({
//        url:'/home/place_oder/',
//        type:'GET',
//        dataType:'json',
//
//        data:{},
//        success:function(){
//            console.log('请求成功')
//        },
//        error:function(){
//
//        },
//    })
//    $('#cart_' + cart_id).remove()
//}








//物品金额
function goods_count(){
    $.get('/home/goods_count/',function(data){

        if (data.code == '200'){
            $('.total').html('总价'+data.sum_money)
        }
    })
}



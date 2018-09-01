function select_goods(){
    type = $('.select').val()
    context = $('#context').val()
    location.href = '/backweb/select_goods/'+type+'/?'+'cotext='+context+'/'
}



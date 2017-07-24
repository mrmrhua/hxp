$(document).ready(function () {
     $.ajax({
        url:"api/v1.0/randomtoken",
        type:"GET",
        dataType:'json',
        success:function(result){
            var state =  result['state'];
            // var callback_url = 'http://127.0.0.1%3a5000/login';
            $("input[name='_csrf_token']").val( state );
            // re_url = 'https://open.weixin.qq.com/connect/qrconnect?appid=wxbfacdb1b99885182&redirect_uri='+callback_url+'&response_type=code&scope=snsapi_login&state='+ state +'#wechat_redirect';
            re_url = '/login';
            $("#wxlogin").attr('href',re_url);
        }
    })
})
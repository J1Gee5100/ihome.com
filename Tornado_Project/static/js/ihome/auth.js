function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}
function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
$("#form-auth").submit(function(e){
    e.preventDefault();
    auth_name = $("#real-name").val();
    idcardnum = $("#id-card").val();
    if (!auth_name || !idcardnum) {
        $(".error-msg").html("请填写正确的用户信息！");
        $(".error-msg").show();
        return;
    }
    var data ={
        auth_name:auth_name,
        idcardnum:idcardnum,
    };
    $.ajax({
        url:"/api/profile/auth",
        type:"post",
        data: JSON.stringify(data),
        contentType:"application/json",
        dataType:"json",
        headers:{
        "X-XSRFTOKEN":getCookie("_xsrf"),
        },
        success:function(data){
            if("0" == data.errno){
                $(".error-msg").html(data.errmsg);
                $(".error-msg").hide()
                showSuccessMsg();
                setTimeout(function () {
                    location.href = "/my.html";
                },2000)
                return;
            }
            else {
                $(".error-msg").html(data.errmsg);
                $(".error-msg").show();
                return;
            }
        }
    })
});
$(document).ready(function(){
    $.get("/api/profile/auth", function(data) {
        if ("0" == data.errno) {
            if (!data.data.name) {
            }
            else {
                $("#real-name").val(data.data.name);    
                $("#real-name").attr("disabled",true);
                $("#id-card").val(data.data.idcard);
                $("#id-card").attr("disabled",true);
                $("#btn-success").attr("disabled",true);
            }
            
        }
        else {
            location.href = "/";
        }
    }, "json");
})
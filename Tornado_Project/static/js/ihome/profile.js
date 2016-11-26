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

$(document).ready(function(){
    $.get("/api/profile", function(data){
        if ("4101" == data.errno) {
            location.href = "/login.html";
        }
        else if ("0" == data.errno) {
            $("#user-name").val(data.data.name);
            if (data.data.avatar) {
                $("#user-avatar").attr("src", data.data.avatar);
            }
        }
    })
    $("#form-name").submit(function(e){
        e.preventDefault();
        name = $("#user-name").val();
        if (!name) {
            $(".error-msg").html("请填写正确的用户名！");
            $(".error-msg").show();
            return;
        }
        var data ={
            name:name,
        };
        $.ajax({
            url:"/api/profile/name",
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
                    $(".error-msg").hide();
                    showSuccessMsg();
                    return;
                }
                else {
                    $(".error-msg").html("用户名已存在，请重新设置");
                    $(".error-msg").show();
                    return;
                }
            }
        })
    });
    $(document).ready(function(){
        //上传头像
        $("#form-avatar").submit(function(e){
            e.preventDefault();
            $('.image_uploading').fadeIn('fast');
            var options = {
                url:"/api/profile/avatar",
                type:"POST",
                headers:{
                    "X-XSRFTOKEN":getCookie("_xsrf"),
                },
                success: function(data){
                    if ("0" == data.errno) {
                        $('.image_uploading').fadeOut('fast');
                        $("#user-avatar").attr("src", data.url);
                    }
                }
            };
            $(this).ajaxSubmit(options);
        });
    })
})

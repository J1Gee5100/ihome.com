$(document).ready(function(){
    $.get("/api/myhouse", function(data) {
        if ("0" == data.errno ){
            if (null == data.data.name){
            $(".auth-warn").show();
            }
                // $(".auth-warn").hide()
            // $("#user-mobile").text(data.data.mobile);
            // $("#user-avatar").attr("src",data.data.avatar);
        } else{
            location.href = "/";
        }
    }, "json");
    
})
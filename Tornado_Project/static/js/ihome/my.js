function logout() {
    $.get("/api/logout", function(data){
        if ("0" == data.errno) {
            location.href = "/";
        }
    })
}


$(document).ready(function(){
    $.get("/api/profile", function(data) {
        if ("0" == data.errno){
            $("#user-name").html(data.data.name);
            $("#user-mobile").text(data.data.mobile);
            $("#user-avatar").attr("src",data.data.avatar);
        } else {
            location.href = "/";
        }
    }, "json");
});

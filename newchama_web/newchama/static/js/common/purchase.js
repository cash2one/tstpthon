
function addDestIndustry() {
    var id = jQuery("#industry_id").val();
    var name = jQuery("#industry_name").val();
    if (id == "0" || id == "") return;
    if (!isObjectExsit("dest_industry_" + id)) {
        var html = "<span id='dest_industry_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='industry' type='hidden' value='" + id + "'></span>";
        jQuery("#dest_industry").append(html);
    }
}

function addDestLocation() {
    var id = jQuery("#dest_country").val();
    var name = jQuery("#dest_country option:selected").text();
    if (id == "0" || id == "") return;
    if (!isObjectExsit("dest_country_" + id)) {
        var html = "<span id='dest_country_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='country' type='hidden' value='" + id + "'></span>";
        jQuery("#dest_location").append(html);
    }
}

$("#btn_go_list").click(function() {
    var is_pass = checkMustEnter(0);
    var is_pass_2 = true;
    if ($("#project_keyword").val() == "") {
        var custom_error = '<ul id="' + custom_1 + '" class="parsley-error-list" style="display: block;"><li class="custom-error-message" style="display: list-item;">请填写关键字</li></ul>';
        if ($("#" + custom_1).length == 0)
            $("#key_keyword").after(custom_error);
        is_pass_2 = false;
    }
    else {
        if ($("#" + custom_1).length > 0)
            $("#" + custom_1).remove();
        is_pass_2 = true;
    }
    if (!is_pass || !is_pass_2) return;
    $("#submitStatus").val("pending");
    $(this).prop("disabled", true);
    endSave(function(bool) {
        $("#btn_go_list").prop("disabled", false);
        if (bool) {
            var loadi = layer.load('正在为您匹配最适合您的项目信息，请耐心等待');
            var editid = $("#edit_id").val();
            if (editid == "") return;
            var url = "/purchase/sync_recommond";
            jQuery.post(url,
                {id:editid}, function(data) {
                    if (data == "success") {
                        location.href="/purchase/banking_genius/" + editid;
                    }
                    layer.close(loadi);
            });
        }
    });
});

$("#btn_save").click(function() {
    if (!checkMustEnter(0)) {
        return;
    }
    if (!checkProjectStage()) return;
    $("#submitStatus").val("pending");
    $(this).prop("disabled", true);
    endSave(function(bool) {
        $("#btn_save").prop("disabled", false);
        if (bool) {
            location.href="/purchase/mylists";
        }
    });
});

$("#intro_cn_").keyup(function() {
    var val = $(this).val();
    $("#intro_cn").val(val.replace(/\n/g, "<br/>"));
});

$("#intro_en_").keyup(function() {
    var val = $(this).val();
    $("#intro_en").val(val.replace(/\n/g, "<br/>"));
});
/*
    $("#newStatus_" + ref).attr("disabled", true);
    if (val == "favorite") {
        var url = "/account/add_project_to_favorite";
        $.post(url,{id:ref},function(data) {
            switch (data) {
                case "success":
                    obj.find("option:selected").remove();
                    obj.append("<option value='cancelFavorite'>取消关注</option>");
                    break;
                default :
                    break;
            }
            $("#newStatus_" + ref).attr("disabled", false);
        });
    }
    else if (val == "cancelFavorite") {
        var url = "/account/remove_project_from_favorite";
        $.post(url,{id:ref},function(data) {
            switch (data) {
                case "success":
                    obj.find("option:selected").remove();
                    obj.append("<option value='favorite'>关注</option>");
                    break;
                default :
                    break;
            }
            $("#newStatus_" + ref).attr("disabled", false);
        });
    }
*/
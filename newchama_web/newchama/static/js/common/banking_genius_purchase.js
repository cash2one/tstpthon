
var page = 1;

function loadRecommend() {
    var target_location_id = $("#target_location_id").val();
    var target_industry_id = $("#target_industry_id").val();
    var target_location_Type = $("#target_location_Type").val();
    $(".view-more-recommond_1").addClass("hide_");
    $(".assist_loading").removeClass("hide_");
    page ++;
    var pagesize = 10;
    var url = "/purchase/json_recommend";
    var id = $("#edit_id").val();
    jQuery.post(url,{id:id, page:page, pagesize:pagesize,
        target_location_id:target_location_id, target_industry_id:target_industry_id,
        target_location_Type:target_location_Type},
        function(data) {
            var newData = data.replace(/\s/g,'');
            if(newData) {
                $(".table_recommend_1").children().last().after(data);
                $(".assist_loading").addClass("hide_");
                $(".view-more-recommond_1").removeClass("hide_");
            }
            else {
                var html = '<tr class="noMoreshow_1"><td colspan="6" align="center">暂无相关推荐</td></tr>';
                $(".table_recommend_1").children().last().after(html);
                $(".assist_loading").addClass("hide_");
            }
    });
}

function loadPotentialCount() {
    var target_location_id = $("#target_location_id").val();
    var target_industry_id = $("#target_industry_id").val();
    var target_location_Type = $("#target_location_Type").val();
    if (target_location_id == "0" && target_industry_id == "0") return;
    var url = "/purchase/json_recommend_count";
    var id = $("#edit_id").val();
    jQuery.post(url, {id:id, target_location_id:target_location_id, target_industry_id:target_industry_id,
        target_location_Type:target_location_Type},
        function(data) {
            $(".potentialNum").html(data);
    });
}

jQuery('#target_company_industry_0').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#target_company_industry_0 option:selected").text();
    jQuery("#target_industry_id").val(val);
    jQuery("#target_industry_name").val(name);
    jQuery("#target_company_industry_1").parent().hide();
    jQuery("#target_company_industry_2").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("target_company_industry_1", val);
});

jQuery('#target_company_industry_1').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#target_company_industry_1 option:selected").text();
    jQuery("#target_industry_id").val(val);
    jQuery("#target_industry_name").val(name);
    jQuery("#target_company_industry_2").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("target_company_industry_2", val);
});

jQuery('#target_company_industry_2').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#target_company_industry_2 option:selected").text();
    jQuery("#target_industry_id").val(val);
    jQuery("#target_industry_name").val(name);
});

jQuery("#target_country").change(function(){
    var val = jQuery(this).val();
    LoadProvinces('target_province',jQuery(this).val(),0);
    $("#target_location_id").val(val);
});

jQuery("#target_province").change(function(){
    var val = jQuery(this).val();
    $("#target_location_type").val("province");
    $("#target_location_id").val(val);
});

$("#btn_search").click(function() {
    var target_location_id = $("#target_location_id").val();
    var target_industry_id = $("#target_industry_id").val();
    var target_location_Type = $("#target_location_Type").val();
    if (target_location_id == "0" && target_industry_id == "0") return;
    $(".table_recommend_1 tr").not(":first").remove();

    page = 0;
    loadPotentialCount();
    loadRecommend();
})

$("#btn_review").click(function() {
    var editid = $("#edit_id").val();
    var url = "/purchase/detail/" + editid + "/?type=1";
    pageDetail = $.layer({
        type: 2,
        border: [0],
        title: false,
        fix: false,
        closeBtn:[0, true],
        iframe: {src : url, scrolling: 'no'},
        area: ['1000px', '670px']
    });
    $(".xubox_layer").css("top", "50px");
});

$(".panel-body").delegate(".newStatus","change",function(){
    var val = $(this).val();
    var ref = $(this).attr("ref");
    var obj = $(this);
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
    else if (val == "detail") {
        location.href = "/sales/detail/" + ref + "/";
    }
    else if (val == "message") {
        var recipientType = $("#recipientType").val()
        show_sendmessage(recipientType, ref, "", "");
        $("#newStatus_" + ref).attr("disabled", false);
    }

});
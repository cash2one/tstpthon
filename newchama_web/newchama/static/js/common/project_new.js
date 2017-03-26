page = 1;
function loadData() {
    $("#load_btn").hide();
    $("#loader").show();
    $(".no_record").remove();
    page++;
    var pagesize=10;
    $("#no_more_div").remove();
    var keywords = $("#keywords").val();
    var country_id = $("#country").val();
    var province_id = $("#province").val();
    var industry_id = $("#industry_id").val();
    var subscribe_id = $("#subscribe_id").val();
    var sort = $("#newSort").val();

    var url = "/sales/ajax_more";
    $.get(url,
        {page:page, pagesize:pagesize, sort:sort, subscribe_id:subscribe_id,
        country_id:country_id, province_id:province_id, industry_id:industry_id, keywords:keywords},
        function (data) {
            var newData = data.replace(/\s/g,'');
            $("#loader").before(data);
            if ($("#no_more_div").length > 0) {
            	if (page == 1) {
	                var html = '<li class="news-list-view-all no_record" style="line-height:30px;">暂无推荐项目</li>';
	                $("#loader").before(html);
                }
                $("#loader").hide();
            }
            else {
                $("#loader").hide();
                var have_more_data = $("#have_more_data").length;
                if (have_more_data > 0)
                    $("#load_btn").show();
            }
            $("#no_more_div").remove();
            $("#have_more_data").remove();
    });
}
//inital list data
$("#no_more_div").remove();
$("#have_more_data").remove();

$("#btn_search").click(function() {
    $(".news-list .project-item").remove();
    page = 0;
    $("#subscribe_id").val(0);
    loadData();
});

$("#newSort").change(function() {
    $(".news-list .project-item").remove();
    page = 0;
    loadData();
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
        obj.val("");
        location.href = "/sales/detail/" + ref + "/";
    }
    else if (val == "message") {
        var recipientType = $("#recipientType").val();
        obj.val("");
        show_sendmessage(recipientType, ref, "", "");
        $("#newStatus_" + ref).attr("disabled", false);
    }

});

jQuery('#company_industry_0').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_0 option:selected").text();
    jQuery("#company_industry_1").parent().hide();
    jQuery("#company_industry_2").parent().hide();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
    if (val == "0" || val == "") return;
    industrySelect("company_industry_1", val);
});

jQuery('#company_industry_1').change(function() {
    var val = jQuery(this).val();
    if (val == "0" || val == "") {
        val = jQuery('#company_industry_0').val();
        jQuery("#industry_id").val(val);
        return;
    }
    var name = jQuery("#company_industry_1 option:selected").text();
    jQuery("#company_industry_2").parent().hide();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
    industrySelect("company_industry_2", val);
});

jQuery('#company_industry_2').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#target_company_industry_2 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
});

jQuery("#country").change(function(){
    var val = jQuery(this).val();
    LoadProvinces('province',jQuery(this).val(),0);
    $("#location_type").val("province");
    $("#location_id").val(val);
});

jQuery("#target_province").change(function(){
    var val = jQuery(this).val();
    $("#location_type").val("province");
    $("#location_id").val(val);
});

jQuery(".subscribe").click(function() {
    $(".news-list .project-item").remove();
    $("#subscribe_id").val($(this).attr("ref"));
    page = 0;
    loadData();
});

jQuery("#btn_create").click(function() {
    location.href="/subscribe/add";
})

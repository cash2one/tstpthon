
function goback() {
    history.back();
}

var preUrl = document.referrer;

function custom_alert(message, title) {
    if (typeof(title) == "undefined") title = "New Message";
    bootbox.dialog({
        message: message,
        title: title,
        buttons: {
            main: {
                label: "Confirm",
                className: "btn-primary"
            }
        }
    });
}

function custom_confirm(message, title, fun_) {
    if (typeof(title) == "undefined" || title == "") title = "New Message";
    bootbox.dialog({
        message: message,
        title: title,
        buttons: {
            success: {
                label: "Cancel",
                className: "btn-default"
            },
            main: {
                label: "Confirm",
                className: "btn-primary",
                callback: function() {
                    fun_();
                }
            }
        }
    });
}

function custom_fill_confirm(message, title, fun_) {
    if (typeof(title) == "undefined" || title == "") title = "New Message";
    bootbox.dialog({
        message: message,
        title: title,
        buttons: {
            success: {
                label: "Sontinue",
                className: "btn-primary"
            },
            main: {
                label: "Skip",
                className: "btn-default",
                callback: function() {
                    fun_();
                }
            }
        }
    });
}

function DoDelete(url, id) {
    if (confirm("Are you confirm remove this information?")) {
        jQuery.post(
            url, {id:id},
            function (msg) {
                if (msg == "success") {
                    custom_alert("Operation success!")
                    location.reload();
                }
                else
                    custom_alert(msg);
            },
            "text"
        );
    }
}

function LoadProvinces(element,country_id,value)
    {
        if(country_id>0 && country_id != "")
        {
            var is_chinese =(get_template_lang() == "zh-cn");
            jQuery("#box_"+element).hide();
            jQuery("#"+element).empty();
            jQuery("#"+element).append("<option value='0'>Loading...</option>");
            jQuery("#"+element).trigger("chosen:updated");
            var url = "/services/get_provinces/"+country_id;
            jQuery.getJSON(url,function(data)
            {
                jQuery("#"+element).empty();
                if (is_chinese) {
                    jQuery("#"+element).append("<option value='0'>请选择</option>");
                }else{
                    jQuery("#"+element).append("<option value='0'>Please Select</option>");
                }
                var count = data.length;
                if(count>0)
                {
                    jQuery("#box_"+element).show();

                    for(var k in data)
                    {
                        var id = data[k].pk;
                        var name_en = data[k].fields.name_en;
                        var name_cn =  data[k].fields.name_cn;
                        var name = name_en;
                        if (is_chinese&&name_cn!="")
                        {
                            name = name_cn;
                        }
                        //console.log(id);
                        //console.log(name);
                        if (id == value) {
                            jQuery("#"+element).append("<option value='" + id + "' selected=\"selected\">" + name + "</option>");
                        } else {
                            jQuery("#"+element).append("<option value='" + id + "'>" + name + "</option>");
                        }
                    }
                }
                jQuery("#"+element).trigger("chosen:updated");
            });
        }
    }
function LoadCities(element,province_id,value)
    {
        if(province_id>0 && province_id != "")
        {
            var is_chinese =(get_template_lang() == "zh-cn");
            jQuery("#box_"+element).hide();
            jQuery("#"+element).empty();
            jQuery("#"+element).append("<option value='0'>Loading...</option>");
            jQuery("#"+element).trigger("chosen:updated");
            var url = "/services/get_cities/"+province_id;
            jQuery.getJSON(url,function(data)
            {
                jQuery("#" + element).empty();
                if (is_chinese) {
                    jQuery("#"+element).append("<option value='0'>请选择</option>");
                }else{
                    jQuery("#"+element).append("<option value='0'>Please Select</option>");
                }
                var count = data.length;
                if(count>0) {
                    jQuery("#box_"+element).show();

                    for (var k in data) {
                        var id = data[k].pk;
                        var name_en = data[k].fields.name_en;
                        var name_cn =  data[k].fields.name_cn;
                        var name = name_en;
                        if (is_chinese&&name_cn!="")
                        {
                            name = name_cn;
                        }
                        //console.log(id);
                        //console.log(name);
                        if (id == value) {
                            jQuery("#" + element).append("<option value='" + id + "' selected=\"selected\">" + name + "</option>");
                        } else {
                            jQuery("#" + element).append("<option value='" + id + "'>" + name + "</option>");
                        }
                    }
                }
                jQuery("#" + element).trigger("chosen:updated");
            });
        }
    }
/*
function LoadProvinces(country_id,value) {
    if(country_id>0 && country_id != "")
    {
        jQuery("#province").empty();
        jQuery("#province").append("<option value='0'>Loading...</option>");
        jQuery("#province").trigger("chosen:updated");
        var url = "/services/get_provinces/"+country_id;
        jQuery.getJSON(url,function(data)
        {
            jQuery("#province").empty();
            if (get_template_lang() == "zh-cn")
                jQuery("#province").append("<option value='0'>请选择</option>");
            else
                jQuery("#province").append("<option value='0'>Please Select</option>");
            for(k in data)
            {
                var id = data[k].pk;
                var name = "";
                if (get_template_lang() == "zh-cn")
                    name = data[k].fields.name_cn;
                else
                    name = data[k].fields.name_en;
                if (id == value) {
                    jQuery("#province").append("<option value='" + id + "' selected=\"selected\">" + name + "</option>");
                } else {
                    jQuery("#province").append("<option value='" + id + "'>" + name + "</option>");
                }
            }
            //jQuery("#province").chosen({'width':'100%','white-space':'nowrap'});
            jQuery("#province").trigger("chosen:updated");
        });
    }
}
*/
function RemoveCompanyFile(id) {
    if(confirm('Are you confirm remove this file?'))
    {
        var url = "/member/companies/remove_file";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                custom_alert(data);
            }
        });

    }
}

function RemoveCompanyLogo(id)
{
    if(confirm('Are you confirm remove this file?'))
    {
        var url = "/member/companies/remove_logo";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                custom_alert(data);
            }
        });
    }
}

function RemoveProjectFile(id) {
    if(confirm('Are you confirm remove this file?')) {
        var url = "/sales/removeFile";
        jQuery.post(url,{id:id},function(data){
            if (data == "success") {
               location.reload();
            }
            else {
                custom_alert(data);
            }
        });
    }
}

function industrySelect(selectId, parentId, fun_) {
    //selected value
    var value_selected = arguments[2];
    //var url = "{% url 'industry.json' 0 %}";
    var is_chinese = (get_template_lang() == "zh-cn");
    jQuery("#" + selectId).empty();
    jQuery("#" + selectId).append("<option value='0'>Loading...</option>");
    jQuery("#" + selectId).trigger("chosen:updated");
    var url = "/services/get_industrys/" + parentId;
    var opt = "";
    jQuery.getJSON(url, function(data) {
        if (data.length > 0) {
//            if (jQuery("#" + selectId).parent().is(":hidden"))
                jQuery("#" + selectId).parent().show();
//            else
                //jQuery("#" + selectId).parent().parent().show();
        }
        jQuery("#" + selectId).empty();
        if (is_chinese) {
            jQuery("#" + selectId).append("<option value='0'>选择行业</option>");
        }
        else {
            jQuery("#" + selectId).append("<option value='0'>Please Select</option>");
        }
        jQuery.each(data, function(key, value) {
            var name_en = value.fields.name_en;
            var name_cn = value.fields.name_cn;
            var name = name_en;
            if (is_chinese && name_cn!="") {
                name = name_cn;
            }
            //selected value
            if(value.pk == value_selected) {
               opt += "<option value='" + value.pk + "' selected>"+name+"</option>";
            }
            else {
                opt += "<option value='" + value.pk + "'>"+name+"</option>";
            }
        });
        jQuery("#" + selectId).append(opt);
        jQuery("#" + selectId).trigger("chosen:updated");
        try {
            fun_();
        } catch (e){}
    });
}

/*function addIndustry(id, pre) {
    var tagId = pre + "company_industry_id";
    var tagName = pre + "company_industry_name";
    var tagCls = pre + "company_industry_class";
    var tagInsert = pre + "company_industry";
    var val = jQuery("#" + id).val();

    if (!isCustomerExsit(val, pre)) {
        var name = jQuery("#" + id + " option:selected").text();
        var html = "<span><input name='" + tagId + "' class='" + tagCls + "' type='hidden' value='" + val +
                "'/>" + name + "<a class='customClose'></a></span>";

        jQuery("#" + tagInsert).append(html);
    }
}*/

function isCustomerExsit(val, pre) {
    if (val == "0") return true;
    var bool = false;
    var checkCls = pre + "company_industry_class";
    jQuery("." + checkCls).each(function() {
       if (this.value == val) {
           bool = true;
           return false;
       }
    });
    return bool;
}

function autoSlider(id, min, max) {
    var unit = "M";
	$( "#rangeSlider" + id ).slider({
		range: true,
		min: 0,
		max: 100000,
        step:100,
		values: [ min, max ],
		slide: function( event, ui ) {
            var minVal = ui.values[ 0 ];
            var maxVal = ui.values[ 1 ];
            $("#member_range_mins_" + id).val(minVal * 10000);
            $("#member_range_maxs_" + id).val(maxVal * 10000);
            minVal = transfer2Currency(minVal);
            maxVal = transfer2Currency(maxVal);
			$("#amount" + id ).text ( "" + minVal + unit + " - " + maxVal + unit );
		}
	});
	$( "#amount" +id ).text( transfer2Currency(min) + unit + " - " + transfer2Currency(max) + unit);
}

function transfer2Currency(num) {
    var val = num + "";
    var reverseVal = "";
    var j = 0;
    var len = val.length;
    for (var i = len; i > 0; i --) {
        reverseVal = val.substring(i - 1, i) + reverseVal;
        j ++;
        if (j % 3 == 0 && j < len) reverseVal = "," + reverseVal;
    }
    return reverseVal;
//    var val = num;
//    return val.split('').reverse().join('').replace(/(\d{3}(?=\d)(?!\d+\.|$))/g, '$1,').split('').reverse().join('');
}

function changecss() {
    $('.table-striped tr').hover(function () {
        $(this).addClass("custom_select");
    }, function () {
        $(this).removeClass("custom_select");
    });
}

function DeleteDemand(id)
{
    custom_confirm("Are you sure you want to delete?", "New Message", function() {
        var url = "/purchase/delete";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
                //location.reload();
                if (preUrl != "")
                    location.href = preUrl;
                else
                    location.href = "/purchase/mylists";
            }else
            {
                custom_alert(data);
            }
        });
    });
}
function OfflineDemand(id)
{
    custom_confirm("Are you sure you want to get it off the market?", "New Message", function() {
        var url = "/purchase/offline";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
                location.reload();
            }else
            {
                custom_alert(data);
            }
        });
    });
}

function DeleteSales(id)
{
    custom_confirm("Are you sure you want to delete?", "New Message", function() {
        var url = "/sales/delete";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
                if (preUrl != "")
                    location.href = preUrl;
                else
                    location.href = "/sales/mylist";
            }else
            {
                custom_alert(data);
            }
        });
    });
}
function OfflineSales(id)
{
    custom_confirm("Are you sure you want to get it off the market?", "New Message", function() {
        var url = "/sales/offline";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
                location.reload();
            }else
            {
                custom_alert(data);
            }
        });
    });
}

$(".slider-tag").click(function() {
    var index = $(".slider-tag").index($(this));
    $(".slider-hide").eq(index).slideToggle();
    if ($(this).hasClass("glyphicon-chevron-down")) {
        $(this).removeClass("glyphicon-chevron-down");
        $(this).addClass("glyphicon-chevron-up");
    }
    else {
        $(this).removeClass("glyphicon-chevron-up");
        $(this).addClass("glyphicon-chevron-down");
    }
});

$(".glyphicon-cog-tag").click(function() {
    var index = $(".glyphicon-cog-tag").index($(this));
    $(".glyphicon-cog-hide").eq(index).slideToggle();
});


$(".glyphicon-plus-tag").click(function() {
    var index = $(".glyphicon-plus-tag").index($(this));
    $(".glyphicon-plus-hide").eq(index).slideToggle();
    if ($(this).hasClass("glyphicon-minus")) {
        $(this).removeClass("glyphicon-minus");
        $(this).addClass("glyphicon-plus");
    }
    else {
        $(this).removeClass("glyphicon-plus");
        $(this).addClass("glyphicon-minus");
    }
});
function GetAddFavoriteUrl(type)
{
    var url = "";
    switch (type){
        case "project":
            url = "/account/add_project_to_favorite";
            break;
        case "demand":
            url = "/account/add_demand_to_favorite";
            break;
         case "company":
            url = "/account/add_company_to_favorite";
            break;
        case "member":
            url = "/account/add_member_to_favorite";
            break;
         case "data":
            url = "/account/add_data_to_favorite";
            break;
        case "news":
            url = "/account/add_news_to_favorite";
            break;
        default :
            url = "/account/add_project_to_favorite";
            break;
    }
    return url;
}
function GetRemoveFavoriteUrl(type)
{
    var url = "";
    switch (type){
        case "project":
            url = "/account/remove_project_from_favorite";
            break;
        case "demand":
            url = "/account/remove_demand_from_favorite";
            break;
         case "company":
            url = "/account/remove_company_from_favorite";
            break;
        case "member":
            url = "/account/remove_member_from_favorite";
            break;
         case "data":
            url = "/account/remove_data_from_favorite";
            break;
        case "news":
            url = "/account/remove_news_from_favorite";
            break;
        default :
            url = "/account/remove_project_from_favorite";
            break;
    }
    return url;
}
$(".panel-body").delegate(".btn-attach","click",function()
{
    var id = $(this).attr("data-id");
    var type = $(this).attr("data-type");
//    console.log(id);
    var url = "/sales/download_attach/"+id;
    if(type=="demand")
    {
        url = "/purchase/download_attach/"+id;
    }
    window.open(url);
});

/**
 * 添加偏好收藏，
 */
$(".panel-body").delegate(".btn-addfavorite", "click", function() {
    var id = $(this).attr("data-id");
    var type = $(this).attr("data-type");
    var obj = $(this);
    custom_confirm("Are you sure you want to add it to your Favorites?", "New Message", function() {
        var url = GetAddFavoriteUrl(type);
        $.post(url,{id:id},function(data) {
            switch (data) {
                case "success":
                    ChangeFavoriteButtonToCancel(obj);
                    break;
                default :
                    custom_alert(data);
                    break;
            }
        });
    });
});

/**
 * Cancel偏好收藏，
 */
//$(".btn-cancelfavorite").on("click",function()
$(".panel-body").delegate(".btn-cancelfavorite", "click", function() {
    var id = $(this).attr("data-id");
    var type = $(this).attr("data-type");
    var obj = $(this);
    custom_confirm("Are you sure you want to delete it in your Favorites?", "New Message", function() {
        var url = GetRemoveFavoriteUrl(type);
        var $this = $(this);
        $.post(url,{id:id},function(data) {
            switch (data) {
                case "success":
                    ChangeCancelFavoriteButtonToAdd(obj);
                    break;
                default :
                    custom_alert(data);
                    break;
            }
        });
    });
});

/**
 * 移除偏好收藏，同时刷新页面
 */
$(".panel-body").delegate(".btn-remove-favorite", "click", function() {
    var id = $(this).attr("data-id");
    var type = $(this).attr("data-type");
    custom_confirm("Are you sure you want to delete it in your Favorites?", "New Message", function() {
        var url = GetRemoveFavoriteUrl(type);
        var $this = $(this);
        $.post(url,{id:id},function(data) {
            switch (data) {
                case "success":
                    location.reload();
                    break;
                default :
                    custom_alert(data);
                    break;
            }
        });
    });
});

/**
 * 移除偏好收藏，同时利用jquery直接删除地应的li
 */
$(".index_favorite_cancel").click(function() {
    var id = $(this).attr("data-id");
    var type = $(this).attr("data-type");
    var obj = $(this).parent().parent();
    custom_confirm("Are you sure you want to delete it in your Favorites?", "New Message", function() {
        var url = GetRemoveFavoriteUrl(type);
        $.post(url,{id:id},function(data) {
            switch (data) {
                case "success":
                    obj.remove();
                    break;
                default :
                    custom_alert(data);
                    break;
            }
        });
    });
});

function ChangeFavoriteButtonToCancel(btn)
{
    btn.removeClass("btn-addfavorite");
    btn.addClass("btn-cancelfavorite");
    btn.html("<i class=\"glyphicon glyphicon-heart-empty\"></i>&nbsp;Cancel");
    /*btn.unbind("click");
    btn.bind("click",function() {
        var id = $(this).attr("data-id");
        var type = $(this).attr("data-type");
        var url = GetRemoveFavoriteUrl(type);
        var $this = $(this);
        $.post(url, {id: id}, function (data) {
            switch (data) {
                case "success":
                    alert("success");
                    ChangeCancelFavoriteButtonToAdd($this);
                    break;
                default :
                    alert(data);
                    break;
            }
        });
    });*/
}
function ChangeCancelFavoriteButtonToAdd(btn)
{
    btn.removeClass("btn-cancelfavorite");
    btn.addClass("btn-addfavorite");
    btn.html("<i class=\"glyphicon glyphicon-heart\"></i>&nbsp;WatchList");
    /*btn.unbind("click");
    btn.bind("click",function()
    {
        var id = $(this).attr("data-id");
        var type = $(this).attr("data-type");
        var url = GetAddFavoriteUrl(type);
        var $this = $(this);
        $.post(url,{id:id},function(data){
            switch (data)
            {
                case "success":
                    alert("success");
                    ChangeFavoriteButtonToCancel($this);
                    break;
                default :
                    alert(data);
                    break;
            }
        });
    });*/
}

/**
 * 格式话货币
 * usage: someVar.formatMoney(decimalPlaces, symbol, thousandsSeparator, decimalSeparator)
   defaults: (2, "$", ",", ".")
 */
function formatMoney(number, places, symbol, thousand, decimal) {
    number = number || 0;
    places = !isNaN(places = Math.abs(places)) ? places : 2;
    symbol = symbol !== undefined ? symbol : "$";
    thousand = thousand || ",";
    decimal = decimal || ".";
    var negative = number < 0 ? "-" : "",
        i = parseInt(number = Math.abs(+number || 0).toFixed(places), 10) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return symbol + negative + (j ? i.substr(0, j) + thousand : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thousand) + (places ? decimal + Math.abs(number - i).toFixed(places).slice(2) : "");
}

$("#keyword_top").keydown(function(){
    var keyword = $(this).val();
    if(event.keyCode==13)
    {
        if(keyword == "")
        {
            return false;
        }else
        {
            location.href="/sales/search_keyword/"+keyword;
            return false;
        }
    }

});

$("#btn_search_top").click(function() {
    var keyword = $("#keyword_top").val();
    if(keyword == "")
        {
            return false;
        }else
        {
            location.href="/sales/search_keyword/"+keyword;
            return false;
        }
});

/**
 * 添加偏好设置
 * data-type： news, project, demand
 * data-tag： 偏好名称
 */

$(".panel-body").delegate(".preference_common_keyword", "click", function() {
    var obj = $(this);
    custom_confirm("Are you sure you want to set the preference?", "New Message", function() {
        var type = obj.attr("data-type");
        var tag = obj.attr("data-tag")
        if (tag == "" || tag == "undefined")
            tag = obj.text();
        var url = "/account/ajax_preference_news";
        $.post(url, {type_public:type, tag:tag},
            function(data) {
                switch (data) {
                    case "success":
                        break;
                    case "exist":
                        custom_alert("The preference has already existed.");
                        break;
                    default :
                        custom_alert(data);
                        break;
            }
        });
    })
});

var preference_type = jQuery("#preference_type").val();
jQuery(".nav-tabs li").each(function() {
    jQuery(this).removeClass("active");
    if (preference_type == jQuery(this).attr("id")) {
        jQuery(this).addClass("active");
    }
})

autoSlider(0, 1000, 3000);
//industrySelect("company_industry_0", 0);
$("#member_keyword_" ).autocomplete({
    source: function( request, response ) {
        var inTags = jQuery('#member_keyword').val();
        $.ajax({
            url: "/services/getKeywords?term="+request.term+"&inTags=" + inTags,
            dataType: "json",
            success: function( data ) {
                response(data);
            }
        });
    },
    minLength: 2
});

jQuery('#company_industry_0').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_0 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
    $("#company_industry_1").parent().hide();
    $("#company_industry_2").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("company_industry_1", val);
});

jQuery('#company_industry_1').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_1 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
    $("#company_industry_2").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("company_industry_2", val);
});

jQuery('#company_industry_2').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_2 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
});

function open_industry_win() {
    $('#preference_industry_win').modal('show');
}

function open_location_win() {
    $('#preference_location_win').modal('show');
}

function open_keyword_win() {
    $('#preference_keyword_win').modal('show');
}

function addIndustry2() {
    var industry_id = jQuery("#industry_id").val();
    var industryName = jQuery("#industry_name").val();
    if (industry_id == "0" || typeof(industry_id) == "undefined") {
        return;
    }
    var industryCountry = jQuery("#industryCountry").val();
    if (industryCountry == "0") {
        return;
    }
    var currencyId = jQuery("input[name='industryCurrency']:checked").val();
    var currencyName = jQuery("input[name='industryCurrency']:checked").attr("id");
    if (typeof(currencyName) == "undefined") {
        return;
    }
    var industryCountryId = jQuery("#industryCountry").val();
    var industryCountryName = jQuery("#industryCountry option:selected").text();
    var afterUnit = "元";
    var rangeMin = jQuery("#member_range_mins_0").val();
    var rangeMax = jQuery("#member_range_maxs_0").val();
    if (!isMemberExsit("member_industry_" + industry_id + "_" + industryCountryId)) {
        var html = "<span id='member_industry_" + industry_id + "_" + industryCountryId + "' class='alert alert-info preference_selected preference_selected-width'>" +
                "<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove pull-right'></a>地域：" + industryCountryName + "<br/>行业：" + industryName +
                "<br/>金额：" + currencyName + " <a href='###'>" + transfer2Currency(rangeMin) + " - " + transfer2Currency(rangeMax) + "</a>&nbsp;" +
                "<input name='member_industry_ids' type='hidden' value='" + industry_id + "'/><input name='member_range_mins' type='hidden' value='" + rangeMin + "'/>" +
                "<input name='member_range_maxs' type='hidden' value='" + rangeMax + "'/><input name='member_currencys' type='hidden' value='" + currencyId + "'/>" +
                "<input name='member_industry_countryIds' type='hidden' value='" + industryCountryId + "'/></span>";
        jQuery("#member_industry").append(html);
        jQuery("#preference_industry_win").modal('hide');
    }
}

function isMemberExsit(id) {
    return (jQuery("#"+id).val()!=undefined);
}

function addLocation() {
    var val = jQuery("#country").val();
    if (val == "" || val == "0") return;
    var name = jQuery("#country option:selected").text();

    if (!isMemberExsit("member_location_" + val)) {
        var html = "<span id='member_location_" + val + "' class='alert alert-info preference_selected preference_selected-width'> <a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove pull-right'></a>" +
                "<input name='member_country_ids' type='hidden' value='" + val + "'/><input name='member_titles' type='hidden' value='" + name + "'/></span>";
        jQuery("#member_location").append(html);
        jQuery("#preference_location_win").modal('hide');
    }
}

function addKeyword() {
    var val = jQuery("#member_keyword_").val();
    if (!isMemberExsit("member_keyword_" + val)) {
        var html = "<span id='member_keyword_" + val + "' class='alert alert-info preference_selected preference_selected-width'> <a href='###'>" + val + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove pull-right'></a>" +
                   "<input name='member_keywords' type='hidden' value='" + val + "'/></span>";
        jQuery("#member_keyword_tag").append(html);
        jQuery("#member_keyword_").val("");
        jQuery("#preference_keyword_win").modal('hide');
    }
}

function ajax_industry() {
    var i = 0; bool = true;
    $('.custom-required-industry').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#id").val();
        var industryCountry = $("#industryCountry").val();
        var industryId = $("#industry_id").val();
        var industryName = $("#industry_name").val();
        var industryCurrency = $("[name='industryCurrency']:checked").val();
        var member_range_min = $("#member_range_mins_0").val();
        var member_range_max = $("#member_range_maxs_0").val();
        var type_public = $("#preference_type").val();
        type_public = type_public.substring(3, type_public.length);
        var url = "/account/ajax_preference";
        $.post(url,
            {id: project_id, type_public: type_public, type_category: "industry", member_industry_id: industryId,
                member_industry_countryId: industryCountry, member_range_min: member_range_min, member_range_max: member_range_max,
                member_currency: industryCurrency
            },
            function (data) {
                switch (data) {
                    case "success":
                        location.href = location.href;
                        break;
                    case "exist":
                        custom_alert("偏好已存在");
                        break;
                    default :
                        custom_alert(data);
                        break;
                }
            });
    }
//    })
}

function ajax_location() {
    var i = 0; bool = true;
    $('.custom-required-location').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#id").val();
        var locationCountry = $("#country").val();
        var locationCountryName = jQuery("#country option:selected").text();
        var url = "/account/ajax_preference";
        var type_public = $("#preference_type").val();
        type_public = type_public.substring(3, type_public.length);
        $.post(url,
            {id: project_id, type_public: type_public, type_category: "location", member_country_id: locationCountry, member_title: locationCountryName},
            function (data) {
                switch (data) {
                    case "success":
                        location.href = location.href;
                        break;
                    case "exist":
                        custom_alert("偏好已存在");
                        break;
                    default :
                        custom_alert(data);
                        break;
                }
            });
    }
//    })
}

function ajax_keyword() {
    var i = 0; bool = true;
    $('.custom-required').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#id").val();
        var keyword = $("#member_keyword_").val();
        var url = "/account/ajax_preference";
        var type_public = $("#preference_type").val();
        type_public = type_public.substring(3, type_public.length);
        $.post(url,
            {id: project_id, type_public: type_public, type_category: "keyword", keyword: keyword},
            function (data) {
                switch (data) {
                    case "success":
                        location.href = location.href;
                        break;
                    case "exist":
                        custom_alert("偏好已存在");
                        break;
                    default :
                        custom_alert(data);
                        break;
                }
            });
    }
//    })
}

$(".glyphicon-remove").click(function() {
    var obj = $(this)
    custom_confirm("您确定要删除此偏好吗?", "信息提示", function() {
        var id = obj.attr("data-id");
        var type = obj.attr("data-type");
        var url = "/account/ajax_preference_remove";
        $.post(url, {type:type, id:id},
            function(data) {
                switch (data) {
                    case "success":
                        obj.parent().remove();
                        break;
                    default :
                        custom_alert(data);
                        break;
            }
        });
    });
});


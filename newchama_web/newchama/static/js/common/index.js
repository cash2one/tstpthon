
autoSlider(0, 1000, 3000);
//industrySelect("company_industry_0", 0);

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

$(".index_list li a").click(function(){
    var id = $(this).attr("rel");
    $('table[id^=index_list_]').hide();
    $("#index_list_"+id).show();
    $(".index_list li").not(this).removeClass("active");
    $(this).parent().addClass("active");
});

$(".nav_header_custom").delegate(".project_index_tab", "click", function() {
    var url = $(this).attr("ref");
    $(this).parent().siblings("li").not(this).removeClass("active");
    $(this).parent().addClass("active");
    $("#project_index").html("");
    $("#project_index").next().show();
    $.post(url, function (data) {
        $("#project_index").next().hide();
        $("#project_index").html(data);
        },
        "html"
    );
});

$(".nav_header_custom").delegate(".demand_index_tab", "click", function() {
    var url = $(this).attr("ref");
    $(this).parent().siblings("li").not(this).removeClass("active");
    $(this).parent().addClass("active");
    $("#demand_index").html("");
    $("#demand_index").next().show();
    $.post(url, function (data) {
        $("#demand_index").next().hide();
        $("#demand_index").html(data);
        },
        "html"
    );
});

$("#project_search_btn").click(function() {
    var industryIds = "";
    $("[name='project_industry_id']:checked").each(function() {
        industryIds += $(this).val() + ",";
    });
    var locationIds = "";
    $("[name='project_location_id']:checked").each(function() {
        locationIds += $(this).val() + ",";
    });
    if (industryIds.length > 0) industryIds = industryIds.substring(0, industryIds.length - 1);
    if (locationIds.length > 0) locationIds = locationIds.substring(0, locationIds.length - 1);
    var url = $(this).attr("ref");
    url = url + "?industryId=" + industryIds + "&locationId=" + locationIds;
    $(".project_index_tab").parent().siblings("li").removeClass("active");
    $(".project_index_tab").eq(0).parent().addClass("active");
    $("#project_index").html("");
    $("#project_index").next().show();
    $.post(url, function (data) {
        $("#project_index").next().hide();
        $("#project_index").html(data);
        },
        "html"
    );
});

$("#demand_search_btn").click(function() {
    var industryIds = "";
    $("[name='demand_industry_id']:checked").each(function() {
        industryIds += $(this).val() + ",";
    });
    var locationIds = "";
    $("[name='demand_location_id']:checked").each(function() {
        locationIds += $(this).val() + ",";
    });
    if (industryIds.length > 0) industryIds = industryIds.substring(0, industryIds.length - 1);
    if (locationIds.length > 0) locationIds = locationIds.substring(0, locationIds.length - 1);
    var url = $(this).attr("ref");
    url = url + "?industryId=" + industryIds + "&locationId=" + locationIds;
    $(".demand_index_tab").parent().siblings("li").removeClass("active");
    $(".demand_index_tab").eq(0).parent().addClass("active");
    $("#demand_index").html("");
    $("#demand_index").next().show();
    $.post(url, function (data) {
        $("#demand_index").next().hide();
        $("#demand_index").html(data);
        },
        "html"
    );
});

$("#preference_project_industry_submit").click(function() {
    var i = 0; bool = true;
    $('.custom-required-sale-industry').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#preference_project_id").val();
        var industryCountry = $("#industryCountry").val();
        var industryId = $("#industry_id").val();
        var industryName = $("#industry_name").val();
        var industryCurrency = $("[name='industryCurrency']:checked").val();
        var member_range_min = $("#member_range_mins_0").val();
        var member_range_max = $("#member_range_maxs_0").val();
        var url = "/account/ajax_preference";
        $.post(url,
            {id:project_id, type_public:"project", type_category:"industry", member_industry_id:industryId,
                member_industry_countryId:industryCountry, member_range_min:member_range_min, member_range_max:member_range_max,
                member_currency:industryCurrency
            },
            function(data) {
                switch (data) {
                    case "success":
                        clear_preference_project_industry();
                        custom_alert("偏添加完成");
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
});

$("#preference_project_location_submit").click(function() {
    var i = 0; bool = true;
    $('.custom-required-sale-location').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#preference_project_id").val();
        var locationCountry = $("#locationCountry").val();
        var locationCountryName = jQuery("#locationCountry option:selected").text();
        var url = "/account/ajax_preference";
        $.post(url,
            {id:project_id, type_public:"project", type_category:"location", member_country_id:locationCountry, member_title:locationCountryName},
            function(data) {
                switch (data) {
                    case "success":
                        $("#locationCountry").val("");
                        custom_alert("偏添加完成");
//                        $(".index_preference_project_locatoin").append("<label class='checkbox-inline'> <input type='checkbox' name='demand_location_id' id='demand_location_id' value='" + locationCountry + "'/>" + locationCountryName + "</label>");
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
});

autoSlider(1, 1000, 3000);
//industrySelect("company_industry_3", 0);

jQuery('#company_industry_3').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_3 option:selected").text();
    jQuery("#industry_id1").val(val);
    jQuery("#industry_name1").val(name);
    $("#company_industry_4").parent().hide();
    $("#company_industry_5").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("company_industry_4", val);
});

jQuery('#company_industry_4').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_4 option:selected").text();
    jQuery("#industry_id1").val(val);
    jQuery("#industry_name1").val(name);
    $("#company_industry_5").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("company_industry_5", val);
});

jQuery('#company_industry_5').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_5 option:selected").text();
    jQuery("#industry_id1").val(val);
    jQuery("#industry_name1").val(name);
});

$("#preference_demand_industry_submit").click(function() {
    var i = 0; bool = true;
    $('.custom-required-demand-industry').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#preference_demand_id").val();
        var industryCountry = $("#industryCountry1").val();
        var industryId = $("#industry_id1").val();
        var industryName = $("#industry_name1").val();
        var industryCurrency = $("[name='industryCurrency2']:checked").val();
        var member_range_min = $("#member_range_mins_1").val();
        var member_range_max = $("#member_range_maxs_1").val();
        var url = "/account/ajax_preference";
        $.post(url,
            {id:project_id, type_public:"demand", type_category:"industry", member_industry_id:industryId,
                member_industry_countryId:industryCountry, member_range_min:member_range_min, member_range_max:member_range_max,
                member_currency:industryCurrency
            },
            function(data) {
                switch (data) {
                    case "success":
                        clear_preference_demand_industry();
                        custom_alert("Successfully added to preference.");
//                        $(".index_preference_demand_industry").append("<label class='checkbox-inline'> <input type='checkbox' name='demand_location_id' id='demand_location_id' value='" + industryId + "'/>" + industryName + "</label>");
                        break;
                    case "exist":
                        custom_alert("The preference has already existed.");
                        break;
                    default :
                        custom_alert(data);
                        break;
            }
        });
    }
});

$("#preference_demand_location_submit").click(function() {
    var i = 0; bool = true;
    $('.custom-required-demand-location').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            bool = false;
            i ++;
        }
    });
    if (bool) {
        var project_id = $("#preference_demand_id").val();
        var locationCountry = $("#locationCountry1").val();
        var locationCountryName = jQuery("#locationCountry1 option:selected").text();
        var url = "/account/ajax_preference";
        $.post(url,
            {id:project_id, type_public:"demand", type_category:"location", member_country_id:locationCountry, member_title:locationCountryName},
            function(data) {
                switch (data) {
                    case "success":
                        $("#locationCountry1").val("");
                        custom_alert("Successfully added to preference.");
//                        $(".index_preference_demand_location").append("<label class='checkbox-inline'> <input type='checkbox' name='demand_location_id' id='demand_location_id' value='" + locationCountry + "'/>" + locationCountryName + "</label>");
                        break;
                    case "exist":
                        custom_alert("The preference has already existed.");
                        break;
                    default :
                        custom_alert(data);
                        break;
            }
        });
    }
});

$("#preference_demand_industry_cancel").click(function() {
    clear_preference_demand_industry();
});

$("#preference_demand_location_cancel").click(function() {
    $("#locationCountry1").val("");
});

$("#preference_project_industry_cancel").click(function() {
    clear_preference_project_industry();
});

function clear_preference_project_industry() {
    $("#industryCountry").val("");
    $("#company_industry_0").val("");
    $("#company_industry_1").val("");
    $("#company_industry_2").val("");
    $("#company_industry_1").parent().hide();
    $("#company_industry_2").parent().hide();
    autoSlider(0, 1000, 3000);
}

function clear_preference_demand_industry() {
    $("#industryCountry1").val("");
    $("#company_industry_3").val("");
    $("#company_industry_4").val("");
    $("#company_industry_5").val("");
    $("#company_industry_4").parent().hide();
    $("#company_industry_5").parent().hide();
    autoSlider(1, 1000, 3000);
}

$("#preference_project_location_cancel").click(function() {
    $("#locationCountry").val("");
});


$("#send_invite_email_btn").click(function() {
    var reg = /^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
    var invite_email = $('#invite_email').val();
    if (reg.test(invite_email)) {
        $("#send_invite_email_ing").show();
        var obj = $(this);
        obj.hide();
        $.post("/account/send_invitecode/", {invite_email: invite_email}, function (result) {
            result = JSON.parse(result);
            if (result.is_ok == 1) {
                $('#invite_email').val("");
                custom_alert('邀请邮件已成功发送.');
            }
            else {
                custom_alert('您的邀请发送失败！');
            }
            $("#send_invite_email_ing").hide();
            obj.show();
        });
    }
    else {
        custom_alert('邮件格式错误！');
    }
});

$(".slider-tag-custom").click(function() {
    var index = $(".slider-tag-custom").index($(this));
    $(".slider-custom-title").eq(index).slideToggle();
    $(".slider-custom-hide").eq(index).slideToggle();
    if ($(this).hasClass("glyphicon-chevron-down")) {
        $(this).removeClass("glyphicon-chevron-down");
        $(this).addClass("glyphicon-chevron-up");
    }
    else {
        $(this).removeClass("glyphicon-chevron-up");
        $(this).addClass("glyphicon-chevron-down");
    }
});

$(".slider-tag-custom-2").click(function() {
    var index = 0;
    $(".slider-custom-title").eq(index).slideToggle();
    $(".slider-custom-hide").eq(index).slideToggle();
    if ($(".slider-tag-custom").eq(index).hasClass("glyphicon-chevron-down")) {
        $(".slider-tag-custom").eq(index).removeClass("glyphicon-chevron-down");
        $(".slider-tag-custom").eq(index).addClass("glyphicon-chevron-up");
    }
    else {
        $(".slider-tag-custom").eq(index).removeClass("glyphicon-chevron-up");
        $(".slider-tag-custom").eq(index).addClass("glyphicon-chevron-down");
    }
});

$(".project_arrow_right").click(function() {
    var html = $(".nav_project_list").children().eq(1);
    $(".nav_project_list").children().eq(1).remove();
    $(".nav_project_list").append(html);
});

$(".project_arrow_left").click(function() {
    var html = $(".nav_project_list").children().last();
    $(".nav_project_list").children().last().remove();
    $(".nav_project_list").children().eq(0).after(html);
});

$(".demand_arrow_right").click(function() {
    var html = $(".nav_demand_list").children().eq(1);
    $(".nav_demand_list").children().eq(1).remove();
    $(".nav_demand_list").append(html);
});

$(".demand_arrow_left").click(function() {
    var html = $(".nav_demand_list").children().last();
    $(".nav_demand_list").children().last().remove();
    $(".nav_demand_list").children().eq(0).after(html);
});

$(".glyphicon-cog-tag-hide").click(function() {
    var index = $(".glyphicon-cog-tag-hide").index($(this));
    $(".glyphicon-cog-hide").eq(index).slideToggle();
});

page = 1;
function loadData() {
    $("#load_btn").hide();
    $("#loader").show();
    page++;
    var pagesize=5;

    var url = "/account/json_dynamic";
    $.get(url,
        {page:page, pagesize:pagesize},
        function (data) {
            var newData = data.replace(/\s/g,'');
            if(newData) {
                $("#loader").before(data);
            }
            else {
                $("#load_btn").remove();
            }
            $("#load_btn").show();
            $("#loader").hide();
    });
}

var slider_leftwidth = 928;
var slider_index = 0;
var slider_time;
$("#index_left").click(function() {
    var _scroll = $("#index_slider_header");
    _scroll.animate({marginLeft:'+=' + slider_leftwidth}, 1000, function() {
        _scroll.css({marginLeft: -928}).find("img:last").prependTo(_scroll);
    });
    clearTimeout(slider_time);
    slider_time = setTimeout("index_slide()", 3000);
    if (slider_index == 0)
        slider_index = 1;
    else
        slider_index = 0;
});

$("#index_right").click(function() {
    var _scroll = $("#index_slider_header");
    _scroll.animate({marginLeft:'-=' + slider_leftwidth}, 1000, function() {
        _scroll.css({marginLeft: -928}).find("img:first").appendTo(_scroll);
    });
    clearTimeout(slider_time);
    slider_time = setTimeout("index_slide()", 3000);
    if (slider_index == 0)
        slider_index = 1;
    else
        slider_index = 0;
});

$("#immediate_use").click(function() {
    var cls = ".deal_genius";
    if (slider_index == 0)
        cls = ".deal_alert";
    pagePushArea = $.layer({
        type: 1,
        shade: [0],
        area: ['auto', 'auto'],
        title: false,
        fix: false,
        border: [0],
        shade: [0.3, '#000'],
        closeBtn: [0, true], //去掉默认关闭按钮
        page: {dom : cls}
    });
    $(".xubox_layer").css("top", "50px");
});

function index_slide() {
    var _scroll = $("#index_slider_header");
    _scroll.animate({marginLeft:'-=' + slider_leftwidth}, 1000, function() {
        _scroll.css({marginLeft: -928}).find("img:first").appendTo(_scroll);
    });
    slider_time = setTimeout("index_slide()", 3000);
    if (slider_index == 0)
        slider_index = 1;
    else
        slider_index = 0;
}

index_slide();

$("#immediate_close").click(function() {
    $("#deal_genius_adv").slideUp();
});

$("#create_project").click(function() {
    location.href="/sales/add/0/";
});

$("#create_subscribe").click(function() {
    location.href="/subscribe/add";
});


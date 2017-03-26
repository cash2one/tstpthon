
var custom_1 = "parsley-62015-custom";

if ($.fn.popover) { $('.ui-popover').popover ({ container: 'body' }) }

try {
    jQuery('#expire_date').datepicker({format: 'yyyy-mm-dd'});
    jQuery('#lock_date').datepicker({format: 'yyyy-mm-dd'});
} catch(e){}

jQuery("input[name='is_list_company']").click(function() {
    if ($(this).val() == 1) {
        $("#ticker").attr("disabled", false);
    }
    else {
        $("#ticker").attr("disabled", true);
    }
});
/*
$('input[data-type="number"]').iMask({
    type : 'number',
    decDigits : -1 ,
    decSymbol : '',
    sanity : function( val ){
        //return Math.min( 100000000000, Math.max(0, parseFloat( val.replace(/[^\.\d]/g, ''))));
        return Math.min( 999999999999, Math.max(0, parseFloat( val.replace(/[^\.\d]/g, ''))));
    }
});
*/
jQuery("#currency_select").change(function() {
    var val = jQuery(this).val();
    var unit = jQuery("#" + this.id + " option:selected").text();
    jQuery(".currency_unit").html(unit);
    var unit = getCurrentCurrency();
    $('input[data-type="number"]').each(function() {
        this.value = this.value.replace(/[^\d]/g, '');
        var val = $(this).val();
//        if (val != "") {
        if (val == "") val = 0;
            var nextId = $(this).next().attr("id");
            if (nextId == "autosymbol") $(this).next().html(unit + val);
            else $(this).after("<div id='autosymbol'>" + unit + val + "</div>");
//        }
    })
});

$('input[data-type="number"]').keyup(function() {
    handleCurrency(this);
});

function handleCurrency(obj) {
    obj.value = obj.value.replace(/[^\d]/g, '');
    var val = $(obj).val();
    val = formatMoney(val, '', '');
    var unit = getCurrentCurrency();
    var nextId = $(obj).next().attr("id");
    if (nextId == "autosymbol") $(obj).next().html(unit + val);
    else $(obj).after("<div id='autosymbol'>" + unit + val + "</div>");
}

$('#deal_size').keyup(function() {
    var val = $(this).val();
    var percent = $("#stock_percent").val();
    countDealSize(val, percent);
});

$("#stock_percent").keyup(function() {
    var val = $("#deal_size").val();
    var percent = $(this).val();
    countDealSize(val, percent);
});

function countDealSize(eev, sp) {
    var _element = $("#expected_enterprice_value");
    var val = 0; var percent = 0; var result = 0;
    if (eev != "")
        val = parseInt(eev.replace(/,/g, ""));
    if (sp != "")
        result = val / (sp / 100);
    _element.val(parseInt(result));
    result = formatMoney(result, '', '')
    var nextId = _element.next().attr("id");
    var unit = getCurrentCurrency();
    if (nextId == "autosymbol") _element.next().html(unit + result);
    else _element.after("<div id='autosymbol'>" + unit + result + "</div>");
}

jQuery("#country").change(function(){
    LoadProvinces('province',jQuery(this).val(),0);
});

jQuery("#is_audited").click(function() {
    if (jQuery(this).prop("checked")) {
        $("#financial_audit_company_name").attr("required", true);
        jQuery(".bigfour").show();
    }
    else {
        $("#financial_audit_company_name").attr("required", false);
        jQuery(".bigfour").hide();
    }
});

$(".s_rate_bak").keyup(function() {
    var total = 0;
    var index = $(".s_rate").index($(this));
    $(".s_rate").each(function(i) {
        if (index < i) {
            var result = 100 - parseFloat(total);
            if (result <= 0) {
                $(this).val("0");
            }
            else {
               if (isNaN(result)) result = 0;
                $(this).val(result);
            }
        }
        if (index == i) {
            var result = 100 - parseFloat(total) - $(this).val();
            if (result < 0) {
                $(this).val(100 - parseFloat(total));
            }
        }
        total += parseFloat($(this).val());
    });
});

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

jQuery('#target_company_industry_0').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_0 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
    jQuery("#company_industry_1").parent().hide();
    jQuery("#company_industry_2").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("company_industry_1", val);
});

jQuery('#company_industry_1').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_1 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
    jQuery("#company_industry_2").parent().hide();
    if (val == "0" || val == "") return;
    industrySelect("company_industry_2", val);
});

$("#service_type").change(function() {
    var val = jQuery(this).val();
    if (val == 2) $(".project_stage").removeClass("hide_");
    else $(".project_stage").addClass("hide_");
});

jQuery('#company_industry_2').change(function() {
    var val = jQuery(this).val();
    var name = jQuery("#company_industry_2 option:selected").text();
    jQuery("#industry_id").val(val);
    jQuery("#industry_name").val(name);
});

jQuery("#financial_audit_company_name").autocomplete({
    source: function( request, response ) {
        $.ajax({
            url: "/services/get_audit_companies/"+request.term,
            dataType: "json",
            success: function( jsonResponse ) {
                var data = $(jsonResponse).map(function(id,item) {
                    return {
                        value: item.fields.name_cn,
                        label: item.fields.name_cn,
                        id: item.pk
                    };
                });
                response(data);
            }
        });
    },
    minLength: 2
});

jQuery("#ticker" ).autocomplete({
    source: function( request, response ) {
        jQuery.ajax({
            url: "/services/get_listed_companies/"+request.term,
            dataType: "json",
            success: function( jsonResponse ) {
                var data = $(jsonResponse).map(function(id,item) {
                    return {
                        value: item.fields.stock_symbol,
                        label: item.fields.stock_symbol + ":" + item.fields.short_name_cn,
                        id: item.pk
                    };
                });
                response(data);
            }
        });
    },
    minLength: 2
});

jQuery("#target_company").autocomplete({
    source: function( request, response ) {
        $.ajax({
            url: "/services/get_active_companies/"+request.term,
            dataType: "json",
            success: function( jsonResponse ) {
                var data = $(jsonResponse).map(function(id,item) {
                    if (get_template_lang() == "zh-cn") {
                        return {
                            value: item.fields.name_cn,
                            label: item.fields.name_cn,
                            id: item.pk
                        };
                    }
                    else {
                        return {
                            value: item.fields.name_en,
                            label: item.fields.name_en,
                            id: item.pk
                        };
                    }
                });
                response(data);
            }
        });
    },
    minLength: 2,
    select: function(event, data) {
        jQuery("#target_company_id").val(data.item.id);
    }
});

jQuery("#target_member").autocomplete({
    source: function( request, response ) {
        $.ajax({
            url: "/services/get_active_member/"+request.term,
            dataType: "json",
            success: function( jsonResponse ) {
                var data = $(jsonResponse).map(function(id,item) {
                    return {
                        value: item.fields.first_name + " " + item.fields.last_name,
                        label: item.fields.first_name + " " + item.fields.last_name,
                        id: item.pk
                    };
                });
                response(data);
            }
        })
    },
    minLength: 2,
    select: function(event, data) {
        jQuery("#target_member_id").val(data.item.id);
    }
});

$("#key_keyword" ).autocomplete({
    source: function( request, response ) {
        var inTags = jQuery('#project_keyword').val();
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

function addIndustry2() {
    var industry_id = jQuery("#target_industry_id").val();
    var industryName = jQuery("#target_industry_name").val();
    if (industry_id == "0" || industry_id == "") return;
    if (!isObjectExsit("target_industry_" + industry_id)) {
        var html = "<span id='target_industry_" + industry_id + "' class='alert alert-info preference_selected'><a href='###'>" + industryName + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='target_industries' type='hidden' value='" + industry_id + "'></span>";
        jQuery("#target_industry").append(html);
    }
}

function addCompany2() {
    var id = jQuery("#target_company_id").val();
    var name = jQuery("#target_company").val();
    if (id == "0" || id == "") return;
    if (!isCompanyExsit(id)) {
        $(".target_company_div").removeClass("hide_");
        //在id=target_company_ 加 2_ 是因为查询推荐机构是从listedcompany中查询的，为了在编辑状态下能正确删除，所以添加对应节点说明，否则同一个id因为可能从member_company,investment_company和listed_company中获取到重复的id
        var html = "<span id='target_company_1_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='target_companies' type='hidden' value='" + id + "'></span>";
        jQuery("#target_compaies").append(html);
        jQuery("#target_company").val("");
        jQuery("#target_company_id").val("");
    }
}

function isCompanyExsit(val) {
    var bool = false;
    jQuery("input[name='target_companies']").each(function() {
        if (jQuery(this).val() == val) {
            bool = true;
            return false;
        }
    });
    return bool;
}

function addMember2() {
    var id = jQuery("#target_member_id").val();
    var name = jQuery("#target_member").val();
    if (id == "0" || id == "") return;
    if (!isObjectExsit("target_member_" + id)) {
        var html = "<span id='target_member_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='target_members' type='hidden' value='" + id + "'></span>";
        jQuery("#target_members").append(html);
        jQuery("#target_member").val("");
        jQuery("#target_member_id").val("");
    }
}

function addKeyword2() {
    var name = jQuery("#key_keyword").val();
    if (name == "") return;
    if (!isObjectExsit("target_keyword_" + name)) {
        var html = "<span id='target_keyword_" + name + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove project_key_remove' ref='"+name+"'></a>" +
            "</span>";
        jQuery("#target_keywords").append(html);
        var val = jQuery("#project_keyword").val();
        if (val == "")
            val = name;
        else
            val += "," + name;
        jQuery("#project_keyword").val(val);
        jQuery("#key_keyword").val("")
    }
    if ($("#" + custom_1).length > 0)
        $("#" + custom_1).remove();
}

$(".panel-body").delegate(".project_key_remove", "click", function() {
    var val = $(this).parent().text().trim() + ",";
    var key = $("#project_keyword").val() + ",";
    key = key.replace(val, "");
    $("#project_keyword").val(key.substring(0, key.length - 1));
});

$(".panel-body").delegate(".glyphicon-remove", "click", function() {
    var len = $("#target_compaies .preference_selected").length;
    if (len <= 1) {
        $(".target_company_div").addClass("hide_");
    }
});

function isObjectExsit(id) {
    return (jQuery("#"+id).val()!=undefined);
}

$("#btn_add_attach").click(function() {
    var type = $("#attachment_type").val();
    if (type == "0") {
        custom_alert("请先选择您要上传的附件类型", "信息提示");
        return;
    }
    if (isAttachExsit(type)) {
        custom_alert("该附件已存在", "信息提示");
        return;
    }
    var name = $("#attachment_type option:selected").text();
    var html = "<div class='form-group attach_sub' ref='" + name + "'><div class='col-md-3'>" + name + "</div>" +
                "<div class='col-md-6'><input type='hidden' name='upload_types' value='" + type + "'><input type='hidden' name='upload_type_names' value='" + name + "'><input type='file' name='upload_file_" + type + "' /></div></div>";
    $(".attach_area").parent().append(html);
});

$("#btn_remove_attach").click(function() {
//    if ($(".attach_sub").length <= 1) {
//        return;
//    }
    var txt = $(".attach_sub").last().attr("ref");
    custom_confirm("您确定要删除 [ " + txt + " ] 的附件吗?", "信息提示", function() {
        $(".attach_sub").last().remove();
    });
});

function isAttachExsit(type) {
    var bool = false;
    $("input[name='upload_types']").each(function() {
       if ($(this).val() == type) {
           bool = true;
           return false;
       }
    });
    return bool;
}
/*
$("#btn_draft").click(function() {
    $('.parsley-form').parsley('destroy');
    var bool = true;
    var i = 0;
    $("select").each(function() {               //if the select value is empty, then set 0, or it will be wrong
       if ($(this).val() == "") {
           $(this).val("0");
       }
    });
    $('.custom-required').each(function() {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            i ++;
            bool = false;
        }
    });
    if (bool) {
        $("#submitStatus").val("draft");
        $('#formData').submit();
    }
});
*/
 $('input[data-type="percent"]').iMask({
     type : 'number',
     decDigits : -1 ,
     decSymbol : '',
     sanity : function( val ) {
        return Math.min( 100, Math.max(0, parseFloat( val.replace(/[^\.\d]/g, ''))));
     }
 });

 $('input[data-type="percentPlus"]').iMask({
    type      : 'fixed',
    mask      : '99999',
    stripMask : true
 });

jQuery("input[name='is_suitor']").click(function() {
    var val = jQuery(this).val();
    if (val == "1")
        jQuery(".suitor input").attr("disabled", false);
    else
        jQuery(".suitor input").attr("disabled", true);
});

jQuery("#btn_reset").click(function() {
    location.href = location.href;
});

function endSave(fun_) {
    $(".alert_message").remove();
	$("#formData").ajaxSubmit({
	    type: 'post',
	    dataType: 'json',
	    success: function(data) {
            if (data.result == "success") {
                $("#edit_id").val(data.id);
                //sthowStep(4);
                fun_(true);
            }
            else {
                if (data.message == "typeError")
                    errorMessages("上传文件必须是doc|docx|pdf");
                else if (data.message == "tooBig")
                    errorMessages("文件大小不能大于20兆");
                else
                    errorMessages("提交内容有误，请调整后再试，或联系管理员，谢谢");
                    //errorMessages(data.message);
                $(".alert_message").removeClass("hide_");
            }
            fun_(false);
	    }
	});
}

function errorMessages(errorMsg) {
    var html = '<div class="alert alert-warning alert_message"><a class="close" data-dismiss="alert" href="#" aria-hidden="true">&times;</a><span id="error_message">'+ errorMsg +'</span></div>';
    $(".tip_span").append(html);
}

function checkMustEnter(index) {
    var bool = true;
    var i = 0;
    if (index == 0)
        cls = "custom-required";
    else if (index == 1) {
        cls = "custom-required_";
    }
    else
        return true;
    $('.parsley-form').parsley('destroy');
//    $("select").each(function () {               //if the select value is empty, then set 0, or it will be wrong
//        if ($(this).val() == "") {
//            $(this).val("0");
//        }
//    });
    var bool = true;
    $('.' + cls).each(function () {
        if (!$(this).parsley().validate()) {
            if (i == 0) $(this).focus();
            i++;
            bool = false;
        }
    });

    if (index == 1) {
        if ($("#project_keyword").val() == "") {
            var custom_error = '<ul id="' + custom_1 + '" class="parsley-error-list" style="display: block;"><li class="custom-error-message" style="display: list-item;">请填写关键字</li></ul>';
            if ($("#" + custom_1).length == 0)
                $("#key_keyword").after(custom_error);
            bool = false;
        }
        else {
            if ($("#" + custom_1).length > 0)
                $("#" + custom_1).remove();
            bool = true;
        }
    }
    return bool;
}

function checkProjectStage() {
    if ($("#service_type").val() != 2) return true;
    var bool = true;
    $('.custom-required_s').each(function () {
        if (!$(this).parsley().validate()) {
            $(this).focus();
            bool = false;
        }
    });
    return bool;
}

industrySelect("target_company_industry_0", 0);

$('input[data-type="number"]').each(function() {
    handleCurrency(this);
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
/*
jQuery(".chosen-select").chosen({'width':'100%','white-space':'nowrap'});
jQuery('#expire_date').datepicker({dateFormat: "yy-mm-dd"});
jQuery('#lock_date').datepicker({dateFormat: "yy-mm-dd"});

jQuery("#company_stock_symbol").change(function() {
    jQuery("#company_stock_exchange").val(jQuery("#" + this.id + " option:selected").attr("val"));
});

jQuery("#service_type").change(function() {
    var val = jQuery(this).val();
    if (val == 6)           //增发
        jQuery(".service_type").show();
    else
        jQuery(".service_type").hide();
});

jQuery("#list_company").click(function() {
    if (jQuery(this).attr("checked")== "checked")
        jQuery("#ticker_div").show();
    else
        jQuery("#ticker_div").hide();
});

jQuery("#is_audited").click(function() {
    if (jQuery(this).attr("checked")== "checked")
        jQuery(".bigfour").show();
    else
        jQuery(".bigfour").hide();
});

jQuery("#is_suitor").click(function() {
    if (jQuery(this).attr("checked")== "checked")
        jQuery(".suitor").show();
    else
        jQuery(".suitor").hide();
});

jQuery("#is_big_four").click(function() {
    jQuery("#financial_audit_company_name").val(0);
    if (jQuery(this).attr("checked") == "checked")
        jQuery(".financial_audit_company__name_option_False").wrap("<span class='hide_'></span>");
    else
        jQuery(".financial_audit_company__name_option_False").unwrap("span");

    jQuery("#financial_audit_company_name").trigger("chosen:updated");
});
$("#ticker" ).autocomplete({
  source: function( request, response ) {
    $.ajax({
      url: "/repository/get_listed_companies/"+request.term,
      dataType: "json",
      success: function( jsonResponse ) {
         var data = $(jsonResponse).map(function(id,item) {
          return {
            value: item.fields.stock_symbol,
            label: item.fields.stock_symbol + ":" + item.fields.short_name_en,
            id: item.pk
          };
        })
       response(data);
      }
    });
  },
  minLength: 2
});

jQuery("#financial_audit_company_name").autocomplete({
  source: function( request, response ) {
    $.ajax({
      url: "/repository/get_audit_companies/"+request.term,
      dataType: "json",
      success: function( jsonResponse ) {
         var data = $(jsonResponse).map(function(id,item) {
          return {
            value: item.fields.name_cn,
            label: item.fields.name_cn,
            id: item.pk
          };
        })
       response(data);
      }
    });
  },
  minLength: 2
});

jQuery("#target_member").autocomplete({
    source: function( request, response ) {
        $.ajax({
            url: "/repository/get_active_member/"+request.term,
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

jQuery("#currency_select").change(function() {
    var val = jQuery(this).val();
    var unit = jQuery("#" + this.id + " option:selected").text();
    jQuery(".currency_unit").html(unit);
});

jQuery("#country").change(function(){
    LoadProvinces('province',jQuery(this).val(),0);
    jQuery("#province_id").val(0);
    jQuery("#city_id").val(0);
});
jQuery("#province").change(function(){
    var province_id=jQuery(this).val();
    LoadCities('city',province_id,0);
    jQuery("#province_id").val(province_id);
    jQuery("#city_id").val(0);
});

jQuery("#city").change(function(){
    var city_id=jQuery(this).val();
    jQuery("#city_id").val(city_id);
});

jQuery("#equity_add").click(function() {
    var html = $("#equity_structure_div_1").clone(true);
    html.attr("id", "equity_structure_div_" + structurenum);
    html.find("select").attr("id", "equity_structure_select_" + structurenum);
    html.find("input").attr("value", "");

    var addTag = "equity_structure_div";
    if (structurenum > 0) addTag = addTag + "_" + (structurenum - 1);
    jQuery("#" + addTag).after(html);
    structurenum ++;
});

jQuery("#equity_remove").click(function() {
    if (structurenum <= 2) return;
    structurenum --;
    $("#equity_structure_div_" + structurenum).remove();
});

industrySelect("company_industry_0", 0);
industrySelect("target_company_industry_0", 0);

jQuery('#target_company_industry_0').change(function() {
    var val = jQuery(this).val();
    industrySelect("target_company_industry_1", val);
});

jQuery('#target_company_industry_1').change(function() {
    var val = jQuery(this).val();
    industrySelect("target_company_industry_2", val);
});

jQuery('#company_industry_0').change(function() {
    var val = jQuery(this).val();
    industrySelect("company_industry_1", val);
});

jQuery('#company_industry_1').change(function() {
    var val = jQuery(this).val();
    industrySelect("company_industry_2", val);
});

jQuery("#industry_0").click(function() {
    addIndustry("target_company_industry_0", "target_");
});

jQuery("#industry_1").click(function() {
    addIndustry("target_company_industry_1", "target_");
});

jQuery("#industry_2").click(function() {
    addIndustry("target_company_industry_2", "target_");
});

jQuery(".customClose").live("click", function() {
    jQuery(this).parent().remove();
});

jQuery('#project_keyword').tagsInput({
    'width':'auto',
    'height':'64px',
    'autocomplete_url': "/repository/getKeywords?inTags="+jQuery('#project_keyword').val()
});

function addCompany2() {
    var id = jQuery("#target_company_id").val();
    var name = jQuery("#target_company").val();
    if (id == "0" || id == "") return;
    if (!isCompanyExsit(id)) {
        //在id=target_company_ 加 2_ 是因为查询推荐机构是从listedcompany中查询的，为了在编辑状态下能正确删除，所以添加对应节点说明，否则同一个id因为可能从member_company,investment_company和listed_company中获取到重复的id
        var html = "<span id='target_company_1_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='target_companies' type='hidden' value='" + id + "'><input name='target_companies_type' type='hidden' value='1'></span>";
        jQuery("#target_compaies").append(html);
        jQuery("#target_company").val("");
        jQuery("#target_company_id").val("");
    }
}

function isCompanyExsit(val) {
    var bool = false;
    jQuery("input[name='target_companies_1_']").each(function() {
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

function isObjectExsit(id) {
    return (jQuery("#"+id).val()!=undefined);
}

$("#btn_add_attach").click(function() {
    var type = $("#attachment_type").val();
    if (type == "") {
        custom_alert("请先选择您要上传的附件类型", "信息提示");
        return;
    }
    if (isAttachExsit(type)) {
        custom_alert("该附件已存在", "信息提示");
        return;
    }
    var name = $("#attachment_type option:selected").text();
    var html = "<div class='form-group attach_sub' ref='" + name + "'><label class='col-md-3 control-label'>" + name + "</label>" +
                "<div class='col-md-9'><input type='hidden' name='upload_types' value='" + type + "'><input type='hidden' name='upload_type_names' value='" + name + "'><input type='file' name='upload_file_" + type + "' /></div></div>";
    $(".attach_area").after(html);
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
*/

jQuery("#service_type").change(function() {
    var val = jQuery(this).val();
    if (val == 6) {          //增发
        jQuery(".service_type").show();
        $('.custom-required-add').each(function () {
            $(this).attr("required", true);
        });
    }
    else {
        jQuery(".service_type").hide();
        $('.custom-required-add').each(function () {
            $(this).attr("required", false);
        });
    }
});

$('#expected_enterprice_value').keyup(function() {
    var val = $(this).val();
    var percent = $("#stock_percent").val();
    countDealSize(val, percent);
});

$("#stock_percent").keyup(function() {
    var val = $("#expected_enterprice_value").val();
    var percent = $(this).val();
    countDealSize(val, percent);
});

function countDealSize(eev, sp) {
    var val = 0; var percent = 0;
    if (eev != "")
        val = parseInt(eev.replace(/,/g, ""));
    else
        val = 0;
    if (sp != "")
        percent = parseFloat(sp) / 100;
    var result = val * percent;
    result = formatMoney(result, '', '')
    $("#deal_size").val(result);
}

/*
$("#btn_save").click(function() {
    var bool = true;
    $('.parsley-form').parsley('destroy');
    $("select").each(function() {               //if the select value is 0, the set it to empty for the parsley validate
       if ($(this).val() == "0") {
           $(this).val("");
       }
    });

    if ($('.parsley-form').parsley('validate')) {
        $("#submitStatus").val("pending");
        $('#formData').submit();
    }
});
*/
jQuery("#is_agent_project").click(function() {
    if (jQuery(this).prop("checked")) {
        jQuery(".is_agent_project_").show();
    }
    else {
        jQuery(".is_agent_project_").hide();
    }
});

$("#features_cn_").keyup(function() {
    var val = $(this).val();
    $("#features_cn").val(val.replace(/\n/g, "<br/>"));
});

$("#features_en_").keyup(function() {
    var val = $(this).val();
    $("#features_en").val(val.replace(/\n/g, "<br/>"));
});

$("#company_intro_cn_").keyup(function() {
    var val = $(this).val();
    $("#company_intro_cn").val(val.replace(/\n/g, "<br/>"));
});

$("#company_intro_en_").keyup(function() {
    var val = $(this).val();
    $("#company_intro_en").val(val.replace(/\n/g, "<br/>"));
});


$("#company_industry_intro_cn_").keyup(function() {
    var val = $(this).val();
    $("#company_industry_intro_cn").val(val.replace(/\n/g, "<br/>"));
});

$("#company_industry_intro_en_").keyup(function() {
    var val = $(this).val();
    $("#company_industry_intro_en").val(val.replace(/\n/g, "<br/>"));
});

function initFormValidation () {
    $('.parsley-form').each (function () {
        $(this).parsley ({
            trigger: 'change',
            errors: {
                container: function (element, isRadioOrCheckbox) {
                    if (element.parents ('form').is ('.form-horizontal')) {
                        return element.parents ("*[class^='col-']")
                    }
                    return element.parents ('.form-group')
                }
            }
        });
    });
}


$("#financial_year").change(function() {
    var val = $(this).val();
    $(".financial_year_2").html(parseInt(val) - 1);
    $(".financial_year_3").html(parseInt(val) - 2);
});


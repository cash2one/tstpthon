
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

$(".oneclick_btn").click(function() {
    $.layer({
        type: 2,
        border: [0],
        title: '一键发布',
        shadeClose: true,
        closeBtn:[0, true],
        iframe: {src : '/sales/one_click/'},
        area: ['530px', '230px']
    });
});

$(".btn_review").click(function() {
    var editid = $("#edit_id").val();
    var url = "/sales/detail/" + editid + "/?type=1";
    pageDetail = $.layer({
        type: 2,
        border: [0],
        title: false,
        fix: false,
        closeBtn:[0, true],
        iframe: {src : url, scrolling: 'no'},
        area: ['1000px', '790px']
    });
    $(".xubox_layer").css("top", "50px");
});

function emailReview() {
//    emailSend();
//    if (true) return;
    var editid = $("#edit_id").val();
    var url = "/sales/view_email/" + editid;
    pageDetail = $.layer({
        type: 2,
        border: [0],
        title: false,
        closeBtn:false,
        iframe: {src : url, scrolling: 'no'},
        area: ['750px', '660px']
    });
    $(".xubox_layer").css("top", "50px");
}

function resetIframeHeight(h) {
    $("#xubox_layer1").css("height", h);
    $("#xubox_iframe1").css("height", h);
}

function openPage(val) {
    if (val == "") return;
    layer.close(pageDetail);
    showStep(val);
}

$("#target_btn_add").click(function() {
    var editid = $("#edit_id").val();
    if (editid == "") return;
    var target_company_id = $("#target_company_id").val();
    if (target_company_id == "") return;
    var url = "/sales/bankingGenuisSave";
    jQuery.post(url,
        {companyIds:target_company_id, operate:"0", projectId:editid},
        function(data) {
            var result = JSON.parse(data);
            if (result.result == "success") {
                var dat = new Date();
                var newTagNum = result.editId;
                var target_company = $("#target_company").val();
                var html = '<tr><td><a target="_blank" href="/account/company/' + target_company_id + '/">' + target_company + '</a></td><td id="recommendItemControlId_' + newTagNum + '">未发送</td><td><select class="form-control" onchange="bankingGenuisExcute_view_email(this.value, ' + newTagNum + ')"><option value="">请选择</option><option value="1" ref="已发送">发送项目</option><option value="2" ref="移除">移除</option><option value="3" ref="签订NDA状态">移至签订NDA状态</option><option value="4" ref="签订TS状态">移至签订TS状态</option><option value="5" ref="交割">交割</option></select></td></tr>';
                $(".table_recommend_2").children().first().after(html).fadeIn();
            }
    });
});

$("#target_btn_cancel").click(function() {
    $(".newCompanyArea").fadeOut();
});

$("#btn_add_new").click(function() {
    $(".newCompanyArea").fadeIn();
});

$(".recommend_assist li a").click(function() {
    $(".recommend_assist li").not(this).removeClass("active");
    $(this).parent().addClass("active");
//    $(".table_recommend_1").children().remove();
    $(".assist_loading").removeClass("hide_");
    var url = "/sales/json_recommend";
    var id = $("#edit_id").val();
    var page = $(this).attr("ref");
    var pagesize=5;
    jQuery.post(url,{id:id, page:page, pagesize:pagesize},function(data){
        var newData = data.replace(/\s/g,'');
        if(newData)
            $(".table_recommend_1").children().last().after(data);
//            $(".table_recommend_1").html(data);
        $(".assist_loading").addClass("hide_");
    });
});

function loadPotentialCount(type) {
//    var potentialNum = $(".potentialNum").text();
    $(".potentialNum").text(0);
    var target_location_id = $("#target_location_id").val();
    var target_industry_id = $("#target_industry_id").val();
    var target_location_Type = $("#target_location_Type").val();
    var target_reasons = "";
    $("input[name='recomond_reason']:checkbox").each(function() {
        if ($(this).prop("checked"))
            target_reasons += $(this).val() + ",";
    });
    if (target_reasons.length > 0)
        target_reasons = target_reasons.substring(0, target_reasons.length - 1);
    if (target_reasons == 0 && target_location_id == "0" && target_industry_id == "0" && type == "search") return;
    var url = "/sales/json_recommend_count";
    var id = $("#edit_id").val();
    jQuery.post(url, {id:id, target_location_id:target_location_id, target_industry_id:target_industry_id,
        target_location_Type:target_location_Type, target_reasons:target_reasons},
        function(data) {
            $(".potentialNum").html(data);
    });
}

var page = 0;
var page2 = 0;
var dealGenuisCount = 0;

function loadRecommendCondition() {

}

function loadRecommend(type) {
    var target_location_id = $("#target_location_id").val();
    var target_industry_id = $("#target_industry_id").val();
    var target_location_Type = $("#target_location_Type").val();
    var potentialNum = $(".potentialNum").text();
    var target_reasons = "";
    $("input[name='recomond_reason']:checkbox").each(function() {
        if ($(this).prop("checked"))
            target_reasons += $(this).val() + ",";
    });
    if (target_reasons.length > 0)
        target_reasons = target_reasons.substring(0, target_reasons.length - 1);
    if (target_reasons == 0 && target_location_id == "0" && target_industry_id == "0" && type == "search") return;
    $(".view-more-recommond_1").addClass("hide_");
    $(".assist_loading").removeClass("hide_");
    page ++;
    var pagesize = 10;
    var url = "/sales/json_recommend";
    var id = $("#edit_id").val();
    jQuery.post(url,{id:id, page:page, pagesize:pagesize,
        target_location_id:target_location_id, target_industry_id:target_industry_id,
        target_location_Type:target_location_Type, target_reasons:target_reasons, potentialNum:potentialNum},
        function(data) {
            var newData = data.replace(/\s/g,'');
            if(newData) {
                $(".table_recommend_1").children().last().after(data);
                if ($("#no_more_div").length > 0) {
                    var html = '<tr class="noMoreshow_1"><td colspan="6" align="center">暂无相关推荐</td></tr>';
                    if (potentialNum > 0)
                        html = '<tr class="noMoreshow_1"><td colspan="6" align="center">暂无更多推荐</td></tr>';
                    $(".table_recommend_1").children().last().after(html);
                    $(".assist_loading").addClass("hide_");
                }
                else {
                    var have_more_data = $("#have_more_data").length;
                    $(".assist_loading").addClass("hide_");
                    if (have_more_data > 0)
                        $(".view-more-recommond_1").removeClass("hide_");
                }
                $("#no_more_div").remove();
                $("#have_more_data").remove();
            }
            else {
                $(".table_recommend_1").children().last().after(html);
                $(".assist_loading").addClass("hide_");
            }
    });
}

$("#btn_search").click(function() {
    $(".table_recommend_1").children().not(":first").remove();
    page = 0;
    loadPotentialCount("loadMore");
    loadRecommend("assist_loading");
})

function loadRecommedn1() {
    loadRecommend("loadMore");
}

function hideMoreBtn(cls) {
    $("." + cls).addClass("hide_");
}

function loadRecommedn2() {
    $(".view-more-recommond_2").addClass("hide_");
    $(".assist_loading_2").removeClass("hide_");
    page2++;
    var pagesize = 10;
    var url = "/sales/json_recommend";
    var id = $("#edit_id").val();
    jQuery.post(url,{id:id, page:page2, pagesize:pagesize, position:'control'},function(data) {
        var newData = data.replace(/\s/g,'');
        if(newData) {
            $(".table_recommend_2").children().last().after(data);
            if ($("#no_more_div").length > 0) {
                var list = $('td[id^=recommendItemControlId_]');
                if (list.length == 0) {
                    var html = '<tr class="noMoreshow_1"><td colspan="6" align="center">暂无相关推荐</td></tr>';
                    $(".table_recommend_2").children().last().after(html);
                }
//                if (potentialNum > 0)
//                    html = '<tr class="noMoreshow_1"><td colspan="6" align="center">暂无更多推荐</td></tr>';
                $(".assist_loading_2").addClass("hide_");
            }
            else {
                var have_more_data = $("#have_more_data").length;
                $(".assist_loading_2").addClass("hide_");
                if (have_more_data > 0)
                    $(".view-more-recommond_2").removeClass("hide_");
            }
            $("#no_more_div").remove();
            $("#have_more_data").remove();
        }
        else {
            $(".table_recommend_2").children().last().after(html);
            $(".assist_loading_2").addClass("hide_");
        }
    });
}

$("#btn_add_control").click(function() {
    var itemIds = "";
    var companyIds = "";
    $("input[name='recommendItemIds']:checkbox").each(function() {
        if ($(this).prop("checked")) {
            itemIds += $(this).val() + ",";
            companyIds += $(this).attr("ref") + ",";
        }
    });
    if (itemIds.length > 0)
        bankingGenuisSave(0, itemIds.substring(0, itemIds.length - 1), companyIds.substring(0, companyIds.length - 1));
});

$("#btn_add_send").click(function() {
    var itemIds = "";
    var companyIds = "";
    $("input[name='recommendItemIds']:checkbox").each(function() {
        if ($(this).prop("checked")) {
            itemIds += $(this).val() + ",";
            companyIds += $(this).attr("ref") + ",";
        }
    });
    if (itemIds.length > 0) {
        v_email_operate = 1;
        v_email_itemIds = itemIds.substring(0, itemIds.length - 1);
        v_email_companyIds = companyIds.substring(0, companyIds.length - 1);
        emailReview();
    }
    (1, itemIds.substring(0, itemIds.length - 1), companyIds.substring(0, companyIds.length - 1));
});

function selcheckbox(val) {
    $("input[name='recommendItemIds']:checkbox").each(function() {
        if ($(this).val() == val) {
            $(this).attr("checked", false);
            $(this).attr("disabled", true);
            return ;
        }
    });
}

var v_email_operate = 0;
var v_email_itemIds = "";
var v_email_companyIds = "";
var v_email_control_operate = 0;
var v_email_control_id = 0;
var v_send_extend_email = false;
function bankingGenuisSave_view_email(operate, itemIds, companyIds) {
    if (operate == 1) {
        v_email_operate = operate;
        v_email_itemIds = itemIds;
        v_email_companyIds = companyIds;
       emailReview();
    }
    else {
        bankingGenuisSave(operate, itemIds, companyIds);
    }
}

function bankingGenuisExcute_view_email(val, ptodId) {
    if (val == "1") {
        v_email_control_operate = val;
        v_email_control_id = ptodId;
       emailReview();
    }
    else
        bankingGenuisExcute(val, ptodId);
}

function emailSend() {
    if (v_send_extend_email)
        send_extenal_email();
    else if (v_email_operate > 0)
        bankingGenuisSave(v_email_operate, v_email_itemIds, v_email_companyIds);
    else
        bankingGenuisExcute(v_email_control_operate, v_email_control_id);
    v_email_operate = 0;
    v_email_itemIds = "";
    v_email_companyIds = "";
    v_email_control_operate = 0;
    v_email_control_id = 0;
    v_send_extend_email = false;
}

function bankingGenuisSave(operate, itemIds, companyIds) {
    var editid = $("#edit_id").val();
    if (editid == "") return;
    var url = "/sales/bankingGenuisSave";
    var text = "已添加到队列";
    var tipText = "正在为您添加到队列";
    if (operate == 1) {
        text = "已发送";
        tipText = "正在为您发送项目";
//        return;
    }
    //$("#operate_status_" + itemIds).next().attr("disabled", true);
    var loadi = layer.load("正在为您操作，请稍后...");
    setTimeout(function() {
        jQuery.post(url,
            {itemIds: itemIds, companyIds: companyIds, operate: operate, projectId: editid},
            function (data) {
                var result = JSON.parse(data);
                if (result.result == "success") {
                    var ids = "";
                    try {
                        ids = itemIds.split(",");
                        for (var i = 0; i < ids.length; i++) {
                            var id = ids[i];
                            $("#operate_status_" + id).html(text);
                            $("#operate_status_" + id).next().attr("disabled", true);
                            selcheckbox(id);
                        }
                    } catch (e) {
                        $("#operate_status_" + itemIds).html(text);
                        //                    $("#recommendItemId_" + itemIds).remove();
                    }
                    layer.msg('操作成功.', 2, {type: 9}); //风格二
                    $("#operate_status_" + itemIds).next().attr("disabled", true);
                    selcheckbox(itemIds);
                }
                else {
                    layer.msg('发送超时，请重新发送.', 2, {type: 3}); //风格二
                }
                layer.close(loadi);
                //            $("#operate_status_" + itemIds).next().attr("disabled", false);
            });
    }, 2000);
}

function bankingGenuisExcute(val, ptodId) {
    if (val == "") return;
    var tipText = "";
    switch (parseInt(val)) {
        case 1:
            tipText = "已发送";
            break;
        case 2:
            tipText = "已移除";
            break;
        case 3:
            tipText = "签订NDA";
            break;
        case 4:
            tipText = "签订TS";
            break;
        case 5:
            tipText = "交割";
            break;
    }
    var url = "/sales/bankingGenuisExcute";
    $("#recommendItemControlSelectId_" + ptodId).attr("disabled", true);
    var loadi = layer.load("正在为您操作，请稍后...");
    setTimeout(function() {
        jQuery.post(url,
            {ptodId: ptodId, operate: val},
            function (data) {
                if (data == "success") {
                    $("#recommendItemControlId_" + ptodId).html(tipText);
                    layer.msg('操作成功.', 2, {type: 9}); //风格二
                }
                else {
                    layer.msg('发送超时，请重新发送.', 2, {type: 3}); //风格二
                }
                $("#recommendItemControlSelectId_" + ptodId).attr("disabled", false);
                layer.close(loadi);
            });
    }, 2000);
}

jQuery("#is_agent_project").click(function() {
    if (jQuery(this).prop("checked")) {
        jQuery(".is_agent_project_").show();
    }
    else {
        jQuery(".is_agent_project_").hide();
    }
});

$("input[name='is_suitor']:radio").click(function() {
    if ($(this).val() == "3")
        $("#btn_confirm").prop("disabled", true);
    else
        $("#btn_confirm").prop("disabled", false);
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

$(".step_btn_publish").click(function() {
    var index = $(".step_btn_publish").index($(this));
    if (index == 5) return;
    var curr_step = $("#curr_step").val();
    if (curr_step == "") curr_step = 0;
    //if (curr_step >= index) showStep(index);
    showStep(index);
});

function showStep(index) {
    if (parseInt(index) > 0) {
        var preIndex = parseInt(index) - 1;
        var editid = $("#edit_id").val();
        if (!checkMustEnter(preIndex)) {
//            custom_alert("你的项目信息未填写完整，请先补全项目信息");
            showStep(preIndex);
            return;
        }
        if (editid == "" && parseInt(index) > 0)
            index = 0;
        else if (($("#company_industry_0").val() == "" || $("#project_keyword").val() == "") && parseInt(index) > 1)
            index = 1;
        else if ($("#curr_project_status").val() == "4" && parseInt(index) > 2)
            index = 2;
    }
    switch (index) {
        case 0:
            $("#btn_save").addClass("hide_");
            $("#btn_next").removeClass("hide_");
            $("#btn_cancel").removeClass("hide_");
            $(".project_status_area").addClass("hide_");
            break;
        case 1:
            $("#btn_save").addClass("hide_");
            $("#btn_next").removeClass("hide_");
            $("#btn_cancel").addClass("hide_");
            $(".project_status_area").addClass("hide_");
            break;
        case 2:
            $("#btn_next").addClass("hide_");
            $("#btn_cancel").addClass("hide_");
            $("#btn_save").removeClass("hide_");
            $(".project_status_area").addClass("hide_");
            break;
        case 3:
            $("#btn_save").addClass("hide_");
            $("#btn_next").addClass("hide_");
            $("#btn_cancel").addClass("hide_");
            $(".project_status_area").removeClass("hide_");
//            $(".table_recommend_1").children().not(":first").remove();
            if (page == 0 && dealGenuisCount == 0) {
                //Terry
                loadPotentialCount();
                loadRecommedn1();
            }
            break;
        case 4:
            $("#btn_save").addClass("hide_");
            $("#btn_next").addClass("hide_");
            $("#btn_cancel").addClass("hide_");
            $(".project_status_area").removeClass("hide_");
            page2 = 0;
            $(".table_recommend_2").children().not(":first").remove();
            loadRecommedn2();
            break;
        case 88:
            $("#btn_save").addClass("hide_");
            $("#btn_next").addClass("hide_");
            $("#btn_cancel").addClass("hide_");
            $(".project_status_area").removeClass("hide_");
            index = 3;
//            $(".table_recommend_1").children().not(":first").remove();
            break;
    }
    $(".step_btn_publish").removeClass("curr");
    $(".step_btn_publish").eq(index).addClass("curr");
    $(".step_class").addClass("hide_");
    $(".step_class").eq(index).removeClass("hide_");
    var curr_step = $("#curr_step").val();
    if (curr_step == "") curr_step = 0;
    $(".step_btn_publish").each(function(i) {
        if (index >= i && curr_step >= i) {
            $(this).addClass("over");
        }
        else {
            return false;
        }
    });
    if (curr_step < index)
        $("#curr_step").val(parseInt(curr_step) + 1);
}

function getCurrStep() {
    var index = 0;
    $(".step_btn_publish").each(function(i) {
        if ($(this).hasClass("curr")) {
            index = i;
            return false;
        }
    });
    return index;
}

$("#btn_next").click(function() {
    var index = getCurrStep();
    if (index == 0) {
        if (!checkMustEnter(index)) return;
    }
    if (!checkProjectStage()) return;
    $(".alert_message").remove();
    $(this).prop("disabled", true);
    $("#submitStatus").val("draft");
    $("#need_match").val(0);
	$("#formData").ajaxSubmit({
	    type: 'post',
	    dataType: 'json',
	    success: function(data) {
            if (data.result == "success") {
                $("#edit_id").val(data.id);
                $(".project_title").text(data.project_title);
                if (index < 4) {
                    showStep(index + 1);
                }
            }
            else {
                if (data.message == "demandExsit")
                    errorMessages("该需求名称已存在，请调整");
                else if (data.message == "projectExsit")
                    errorMessages("该项目名称已存在，请调整");
                else if (data.message == "symbolNotExsit")
                    errorMessages("请确认您填写的上市公司代码是否正确");
                else if (data.message == "typeError")
                    errorMessages("只允许提交后缀为doc、docx和pdf文件的附件");
                else if (data.message == "tooBig")
                    errorMessages("文件大小不能大于20兆");
                else
                    errorMessages("提交项目出错，请稍后再试，或联系管理员，谢谢");
                $(".alert_message").removeClass("hide_");
            }
            $("#btn_next").prop("disabled", false);
	    }
	});
});

$("#btn_back").click(function() {
    showStep(0);
});

var pagePushArea;
var emailPagePushArea;
var pageDetail;
$("#btn_save").click(function() {
    $("#need_match").val(1);
    pagePushArea = $.layer({
        type: 1,
        shade: [0],
        area: ['auto', 'auto'],
        title: false,
        border: [0],
        shade: [0.3, '#000'],
        closeBtn: [0, false], //去掉默认关闭按钮
        page: {dom : '.push_area'}
    });
});

$('#popColseBtn').on('click', function(){
    layer.close(pagePushArea);
});

$("#btn_open_outlook").click(function() {
    emailPagePushArea = $.layer({
        type: 1,
        shade: [0],
        area: ['auto', 'auto'],
        title: "发送Teaser给外部用户",
        border: [0],
        closeBtn: [0, true], //去掉默认关闭按钮
        btns:2,
        btn: ['确定', '取消'],
        yes: function() {
            v_send_extend_email = true;
            emailReview();
        },
        /*no: function(){

        },*/
        page: {dom : '.email_area'}
    });
});

function send_extenal_email() {
    var url = "/sales/send_extenal_email";
    var editid = $("#edit_id").val();
    var other_email = $("#other_email").val();
    if (other_email.trim() == "") return;
    var loadi = layer.load('邮件发送中，请稍等.', 23);
    jQuery.post(url,
        {id:editid, other_email: other_email}, function(data) {
            if (data == "success") {
                $("#other_email").val("");
                layer.close(emailPagePushArea);

                layer.close(loadi);
                layer.msg('邮件发送成功.', 3, {type:9}); //风格二
            }
            else if (data == "not approved") {
                layer.close(loadi);
                layer.msg('您的项目还未审核通过，无法使用此功能.', 3, {type:9}); //风格二
            }
            else {
                layer.close(loadi);
                layer.msg('邮件超时，请重新发送.', 3, {type:3}); //风格二
            }
    });
}

$('#email_popColseBtn').on('click', function(){
    layer.close(emailPagePushArea);
});

$("#btn_confirm").click(function() {
    $("#submitStatus").val("pending");
    $("#btn_confirm").prop("disabled", true);
    $("#curr_project_status").val("1");
    endSave(function(bool) {
        $("#btn_confirm").prop("disabled", false);
        if (bool) {
            layer.close(pagePushArea);
            var editid = $("#edit_id").val();
            if (editid == "") return;
            dealGenuisCount = 1;
            showStep(3)
            $(".view-more-recommond_1").before('<table class="col-xs-12 deal_genius_counting_div"><tr><td width="150"></td><td><br/><div class="progress"><div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div></div></td><td width="150"></td></tr><tr><td width="150"></td><td align="center">正在为您匹配最适合您的投资机构，请耐心等待&nbsp;<span id="progress-rate">0%</span></td><td width="150"></td></tr></table>');
            counting();
            $(".view-more-recommond_1").addClass("hide_");
            var url = "/sales/sync_recommond";
            jQuery.post(url,
                {id:editid}, function(data) {
                    if (data == "success") {
                        $(".progress-bar-info").width("100%");
                        $("#progress-rate").html("100%");
                        $(".deal_genius_counting_div").remove();
                        $(".view-more-recommond_1").removeClass("hide_");
                        dealGenuisCount = 0;
                        showStep(3);
                        clearCounting();
                    }
            });
//            var loadi = layer.load('正在为您匹配最适合您的投资机构，请耐心等待');
//            var editid = $("#edit_id").val();
//            if (editid == "") return;
//            var url = "/sales/sync_recommond";
//            jQuery.post(url,
//                {id:editid}, function(data) {
//                    if (data == "success") {
//                        showStep(3);
//                    }
//                    layer.close(loadi);
//            });
        }
    });
});

var countTime ;
var processInt = 1;
function counting() {
    processInt ++;
    var times = 600;
    if (processInt >= 99) {
        return;
    }
    else if (processInt >= 95) {
        times = 6000;
    }
    else if (processInt >= 75) {
        times = 3000;
    }
    else if (processInt >= 50) {
        times = 1000;
    }
    //if (processInt >= 100) processInt = 1;
    $(".progress-bar-info").width(processInt + "%");
    $("#progress-rate").html(processInt + "%");
    countTime = setTimeout("counting()", times);
}

function clearCounting() {
    clearTimeout(countTime);
}

function initEdit() {
    var status = $("#status").val();
    if (status != "" && status > 0)
        showStep(parseInt(status));
    else
        showStep(0)
}
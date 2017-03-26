$(function() {
    $(".industry2").click(function() {
        var name = $(this).attr("data-name")
        var id = $(this).val();
        var parentId = $(this).attr("data-parent-id");
        if ($(this).prop("checked"))
            mergreIndustryShow(id, name, parentId);
        else
            $("#child_industry_" + id).remove();
        checkChildIsAllChecked(parentId);
    });

    $(".industry1").click(function() {
        var id = $(this).val();
        if ($(this).prop("checked")) {
            mergreIndustryShow("", "", id);
            makeAllChildChecked(id);
        }
        else {
            $("#parent_industry_" + id).remove();
            makeAllChildUnChecked(id);
        }
    });

    $(".setting_plus").click(function() {
        var html = $(this).text();
        if (html == " + ") {
            $(this).text(" - ");
            $(this).next().next().show();
        }
        else {
            $(this).text(" + ");
            $(this).next().next().hide();
        }
    });

    function checkChildIsAllChecked(parentId) {
        var bool = true;
        $("#parent-"+parentId).find(".industry2").each(function() {
            if (!$(this).prop("checked")) {
                bool = false;
                return false;
            }
        });
        if (bool)
            $("#industry1-"+parentId).prop("checked", true);
        else
            $("#industry1-"+parentId).prop("checked", false);
    }

    function makeAllChildChecked(parentId) {
        $("#parent-"+parentId).find(".industry2").each(function() {
            $(this).prop("checked", true);
            var childId = $(this).attr("data-name");
            var childName = $(this).attr("data-name");
            mergreIndustryShow(childId, childName, parentId);
        });
    }

    function makeAllChildUnChecked(parentId) {
        $("#parent-"+parentId).find(".industry2").each(function() {
            $(this).prop("checked", false);
            var childId = $(this).attr("data-name");
            $("#child_industry_" + childId).remove();
        });
    }

    function getParentIndustryName(id) {
        var name = "";
        $(".industry1").each(function() {
            if (id == $(this).val()) {
                name = $(this).attr("data-name");
                return false;
            }
        });
        return name;
    }

    function mergreIndustryShow(industry_2, industry_2_name, industry_1) {
        if (industry_1 == "") return;
        var parId = "parent_industry_" + industry_1;
        if (!isObjectExsit(parId)) {
            industry_1_name = getParentIndustryName(industry_1);
            var parHtml = "<div id='" + parId + "'>"+ industry_1_name +"<input type='hidden' name='industry_1' value='" + industry_1 + "'></div>";
            $("#target_industry").append(parHtml)
        }
        if (industry_2 != "") {
            if (isObjectExsit(parId)) {
                var childId = "child_industry_" + industry_2;
                if (!isObjectExsit(childId)) {
                    var childHtml = " <span id='" + childId + "'>" + industry_2_name + "<input type='hidden' name='industry_2' value='" + industry_2 + "'></span>";
                    if (!isChildeExsit(parId)) childHtml = " |" + childHtml;
                    $("#" + parId).append(childHtml);
                }
            }
        }
    }

    $('input[name="industrys"]').each(function() {
        if ($(this).hasClass("industry1")) {
            var id = $(this).val();
            if ($(this).prop("checked"))
                mergreIndustryShow("", "", id);
        }
        else if ($(this).hasClass("industry2")) {
            var name = $(this).attr("data-name")
            var id = $(this).val();
            var parentId = $(this).attr("data-parent-id");
            if ($(this).prop("checked"))
                mergreIndustryShow(id, name, parentId);
        }
    });

    $("#intro_cn_").keyup(function() {
        var val = $(this).val();
        $("#intro_cn").val(val.replace(/\n/g, "<br/>"));
    });

    $("#uploadFile").fileupload({
        url:"/services/upload_file",//文件上传地址，当然也可以直接写在input的data-url属性内
        dataType: 'text',
        acceptFileTypes:  /(\.|\/)(gif|jpe?g|png)$/i,
        done: function (e, data) {
            result = jQuery.parseJSON(data.result);
            if (result.status == "success") {
                $("#img_thumbnail").attr("src", result.path);
                $("#imgName").val(result.imgName);
                $("#img_thumbnail").width("");
                $("#img_thumbnail").height("");
                width = result.imgWidth;
                height = result.imgHeight;
                if (width > height)
                    $("#img_thumbnail").width(228);
                else
                    $("#img_thumbnail").height(228);
                initJcrop();
            }
            else {
                alert(result.message);
            }
            $("#selectFileButton").show();
            $("#selectFileUploading").hide();
        },
        progressall: function (e, data) {
        }
    });

    var jcrop_api;
    xsize = 180;//$pcnt.width(),
    ysize = 180;//$pcnt.height();

    function updateImgParam(c) {
        if (parseInt(c.w) > 0) {
            $('#x1').val(c.x);
            $('#y1').val(c.y);
            $('#x2').val(c.x2);
            $('#y2').val(c.y2);
            $('#w').val(c.w);
            $('#h').val(c.h);
        }
    }

    function initJcrop() {
        try {jcrop_api.destroy();}catch(e){}
        $('#img_thumbnail').Jcrop({
            onRelease: releaseCheck,
            onChange: updateImgParam,
            onSelect: updateImgParam,
            aspectRatio: xsize / ysize
        },function(){
            jcrop_api = this;
            var w = $("#img_thumbnail").width();
            var h = $("#img_thumbnail").height();
            $("#imgWidth").val(w);
            $("#imgHeight").val(h);
            var init_w = 0;
            var init_h = 0;
            if (w > h) {
                init_w = (300 - h) / 2;
                xsize = h;
                ysize = h;
            }
            else {
                init_h = (300 - w) / 2;
                xsize = w;
                ysize = w;
            }
            jcrop_api.animateTo([init_w, init_h, w, h]);
        });
    };
    function releaseCheck() {
        jcrop_api.setOptions({ allowSelect: true });
    };
});

jQuery('#target_company_industry_0').change(function() {
    var val = jQuery(this).val();
    if (val == "0" || val == "") return;
    industrySelect("target_company_industry_1", val);
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

function addKeyword2() {
    var name = jQuery("#key_keyword").val();
    if (name == "") return;
    if (!isObjectExsit("target_keyword_" + name)) {
        var html = "<span id='target_keyword_" + name + "' class='alert alert-info preference_selected'><a href='###'>" + name +
                   "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove project_key_remove' ref='"+name+"'></a></span>";
        jQuery("#target_keywords").append(html);
        var val = jQuery("#project_keyword").val();
        if (val == "")
            val = name;
        else
            val += "," + name;
        jQuery("#project_keyword").val(val);
        jQuery("#key_keyword").val("")
    }
}

function isObjectExsit(id) {
    return $("#"+id).length > 0;
}

function isChildeExsit(id) {
    return $("#"+id).children().length > 1;
}

var pagePushArea;
$(".add_industry").click(function() {
    pagePushArea = $.layer({
        type: 1,
        shade: [0],
        area: ['750px', '400px'],
        title: false,
        border: [1],
        shade: [0.3, '#000'],
        page: {dom : '.setting_area'}
    });
});

function goback() {
    history.back();
}
/*
jQuery(".btn-default").click(function() {
    goback();
})
*/
function DoDelete(url, id) {
    if (confirm("Are you confirm remove this information?")) {
        jQuery.post(
            url, {id:id},
            function (msg) {
                if (msg == "success") {
                    alert("Operation success!");
                    location.reload();
                }
                else {
                    alert("Remove error, Please contact the administrator!");
//                    alert(msg);
                }
            },
            "text"
        );
        /*$.ajax({
            type: "post",
            url: url,
            data: {id : id},
            success: function (data, status) {
                if (data == "success") {
                    alert("Operation success!")
                    location.reload();
                }
                else
                    alert("Remove error, Please contact the administrator!")
            },
            error: function() {

            }
        });*/
    }
}

function LoadProvinces(element,country_id,value)
    {
        if(country_id>0 && country_id != "")
        {
            jQuery("#box_"+element).hide();
            jQuery("#"+element).empty();
            jQuery("#"+element).append("<option value=''>Loading...</option>");
            jQuery("#"+element).trigger("chosen:updated");
            var url = "/area/get_provinces/"+country_id;
            jQuery.getJSON(url,function(data)
            {
                var count = data.length;
                if(count>0)
                {
                    jQuery("#box_"+element).show();
                    jQuery("#"+element).empty();
                    jQuery("#"+element).append("<option value=''>Please Select</option>");
                    for(var k in data)
                    {
                        var id = data[k].pk;
                        var name = data[k].fields.name_cn;
                        //console.log(id);
                        //console.log(name);
                        if (id == value) {
                            jQuery("#"+element).append("<option value='" + id + "' selected=\"selected\">" + name + "</option>");
                        } else {
                            jQuery("#"+element).append("<option value='" + id + "'>" + name + "</option>");
                        }
                    }
                    jQuery("#"+element).trigger("chosen:updated");
                }
            });
        }
    }
function LoadCities(element,province_id,value)
    {
        if(province_id>0 && province_id != "")
        {
            jQuery("#box_"+element).hide();
            jQuery("#"+element).empty();
            jQuery("#"+element).append("<option value=''>Loading...</option>");
            jQuery("#"+element).trigger("chosen:updated");
            var url = "/area/get_cities/"+province_id;
            jQuery.getJSON(url,function(data)
            {
                var count = data.length;
                if(count>0) {
                    jQuery("#box_"+element).show();
                    jQuery("#" + element).empty();
                    jQuery("#" + element).append("<option value=''>Please Select</option>");
                    for (var k in data) {
                        var id = data[k].pk;
                        var name = data[k].fields.name_cn;
                        //console.log(id);
                        //console.log(name);
                        if (id == value) {
                            jQuery("#" + element).append("<option value='" + id + "' selected=\"selected\">" + name + "</option>");
                        } else {
                            jQuery("#" + element).append("<option value='" + id + "'>" + name + "</option>");
                        }
                    }
                    jQuery("#" + element).trigger("chosen:updated");
                }
            });
        }
    }

jQuery('#regionlevelone').change(function(){
    LoadRegionLevelTwo('#regionleveltwo', jQuery(this).val(), '');
    LoadRegionLevelThree('#regionlevelthree', jQuery('#regionleveltwo').val(), '');
});
jQuery('#regionleveltwo').change(function(){
    LoadRegionLevelThree('#regionlevelthree', jQuery(this).val(), '');
});


function LoadRegionLevelTwo( element, regionlevelone_id, regionleveltow_id){
    var $element = $(element);
    $element.find('option[value!=""]').remove();
    if ( parseInt(regionlevelone_id) > 0) {
        $.getJSON('/area/get_regionleveltwo/' + regionlevelone_id,
            function(data){
                data.forEach(function(v, i){
                    var $option = $('<option>').val(v.pk).text(v.fields.name_cn);
                    $element.append($option);
                });
                $element.trigger('chosen:updated');
            }
        )
    }
}
function LoadRegionLevelThree( element, regionleveltwo_id, regionlevelthree_id){
    var $element = $(element);
    $element.find('option[value!=""]').remove();
    if ( parseInt(regionleveltwo_id) > 0) {
        $.getJSON('/area/get_regionlevelthree/' + regionleveltwo_id,
            function(data){
                data.forEach(function(v, i){
                    var $option = $('<option>').val(v.pk).text(v.fields.name_cn);
                    $element.append($option);
                    $element.trigger('chosen:updated');
                });
            }
        )
    }
}
function RemoveCompanyFile(id)
{
    if(confirm('Are you confirm remove this file?'))
    {
        var url = "/member/companies/remove_file";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
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
                alert(data);
            }
        });
    }
}

function RemoveProjectFile(id) {
    if(confirm('Are you confirm remove this file?'))
    {
        var url = "/project/removeFile";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function ApproveProject(id) {
    if(confirm('Are you confirm approve this project?'))
    {
        var url = "/project/approve";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function BanProject(id) {
    if(confirm('Are you confirm ban this project?'))
    {
        var url = "/project/ban";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}


function ApproveDemand(id) {
    if(confirm('Are you confirm approve this demand?'))
    {
        var url = "/demand/approve";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function BanDemand(id) {
    if(confirm('Are you confirm ban this demand?'))
    {
        var url = "/demand/ban";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function industrySelect(selectId, parentId, value_selected,fun_) {
    //var url = "{% url 'industry.json' 0 %}";
    var value_selected = arguments[2];
    jQuery("#" + selectId).empty();
    jQuery("#" + selectId).append("<option value='0'>Loading...</option>");
    jQuery("#" + selectId).trigger("chosen:updated");
    var url = "/industry/json/" + parentId;
    var opt = "";
    jQuery.getJSON(url, function(data) {
        if (data.length > 0) {
            jQuery("#" + selectId).parent().show();
        }
        jQuery("#" + selectId).empty();
        jQuery("#" + selectId).append("<option value='0'>Please Select</option>");
        jQuery.each(data, function(key, value) {
            if(value.pk == value_selected)
            {
               opt += "<option value='" + value.pk + "' selected>"+value.fields.name_cn+"</option>";
            }else
            {
                opt += "<option value='" + value.pk + "'>"+value.fields.name_cn+"</option>";
            }
            //opt += "<option value='" + value.pk + "'>"+value.fields.name_en+"</option>";
        });
        jQuery("#" + selectId).append(opt);
        jQuery("#" + selectId).trigger("chosen:updated");
        try {
            fun_();
        } catch (e){}
    });
}



function addIndustry(id, pre) {
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
}

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

function DoSendmail(id) {
    if(confirm('Are you confirm send this mail?'))
    {
        var url = "/member/members/sendmail";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function DoSendNoreadMessagemail(id) {
    if(confirm('Are you confirm send this mail?'))
    {
        var url = "/analysis/send_message_noread_mail";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}


function DoSendNologinMessagemail(id) {
    if(confirm('Are you confirm send this mail?'))
    {
        var url = "/analysis/send_message_nologin_mail";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function DoSendNopublishMessagemail(id) {
    if(confirm('Are you confirm send this mail?'))
    {
        var url = "/analysis/send_message_nopublish_mail";
        jQuery.post(url,{id:id},function(data){
            if(data=="success")
            {
               location.reload();
            }else
            {
                alert(data);
            }
        });
    }
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

function SetRecommendProject(id)
{
    if(confirm("确定推荐?"))
    {
        var url = "/project/setRecommend";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function CancelRecommendProject(id)
{
    if(confirm("确定取消推荐?"))
    {
        var url = "/project/cancelRecommend";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function SetTopProject(id)
{
    if(confirm("确定置顶?"))
    {
        var url = "/project/setTop";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function CancelTopProject(id)
{
    if(confirm("确定取消置顶?"))
    {
        var url = "/project/cancelTop";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function SetRecommendDemand(id)
{
    if(confirm("确定推荐?"))
    {
        var url = "/demand/setRecommend";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function CancelRecommendDemand(id)
{
    if(confirm("确定取消推荐?"))
    {
        var url = "/demand/cancelRecommend";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function SetTopDemand(id)
{
    if(confirm("确定置顶?"))
    {
        var url = "/demand/setTop";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function CancelTopDemand(id)
{
    if(confirm("确定取消置顶?"))
    {
        var url = "/demand/cancelTop";
        jQuery.post(url,{id:id},function(data) {
            if(data=="success")
            {
                location.reload();
            }else
            {
                alert(data);
            }
        });
    }
}

function getTransferVal(val) {
    val = parseInt(val);
    switch (val) {
        case 0:
            return 0;
            break;
        case 1000000000:
            return 5000000;
            break;
        case 2000000000:
            return 10000000;
            break;
        case 3000000000:
            return 20000000;
            break;
        case 4000000000:
            return 50000000;
            break;
        case 5000000000:
            return 1000000000;
            break;
        case 6000000000:
            return 3000000000;
            break;
        case 7000000000:
            return 5000000000;
            break;
        case 8000000000:
            return 10000000000;
            break;
        case 9000000000:
            return 50000000000;
            break;
        case 10000000000:
            return 100000000000;
            break;
    }
}

function getCurrentCurrency() {
    var currency = parseInt($("#deal_currency").val());
    return handleCurrentCurrency(currency);
}

function handleCurrentCurrency(currency) {
    currency = parseInt(currency);
    var unit = "¥";
    switch (currency) {
        case 1:
            unit = "¥";
            break;
        case 2:
            unit = "$";
            break;
        case 3:
            unit = "€";
            break;
    }
    return unit;
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

function autoSlider(id, min, max) {
    var unit = getCurrentCurrency();
	$( "#rangeSlider" + id ).slider({
		range: true,
		min: 0,
		max: 10000000000,
        step:1000000000,
		values: [ min, max ],
		slide: function( event, ui ) {
            var unit = getCurrentCurrency();
            var minVal = ui.values[ 0 ];
            var maxVal = ui.values[ 1 ];
            minVal = getTransferVal(minVal);
            maxVal = getTransferVal(maxVal);
            $("#member_range_mins_" + id).val(minVal);
            $("#member_range_maxs_" + id).val(maxVal);
            minVal = transfer2Currency(minVal);
            maxVal = transfer2Currency(maxVal);
			$("#amount" + id ).text ( unit + "" + minVal + " - " + unit + maxVal );
		}
	});
	$( "#amount" +id ).text( unit + transfer2Currency(min) + " - " + unit + transfer2Currency(max) );
}

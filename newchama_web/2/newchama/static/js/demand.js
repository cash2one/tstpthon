    /*jQuery(".customClose").live("click", function() {
         jQuery(this).parent().remove();
    });
    jQuery(".chosen-select").chosen({'width':'100%','white-space':'nowrap'});
    jQuery('#expire_date').datepicker({dateFormat:'yy-mm-dd'});
    jQuery("#country").change(function(){
        LoadProvinces('province',jQuery(this).val(),0);
    });
    jQuery("#province").change(function(){
        var province_id=jQuery(this).val();
        LoadCities('city',province_id,0);
    });
    function ShowTickerBox()
    {
        jQuery("#box_ticker").show();
    }
    function HideTickerBox()
    {
        jQuery("#box_ticker").hide();
    }
    function ShowAuditCompanyBox()
    {
        jQuery("#box_audit_company").show();
    }
    function HideAuditCompanyBox()
    {
        jQuery("#box_audit_company").hide();
    }
    function ShowSuitorBox()
    {
        jQuery(".suitor").show();
    }
    function HideSuitorBox()
    {
        jQuery(".suitor").hide();
    }
    jQuery("#checkbox_Listed_company").click(function()
    {
        var isChecked = (jQuery(this).attr("checked")=="checked");
        if(isChecked){
            ShowTickerBox();
        }else
        {
            HideTickerBox();
        }
    });
    jQuery("#checkbox_Audited_financial_report").click(function()
    {
        var isChecked = (jQuery(this).attr("checked")=="checked");
        if(isChecked){
            ShowAuditCompanyBox();
        }else
        {
            HideAuditCompanyBox();
        }
    });
    jQuery("#is_suitor").click(function()
    {
        var isChecked = (jQuery(this).attr("checked")=="checked");
        if(isChecked){
            ShowSuitorBox();
        }else
        {
            HideSuitorBox();
        }
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
                label: item.fields.stock_symbol + ":" +
                   item.fields.short_name_en,
                id: item.pk
              };
            })
           response(data);
          }
        });
      },
      minLength: 2,
      select: function( event, ui ) {
        SelectedListedCompany(ui.item.id);
      }
    });
     function SelectedListedCompany(id)
        {
            var url = "/repository/get_listed_company/"+id;
            jQuery.getJSON(url,function(data)
            {
                var count = data.length;
                if(count>0) {
                    //company_name = data[0].fields.name_cn;
                    country = data[0].fields.country;
                    province = data[0].fields.province;
                    city = data[0].fields.city;
                    industry = data[0].fields.industry;
                    //jQuery("#company").val(company_name);
                    if(country>0) {
                        jQuery("#country").val(country);
                        jQuery("#country").trigger("chosen:updated");
                    }
                    if(province>0)
                    {
                        LoadProvinces("province",country,province);
                    }
                    if(city>0) {
                        LoadCities("city",province,city);
                    }
                    if(industry>0)
                    {
                        var url_get_industry = "/industry/get/"+industry;
                        jQuery.getJSON(url_get_industry,function(data_industry){
                            var industry_id = data_industry.id;
                            var industry_level = data_industry.level;
                            var industry_father_id = data_industry.father_id;
                            var industry_father_father_id = data_industry.father_father_id;
                            switch(industry_level)
                            {
                                case 1:
                                    industrySelect("industry_first",0,industry_id);
                                    break;
                                case 2:
                                    industrySelect("industry_first",0,industry_father_id);
                                    industrySelect("industry_second",industry_father_id,industry_id);
                                    break;
                                case 3:
                                    industrySelect("industry_first",0,industry_father_father_id);
                                    industrySelect("industry_second",industry_father_father_id,industry_father_id);
                                    industrySelect("industry_third",industry_father_id,industry_id);
                                    break;
                            }
                        });
                    }
                }
            });
        }

    $("#company_name" ).autocomplete({
      source: function( request, response ) {
        $.ajax({
          url: "/member/companies/autocomplete_search/"+request.term,
          dataType: "json",
          success: function( jsonResponse ) {
             var data = $(jsonResponse).map(function(id,item) {
              return {
                value: item.fields.short_name_en,
                label: item.fields.short_name_en + ":" +
                   item.fields.name_en,
                id: item.pk
              };
            })
           response(data);
          }
        });
      },
      minLength: 2,
      select: function( event, ui ) {
        AddCompany(ui.item.id,ui.item.value );
      }
    });

    $("#member_email").autocomplete({
        source: function(request, response)
        {
            $.ajax({
                url: "/member/members/autocomplete_search/"+request.term,
              dataType: "json",
              success: function( jsonResponse ) {
                  var data = $(jsonResponse).map(function (id, item) {
                      return {
                          value: item.fields.email,
                          label: item.fields.first_name +
                                  item.fields.last_name + ":" +item.fields.email,
                          id: item.pk
                      };
                  })
                  response(data);
              }
            });
        },
        minLength: 2
    });

    function AddMember(id, name) {
       var tagId = "member_id_"+id;
       var tagName = "member_id";
        console.log(id);
        if (!IsMemberAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_member").append(html);
        }else
        {
            alert("added");
        }
    }

    $("#select_member_email").autocomplete({
        source: function(request, response)
        {
            $.ajax({
                url: "/member/members/autocomplete_search/"+request.term,
              dataType: "json",
              success: function( jsonResponse ) {
                  var data = $(jsonResponse).map(function (id, item) {
                      return {
                          value: item.fields.email,
                          label: item.fields.first_name +
                                  item.fields.last_name + ":" +item.fields.email,
                          id: item.pk
                      };
                  })
                  response(data);
              }
            });
        },
        minLength: 2,
        select: function( event, ui ) {
        AddMember(ui.item.id,ui.item.value);
        }
    });

    function AddCompany(id, name) {
        var tagId = "company_id_"+id;
        var tagName = "company_name";
        console.log(id);
        if (!IsCompanyAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_company").append(html);
        }else
        {
            alert("added");
        }
    }

    function IsCompanyAdded(id) {
        return (jQuery("#company_id_"+id).val()!==undefined);
    }
    function IsMemberAdded(id) {
        return (jQuery("#member_id_"+id).val()!==undefined);
    }
    function AddCountry(sel){
        var id = jQuery("#"+sel).val();
        var name = jQuery("#"+sel+" option:selected").text();
        var tagId = "country_id_"+id;
        var tagName = "country";
        if(id=="0"||id==""||id===undefined)
        {
            alert("please select");
            return;
        }
        if (!IsCountryAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_location").append(html);
        }else
        {
            alert("added");
        }
    }
    function IsCountryAdded(id)
    {
        return (jQuery("#country_id_"+id).val()!==undefined);
    }
    function AddProvince(sel){
        var id = jQuery("#"+sel).val();
        var name = jQuery("#"+sel+" option:selected").text();
        var tagId = "province_id_"+id;
        var tagName = "province";
        if(id=="0"||id=="")
        {
            alert("please select");
            return;
        }
        if (!IsProvinceAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_location").append(html);
        }else
        {
            alert("added");
        }
    }
    function IsProvinceAdded(id)
    {
        return (jQuery("#province_id_"+id).val()!==undefined);
    }
    function AddCity(sel){
        var id = jQuery("#"+sel).val();
        var name = jQuery("#"+sel+" option:selected").text();
        var tagId = "city_id_"+id;
        var tagName = "city";
        if(id=="0"||id=="")
        {
            alert("please select");
            return;
        }
        if (!IsProvinceAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_location").append(html);
        }else
        {
            alert("added");
        }
    }
    function IsCityAdded(id)
    {
        return (jQuery("#city_id_"+id).val()!==undefined);
    }
    function AddIndustry(sel)
    {
        var id = jQuery("#"+sel).val();
        var name = jQuery("#"+sel+" option:selected").text();
        var tagId = "industry_id_"+id;
        var tagName = "industry";
        if(id=="0"||id=="")
        {
            alert("please select");
            return;
        }
        if (!IsIndustryAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_industry").append(html);
        }else
        {
            alert("added");
        }
    }
    function IsIndustryAdded(id)
    {
        return (jQuery("#industry_id_"+id).val()!==undefined);
    }
    function AddIndustrySuitor(sel)
    {
        var id = jQuery("#"+sel).val();
        var name = jQuery("#"+sel+" option:selected").text();
        var tagId = "industry_sutior_id_"+id;
        var tagName = "industry_sutior";
        if(id=="0"||id=="")
        {
            alert("please select");
            return;
        }
        if (!IsIndustrySuitorAdded(id)) {
            var html = "<span><input id='"+tagId+"' name='" + tagName + "' type='hidden' value='" + id +
                    "'/>" + name + "<a class='customClose'></a></span>";
            jQuery("#box_industry_suitor").append(html);
        }else
        {
            alert("added");
        }
    }
    function IsIndustrySuitorAdded(id)
    {
        return (jQuery("#industry_sutior_id_"+id).val()!==undefined);
    }

    industrySelect("industry_first", 0);
    jQuery('#industry_first').change(function() {
            var val = jQuery(this).val();
            industrySelect("industry_second", val);
    });

    jQuery('#industry_second').change(function() {
        var val = jQuery(this).val();
        industrySelect("industry_third", val);
    });
    industrySelect("industry_suitor_first", 0);
    jQuery('#industry_suitor_first').change(function() {
            var val = jQuery(this).val();
            industrySelect("industry_suitor_second", val);
    });

    jQuery('#industry_suitor_second').change(function() {
        var val = jQuery(this).val();
        industrySelect("industry_suitor_third", val);
    });

    function CheckDemand(id)
    {
        if(confirm("Are you sure approved?"))
        {
            var url = "/demand/check";
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
    function BanDemand(id)
    {
        if(confirm("Are you sure not approved?"))
        {
            var url = "/demand/ban";
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
    */



function addDestIndustry() {
    var id = jQuery("#industry_id").val();
    var name = jQuery("#industry_name").val();
    if (id == "0" || id == "") return;
    if (!isObjectExsit("dest_industry_" + id)) {
        var html = "<span id='dest_industry_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='industry' type='hidden' value='" + id + "'></span>";
        jQuery("#dest_industry").append(html);
    }
}

function addDestLocation() {
    var id = jQuery("#dest_country").val();
    var name = jQuery("#dest_country option:selected").text();
    if (id == "0" || id == "") return;
    if (!isObjectExsit("dest_country_" + id)) {
        var html = "<span id='dest_country_" + id + "' class='alert alert-info preference_selected'><a href='###'>" + name + "</a>&nbsp;<a href='###' data-dismiss='alert' class='glyphicon glyphicon-remove'></a>" +
            "<input name='country' type='hidden' value='" + id + "'></span>";
        jQuery("#dest_location").append(html);
    }
}

/*$("#btn_save").click(function() {
    var bool = true;
    $('.parsley-form').parsley('destroy');
    if ($('.parsley-form').parsley('validate')) {
        $("#submitStatus").val("pending");
        $('#formData').submit();
    }
});*/


$("#intro_cn_").keyup(function() {
    var val = $(this).val();
    $("#intro_cn").val(val.replace(/\n/g, "<br/>"));
});

$("#intro_en_").keyup(function() {
    var val = $(this).val();
    $("#intro_en").val(val.replace(/\n/g, "<br/>"));
});



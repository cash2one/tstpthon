

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
        if (!IsProvinceAdded(id)) {
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
        if (!IsProvinceAdded(id)) {
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
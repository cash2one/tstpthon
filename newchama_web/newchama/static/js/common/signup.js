
        $(document).ready(function() {
            /*$('#signup-mobile').iMask({
                type      : 'fixed',
                mask      : '99-99999999999',
                stripMask : true
            });
            $("#radio_is_listed_company").click(function () {
                if ($(this).prop("checked")) {
                    $('#stock_code_block').show();
                    $('#box_industry').show();
                } else {
                    $('#stock_code_block').hide();
                }
            });
            */
            $(".radio_isnot_listed_company").click(function () {
                if ($(this).prop("checked")) {
                    $("#ticker").attr("required", false);
                    $('#stock_code_block').hide();
                }
            });
            $(".radio_need_industry").click(function(){
                if($(this).prop("checked"))
                {
                    $("#industry_first").attr("required", true);
                    $('#box_industry').show();
                }
                if($(this).prop("checked") && $(this).val() == "1") {
                    $("#ticker").attr("required", true);
                    $('#stock_code_block').show();
                }
            });
            $(".radio_not_need_industry").click(function(){
                if($(this).prop("checked"))
                {
                    $("#industry_first").attr("required", false);
                    $('#box_industry').hide();
                }
            });
//{#            if ($("#radio_is_listed_company").prop("checked")) {#}
//{#                $('#stock_code_block').show();#}
//{#                $('#box_industry').show();#}
//{#            }#}

            var industry_id_first = $("#industry_id_first").val();
            var industry_id_second = $("#industry_id_second").val();
            var industry_id_third = $("#industry_id_third").val();
            if (industry_id_second||industry_id_first) {
                industrySelect("industry_second", industry_id_first,industry_id_second)
            }
            if (industry_id_third) {
                industrySelect("industry_third", industry_id_second,industry_id_third )
            }

            $("#btn_").click(function() {
                $('.account-form').parsley('destroy');
                if ($('.account-form').parsley('validate')) {
                    $('.account-form').submit();
                }
            });
        });

        $("#company" ).autocomplete({
            source: function( request, response ) {
                $.ajax({
                    url: "/services/get_active_companies/"+request.term,
                    dataType: "json",
                    success: function( jsonResponse ) {
                        var is_chinese = (get_template_lang() == "zh-cn");
                        var data;
                        if (is_chinese) {
                            data = $(jsonResponse).map(function (id, item) {
                                return {
                                    value: item.fields.name_cn,
                                    label: item.fields.name_cn,
                                    id: item.pk
                                };
                            });
                        }
                        else {
                            data = $(jsonResponse).map(function (id, item) {
                                return {
                                    value: item.fields.name_en,
                                    label: item.fields.name_en,
                                    id: item.pk
                                };
                            });
                        }
                        response(data);
                    }
                });
            },
            minLength: 2
            
        });

        $("#ticker" ).autocomplete({
            source: function( request, response ) {
                $.ajax({
                    url: "/services/get_listed_companies/"+request.term,
                    dataType: "json",
                    success: function( jsonResponse ) {
                        var is_chinese = (get_template_lang() == "zh-cn");
                        var data;
                        if (is_chinese) {
                            data = $(jsonResponse).map(function (id, item) {
                                return {
                                    value: item.fields.stock_symbol,
                                    label: item.fields.stock_symbol + ":" + item.fields.short_name_cn,
                                    id: item.pk
                                };
                            });
                        }
                        else {
                            data = $(jsonResponse).map(function (id, item) {
                                return {
                                    value: item.fields.stock_symbol,
                                    label: item.fields.stock_symbol + ":" + item.fields.short_name_en,
                                    id: item.pk
                                };
                            });
                        }
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
            var url = "/services/get_listed_company/"+id;
            jQuery.getJSON(url,function(data)
            {
                var count = data.length;
                if(count>0) {
                    company_name = data[0].fields.name_cn;
                    country = data[0].fields.country;
                    province = data[0].fields.province;
                    city = data[0].fields.city;
                    industry = data[0].fields.industry;
                    jQuery("#company").val(company_name);
                    if(country>0) {
                        jQuery("#country").val(country);
                    }
                    if(industry>0)
                    {
                        var url_get_industry = "/services/get_industry/"+industry;
                        jQuery.getJSON(url_get_industry,function(data_industry){
                            var industry_id = data_industry.id;
                            var industry_level = data_industry.level;
                            var industry_father_id = data_industry.father_id;
                            var industry_father_father_id = data_industry.father_father_id;
                            switch(industry_level)
                            {
                                case 1:
                                    industrySelect("industry_first",0,industry_id);
                                    $("#industry_id_first").val(industry_id);
                                    break;
                                case 2:
                                    industrySelect("industry_first",0,industry_father_id);
                                    industrySelect("industry_second",industry_father_id,industry_id);
                                    $("#industry_id_second").val(industry_id);
                                    $("#industry_id_first").val(industry_father_id);
                                    break;
                                case 3:
                                    industrySelect("industry_first",0,industry_father_father_id);
                                    industrySelect("industry_second",industry_father_father_id,industry_father_id);
                                    industrySelect("industry_third",industry_father_id,industry_id);
                                    $("#industry_id_third").val(industry_id);
                                    $("#industry_id_second").val(industry_father_id);
                                    $("#industry_id_first").val(industry_father_father_id);
                                    break;
                            }
                        });
                    }
                }
            });
        }
        //industrySelect("industry_first",0,0);
        jQuery('#industry_first').change(function() {
            var val = jQuery(this).val();
            if(val>0) {
                industrySelect("industry_second", val);
            }else
            {
                jQuery('#industry_second').parent().hide();
                jQuery('#industry_third').parent().hide();
            }
            //$("#box_industry_second").hide();
            //$("#box_industry_third").hide();
            //industrySelect("industry_second", val);
            $("#industry_id_first").val(val);
        });
        jQuery('#industry_second').change(function() {
            var val = jQuery(this).val();
            if(val>0) {
                industrySelect("industry_third", val);
            }else
            {
                jQuery('#industry_third').parent().hide();
            }
            //$("#box_industry_third").hide();
            //industrySelect("industry_third", val);
            $("#industry_id_second").val(val);
        });
        jQuery('#industry_third').change(function() {
            var val = jQuery(this).val();
            $("#industry_id_third").val(val);
        });
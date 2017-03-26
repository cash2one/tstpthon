$(document).ready( function() {
    $( "#start_time" ).datepicker();
    $( "#end_time" ).datepicker();
    $( "#deal_start_time" ).datepicker();
    $( "#deal_end_time" ).datepicker();

    var industry_ = parent.$("#industry").html();
    industry_ = industry_.replace("industry_demo", "industry_1");

    $(".check_events").click(function(){
        var $this = $(this);
        var newId = "new_" + $this.val();
        var bool = $this.prop("checked");
        if (!bool) {
            parent.$("#" + newId).remove();
        } else {
            if (parent.$("#" + newId).html() == "undefined"){
                return;
            }
            var $tr = $this.closest('tr');
            var stock_code = $tr.find('td:eq(3)').text().trim();
            var company_short_name = $tr.find('td:eq(4)').text().trim();
            var date = $tr.find('td:eq(6)').text().trim();
            var types = $tr.find('td:eq(7)').text().trim();
            var pdf_url = $tr.find('td:eq(8)').html();
            var href = $tr.find('td:eq(8)').find('a').attr('href');
            var content = $tr.find('td:eq(10)').find('div').text();
            var industry2_ = '<select name="industry_2" id="industry2_' + newId + '" data-placeholder="Please Choose..."></select>';
            var str_1="<tr id='" + newId + "'> <td>" + stock_code + "</td>" +  
            "          <td>" + company_short_name + "</td>" +
            "          <td>" + date + "<input type=hidden name=date value='" + date + "'></td>" +
            "          <td>" + types + "</td>" +
            "          <td>" + pdf_url + "<input type=hidden name=pdf_url value='" + href + "'></td>" +  
            "            <td><a href=\"javascript:;\" class=\"modify\" ref=\"" + newId + "\">修改</a>" +
            "            <a href=\"javascript:;\" class=\"cancel\">取消</a>" +
            " <div id='div_" + newId + "' class='modal fade' style='display:none'>" +
            "   <div class='modal-dialog modal-lg'>" +
            "     <div class='modal-content'>" +
            "       <div class='modal-body'>" +
            "            <table width='100%' border='0'>" +
            "              <tr>" +
            "                 <td width='20%'>公司简称</td> "+
            "                 <td><input type='text' name='company_short_name' value='" + company_short_name + "'style='width:200'> </td>" + 
            "                 <td width='20%'>股票代码</td> "+
            "                 <td><input type='text' name='stock_code' value='" + stock_code + "'style='width:200'> </td>" + 
            "              </tr>" +
            "              <tr>" +
            "                 <td width='20%'>一级行业</td> "+
            "                 <td>" + industry_ + "</td>" +
            "                 <td width='20%'>二级行业</td> "+
            "                 <td>" + industry2_ + "</td>" +
            "              </tr>" +
            "              <tr><td width='20%'>上市公司全称</td><td colspan='3'><input type='text' name='company_full_name' style='width:680px'></td></tr>" +
            "              <tr><td width='20%'>标的公司全称</td><td colspan='3'><input type='text' name='target_firm' style='width:680px'></td></tr>" +
            "              <tr>" +
            "                 <td width='20%'>公告披露日期</td>" +
            "                 <td><input type='text' name='published_date' class='published_date'></td>" +
            "                 <td width='20%'>财务顾问</td> "+
            "                 <td><input type='text' name='financial_advisor' class='financial_advisor'</td>" +
            "              </tr>" +
            "              <tr>" +
            "                 <td width='20%'>标的公司tags</td>" +
            "                 <td><input type='text' name='target_company_tags' class='target_company_tags'></td>" +
            "                 <td width='20%'>投资方tags</td> "+
            "                 <td><input type='text' name='investor_tags' class='investor_tags'</td>" +
            "              </tr>" +
            "              <tr>" +
            "                 <td width='20%'>交易类型</td> "+
            "                 <td><select name='transaction_type'>" +
            "                     <option value=1>控股权收购</option>" +
            "                     <option value=2>小股权投资</option>" +
            "                     <option value=3>老股转让(非并购)</option>" +
            "                     <option value=4>融资或并购</option>" +
            "                     <option value=5>资产转让</option>" +
            "                     <option value=6>增发</option>" +
            "                     <option value=7>企业债券</option>" +
            "                     <option value=8>可换公司债</option>" +
            "                     <option value=9>IPO</option>" +
            "                   </select></td>" +
            "                 <td width='20%'>交易币种</td> "+
            "                 <td><select name='transaction_currency'>" +
            "                     <option value=1>人民币</option>" +
            "                     <option value=2>美元</option>" +
            "                     <option value=3>欧元</option>" +
            "                     <option value=4>英镑</option>" +
            "                     <option value=5>日元</option>" +
            "                     <option value=6>港币</option>" +
            "                     <option value=7>新台币</option>" +
            "                     <option value=8>韩元</option>" +
            "                     <option value=9>其他</option>" +
            "                     <option value=10>未披露</option>" +
            "                   </select></td>" +
            "              </tr>" +
            "              <tr>" +
            "                 <td width='20%'>交易额</td> "+
            "                 <td><input type='text' name='transaction_amount' class='currencyFormat'></td>" +
            "                 <td width='20%'>交易比例 %</td> "+
            "                 <td><input type='text' name='transaction_ratio' style='width:200' maxLength='5'> </td>" +
            "              </tr>" +
            "              <tr><td>公告内容</td><td colspan='3'><textarea name='content' style='width:680px; height:500px'>'" + content + "'</textarea></td></tr>" +
            "            </table>" +
            "       </div>" +
            "       <div class='modal-footer'>" +
            "         <button type='button' class='btn btn-default close-modal-dialog' data-dismiss='modal'>关闭</button>" +
            "       </div>" +
            "     </div>" +
            "   </div>" +
            " </div>" +
            "            </td>" +  
            "          </tr>";
            parent.$(".todo").append(str_1);
        }
    });
    
    // remove the line
    $(".cancel").live("click",function(){
    if(confirm("确定要删除吗?")){  
    $(this).parents("tr").remove();  
     }   
    });

    // modify the line
    $(".modify").live("click",function(){
        var ref = $(this).attr("ref");
        var showWin = "#div_" + ref;
        $(showWin).modal('show');
    });

    $(".close-modal-dialog").live("click",function(){
        $(showWin).modal('hide');
    });

    parent.$(".xxx").each(function() {
    //    var selected = $(this).attr("data-id")// id=^new_\d$
    //    $("input[type='checkbox']").each(function() {
    //        var curr = $(this).attr("rel")
    //       if val == select  
    //           $(this).prop("checked", true)
    //    });
    });

    $(".todo").delegate(".published_date", "focus", function() {
        $(this).datepicker();

    });

    $(".todo").delegate(".currencyFormat", "keyup", function() {
        var result = $(this).val();
        var div = $(this).next();
        if (div.length > 0) {
            $(this).next().html(formatCurrenct(result));
        }
        else {
            $(this).after("<div></div>");
            $(this).next().html(formatCurrenct(result));
        }
    });

    $(".todo").delegate(".industry_father", "change", function() {
        var subId = $(this).parent().next().next().children(":first").attr("id");
        var val = $(this).val();
        industrySelect(subId, val);
    });

});

function formatCurrenct(number) {
    number = number.toString();
    dollars = number.split('.')[0];
    cents = (number.split('.')[1] || '') +'00';
    dollars = dollars.split('').reverse().join('')
        .replace(/(\d{3}(?!$))/g, '$1,')
        .split('').reverse().join('');
    return dollars;
}

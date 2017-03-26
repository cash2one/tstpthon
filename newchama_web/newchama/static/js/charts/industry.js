$(function () {

	if (!$('#bar-chart').length) { return false; }
	if (!$('#bar-chart2').length) { return false; }

	
	bar('bar-chart',0);
	bar('bar-chart2',1);


	//$(window).resize (target_admin.debounce (bar, 325));

});

var current_get_idx_left=0;
var current_get_idx_right=0;

function change_country(id){
	if (id ==0){
		$('#hidden_country_id').val(84);
		$('.is_usa_deal_type2').show();
		$('.is_usa_deal_type1').hide();

		$('#hidden_deal_type').val($("input[name='type_radio']:checked").val());
		$('#can_clicked').val(1);

	}
	else if (id==1){
		$('#hidden_country_id').val(212);
		$('.is_usa_deal_type1').show();
		$('.is_usa_deal_type2').hide();

		$('#hidden_deal_type').val($("input[name='type_radio2']:checked").val());
		
		$('#can_clicked').val(0);

		
	}	
	$('#change_country_block li').removeClass('active');
	$('#change_country_block li').eq(id).addClass('active');



	
	bar('bar-chart',0);
	bar('bar-chart2',1);
}



function change_deal_type(num){
	
	$('#hidden_deal_type').val(num);

	bar('bar-chart',0);
	bar('bar-chart2',1);
}




function bar (element,chart_type) {


	if (chart_type==1){
		current_get_idx_right++
		$('#alert_right').show();
		
	}else{
		current_get_idx_left++;
		$('#alert_left').show();
	}
	
	
	var now_idx_left=current_get_idx_left;
	var now_idx_right=current_get_idx_right;
	
	$('#'+element).empty ();
	$('.labels_tip').empty ();

	var all_data=[];

	var industry_id=$('#hidden_industry_id').val();
	var country_id=$('#hidden_country_id').val();
	var deal_type=$('#hidden_deal_type').val();



	  $.get('/deal/rank/'+Math.random()*100000,{industry_id:industry_id,country_id:country_id,chart_type:chart_type,deal_type:deal_type},function(result){
		    
		    result=JSON.parse(result);
		   
		    if(result.is_ok==1){
		    	var len=0;
		       for (var item in result.top_list) {

		       			if(chart_type==1){
		       				var temp1=[item,item,item,Math.round(result.top_list[item][1]/1000000),result.top_list[item][0]];
		       			}else{
		       				var temp1=[item,item,item,Math.round(result.top_list[item][1]),result.top_list[item][0]];

		       			}
						all_data.push(temp1);
				} 
				all_data.sort(function(a,b){return a[3]<b[3]?1:-1});
				
				var alert_no_record_text="没有统计记录！"
				if(get_template_lang()=="en-us"){
					alert_no_record_text="No Record!"	
				}



				if (chart_type==1){
					if(now_idx_right==current_get_idx_right){

						if(all_data.length==0){
							$('#alert_right').text(alert_no_record_text);
						}else{
							$('#alert_right').hide();
							showbar(all_data,chart_type,element);
						}

					 
					}
				}else{
					if(now_idx_left==current_get_idx_left){
						if(all_data.length==0){
							$('#alert_left').text(alert_no_record_text);
						}else{
							$('#alert_left').hide();
							showbar(all_data,chart_type,element);
						}

					 
					}


				}

			 
		    }
		  });
	

}

function showbar(all_data,chart_type,element){
	var labels_lang=''
	var lang_data=[];
	
	

	if(get_template_lang()=="en-us"){

			if(chart_type==0){
				labels_lang='Count';
			}else{
				labels_lang='Turnover';
			}

			
			$('.labels_tip').show();

			for (var i=0;i<all_data.length;i++){
				lang_data.push({y:all_data[i][0],a:all_data[i][3],l:all_data[i][1],iid:all_data[i][4]});
				var color_idx=i%target_admin.layoutColors.length;

				$('.labels_tip').append("<span><label style='background:"+target_admin.layoutColors[color_idx]+"'>"+all_data[i][0]+"</label>"+all_data[i][1]+"</span>")
				

			}
			
		}else{
			if(chart_type==0){
				labels_lang='笔数';
			}else{
				labels_lang='交易额$';
			}
			
			$('.labels_tip').hide();
			for (var i=0;i<all_data.length;i++){
				lang_data.push({y:all_data[i][2],a:all_data[i][3],l:all_data[i][2],iid:all_data[i][4]});
			}
		}


	Morris.Bar({
		element: element,
		
		data:lang_data,	
		xkey: 'y',
		ykeys: ['a'],
		labels: [labels_lang],
		xLabelAngle: 45,
		stacked:true,
		barColors: function (row, series, type) {
		    if (type === 'bar') {

			      var color_idx=row.x%target_admin.layoutColors.length;

			      return target_admin.layoutColors[color_idx];
		    }
		    else {
		      return target_admin.layoutColors[0];
		    }
		  },
		  hoverCallback: function (index, options, content, row) {
			  //console.log(index, content);
			  var labels_curreny='';

			  if(get_template_lang()=="en-us"){
			  	if(chart_type==1){

				labels_curreny='M';
				}
			  }
			  else{
			  	if(chart_type==1){

				labels_curreny='M';
				}

			  }
			  

			  return "<div class='morris-hover-row-label'>"+row.l+"</div><div class='morris-hover-point' style='color: #16a085'> "+labels_lang+": "+row.a+" "+labels_curreny+" </div>" ;
			}
	}).on('click', function(i, row){
		var can_clicked=$('#can_clicked').val();
		if(can_clicked==1){

		   window.location.href="/deal/industry/"+row.iid; 
		}
		});
}
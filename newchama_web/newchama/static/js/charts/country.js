$(function () {

	if (!$('#bar-chart').length) { return false; }

	bar ();

	//$(window).resize (target_admin.debounce (bar, 325));

});


function change_country(id){
	if (id ==0){
		$('#hidden_country_id').val(84);
	}
	else if (id==1){
		$('#hidden_country_id').val(212);
	}	
	$('#change_country_block li').removeClass('active');
	$('#change_country_block li').eq(id).addClass('active');
	
	bar();
}

function change_chart_type(){	
	$('#hidden_chart_type').val($('#chart_type').val());
	
	bar();
}


function change_deal_type(num){
	
	$('#hidden_deal_type').val(num);
	
	bar();
}



function bar () {
	
	$('#bar-chart').empty ();
	$('.labels_tip').empty ();

	var all_data=[];

	var industry_id=$('#hidden_industry_id').val();
	var country_id=$('#hidden_country_id').val();
	var chart_type=$('#hidden_chart_type').val();
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

				 showbar(all_data,chart_type);
				 
		    }
		  });
	

}

function showbar(all_data,chart_type){
	labels_lang=''
	lang_data=[];
	
	

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
				labels_lang='交易额';
			}
			
			$('.labels_tip').hide();
			for (var i=0;i<all_data.length;i++){
				lang_data.push({y:all_data[i][2],a:all_data[i][3],l:all_data[i][2],iid:all_data[i][4]});
			}
		}


	Morris.Bar({
		element: 'bar-chart',
		
		data:lang_data,	
		xkey: 'y',
		ykeys: ['a'],
		labels: [labels_lang],
		xLabelAngle: 45,
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

				labels_curreny='MUSD';
				}
			  }
			  else{
			  	if(chart_type==1){

				labels_curreny='百万美元';
				}

			  }
			  

			  return "<div class='morris-hover-row-label'>"+row.l+"</div><div class='morris-hover-point' style='color: #16a085'> "+labels_lang+": "+row.a+" "+labels_curreny+" </div>" ;
			}
	}).on('click', function(i, row){
		  var is_cv1=$('#is_cv1').val();
		if(is_cv1==1){

		   window.location.href="/deal/industry/"+row.iid; 
		}
		});
		});
}
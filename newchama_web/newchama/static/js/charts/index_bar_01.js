$(function () {

	if (!$('#bar-chart').length) { return false; }

	bar ();

	$(window).resize (target_admin.debounce (bar, 325));

});

function change_type(type){
	$('#record_type').val(type);
	$('#typeTab li').removeClass('active');
	if(type==0){
		$('#typeTab li').eq(0).addClass('active');
	}else if(type==1){
		$('#typeTab li').eq(1).addClass('active');
	}
	else if(type==2){
		$('#typeTab li').eq(2).addClass('active');
	}
	else if(type==3){
		$('#typeTab li').eq(2).addClass('active');
	}
	
	bar();
}

function change_days(days){
	
	$('#record_days').val(days);
	$('#daysTab button').removeClass('active');

	if(days==90){
		$('#daysTab button').eq(0).addClass('active');
	}else if(days==180){
		$('#daysTab button').eq(1).addClass('active');
	}
	else if(days==360){
		$('#daysTab button').eq(2).addClass('active');
	}
	
	bar();
}

function change_num(num){
	
	$('#record_num').val(num);
	
	bar();
}



function bar () {
	
	$('#bar-chart').empty ();
	$('.labels_tip').empty ();

	var all_data=[];

	var num=$('#record_num').val();
	var type=$('#record_type').val();
	var day=$('#record_days').val();
	  $.get('/cvsource/rank/'+Math.random()*100000,{day:day,num:num,type:type},function(result){
		    
		    result=JSON.parse(result);
		   
		    if(result.is_ok==1){
		    	var len=0;
		       for (var item in result.top_list) {
				       	var temp1=[item,item,item,Math.round(result.top_list[item]/100)];
						all_data.push(temp1);
				} 
				all_data.sort(function(a,b){return a[3]<b[3]?1:-1});

				 showbar(all_data);
		    }
		  });
	

}

function showbar(all_data){
	labels_lang=''
	lang_data=[];
	
	if(get_template_lang()=="en-us"){
			labels_lang='Turnover';
			$('.labels_tip').show();

			for (var i=0;i<all_data.length;i++){
				lang_data.push({y:all_data[i][0],a:all_data[i][3],l:all_data[i][1]});
				var color_idx=i%target_admin.layoutColors.length;

				$('.labels_tip').append("<span><label style='background:"+target_admin.layoutColors[color_idx]+"'>"+all_data[i][0]+"</label>"+all_data[i][1]+"</span>")
				

			}
			
		}else{
			labels_lang='交易额';
			$('.labels_tip').hide();
			for (var i=0;i<all_data.length;i++){
				lang_data.push({y:all_data[i][2],a:all_data[i][3],l:all_data[i][2]});
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
			  return "<div class='morris-hover-row-label'>"+row.l+"</div><div class='morris-hover-point' style='color: #16a085'> "+labels_lang+": "+row.a+" MUSD </div>" ;
			}
	}).on('click', function(i, row){
		  console.log(i, row);
		});
}
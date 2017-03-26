var current_chart_idx=1;
var chart_num=4;
var can_click=true;
$(document).ready(function(){

  var element='chart1';

  if (!$('#'+element).length) { return false; }

  bar (element,84,0);


   $('#chart_btn_right').click(function(){
    if(current_chart_idx>1){
        current_chart_idx-=1;
    }else{
        current_chart_idx=chart_num;
    }
    
    $('.chart-title').hide();
    $('.chart-title').eq(current_chart_idx-1).show();
    $('.chart_nav a').removeClass('on').eq(current_chart_idx-1).addClass('on');
    change_chart(element,current_chart_idx-1);
    
   });

   $('#chart_btn_left').click(function(){
    if(current_chart_idx<chart_num){
        current_chart_idx+=1;
    }else{
        current_chart_idx=1;
    }
    
    $('.chart-title').hide();
    $('.chart-title').eq(current_chart_idx-1).show();
    $('.chart_nav a').removeClass('on').eq(current_chart_idx-1).addClass('on');
    change_chart(element,current_chart_idx-1);
    
   });
   $('.chart_nav a').click(function(){
        var _idx=$('.chart_nav a').index($(this));

        current_chart_idx=_idx+1;

        $('.chart-title').hide();
    $('.chart-title').eq(current_chart_idx-1).show();
    $('.chart_nav a').removeClass('on').eq(current_chart_idx-1).addClass('on');
        
    change_chart(element,current_chart_idx-1);

   });


});


function change_chart(element,num){
  if (num==0){
    can_click=true;
    bar(element,84,num);
    
  }else if(num==1){
    can_click=false;
    donut(element,84,num);

  }
  else if(num==2){
    can_click=false;
    bar(element,212,num);

  }
  else if(num==3){
    can_click=false;
    donut(element,212,num);

  }
  
}

function bar (element,country_id,num) {
  
  $('#'+element).empty ();
  $('.labels_tip').empty ();

  var all_data=[];

  var industry_id=0;
  var chart_type=1;
  var deal_type=99;
  
    $.get('/deal/rank/'+Math.random()*100000,{industry_id:industry_id,country_id:country_id,chart_type:chart_type,deal_type:deal_type,num:15},function(result){
        
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

        if(current_chart_idx-1==num){
          
            showbar(element,all_data,chart_type);
          
        }

         
         
        }
      });
  

}

function showbar(element,all_data,chart_type){
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
    xLabelAngle: 45,stacked:true,
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
      var is_cv1=$('#is_cv1').val();
    if(is_cv1==1){
      console.log(i, row.iid);
      
      if(get_template_lang()!="en-us" && can_click){
      window.location.href="/deal/industry/"+row.iid; 
    }
      
    }
    });
}


function donut (element,country_id,num) {
  $('#'+element).empty ();
  
    var all_data=[];

  var industry_id=0;
  var chart_type=0;

    $.get('/deal/rank_deal_type/'+Math.random()*100000,{industry_id:industry_id,country_id:country_id,chart_type:chart_type},function(result){
        
        result=JSON.parse(result);

        if(result.is_ok==1){
          var sum_all=0;
          for (var item in result.top_list) {
              
                

            sum_all+=result.top_list[item];
        } 

          
           for (var item in result.top_list) {
                var temp1={label: covert_name(item), value: Math.round(result.top_list[item]*100/sum_all) }

            all_data.push(temp1);
        } 

        if(current_chart_idx-1==num){
          show_donut1(element,all_data);
        }
        
        
         
        }
      });

    
  
}

function covert_name(str){
  if(get_template_lang()=="en-us"){
    if(str==0){
      str="List";
    }else if(str==1){
      str="Trans";
    }else if(str==2){
      str="BuyTogether";
    }
  }else{

    if(str==0){
      str="上市";
    }else if(str==1){
      str="融资";
    }else if(str==2){
      str="并购";
    }

  }
  return str;
}

function show_donut1(element,data){
  Morris.Donut({
        element: element,
        data:data,
        colors: target_admin.layoutColors,
        hideHover: true,
        formatter: function (y) { return y + "%" }
    });
}
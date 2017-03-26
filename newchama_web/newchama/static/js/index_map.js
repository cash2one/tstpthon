$(document).ready(function(){
   $('#map_btn_1').hover(function(){
    $('#deal_usa').show();
    $('#deal_cn').hide();
    $('.float_usa').show();
    $('.float_cn').hide();

   },function(){

   });
   $('#map_btn_2').hover(function(){
    $('#deal_cn').show();
    $('#deal_usa').hide();
    $('.float_usa').hide();
    $('.float_cn').show();

   },function(){

   });


})
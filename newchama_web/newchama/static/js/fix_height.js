$(document).ready(function(){
   
   var _window_height=$(window).height();
   var _nav_height=$('nav').height();
   var _footer_height=$('.footer').height();
   var min_height=400;
   
   if (_window_height>=400+_nav_height+_footer_height){
    $('#newchama_logo_main').height(_window_height-_nav_height-_footer_height-100);
    //$('.footer').css('top',_window_height-_footer_height);
   }

})
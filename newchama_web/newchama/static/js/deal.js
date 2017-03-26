$(document).ready(function(){
    idx=$('#active_id').val();
    $('.top_nav_pills li').eq(idx).addClass('active');

})
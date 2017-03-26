

var is_sending=false;

$(document).ready(function(){

    get_new_message();
    bind_sendmessage();
    bind_removemessage();
    bind_readmessage();

})

function get_new_message(){

    $.get('/account/get_new_message_num/'+(new Date()).getTime(),function(result){
        result=JSON.parse(result);

        if(result.is_ok==1){
            if (result.num>0){
                $('#new_badge_num').show();
                $('#new_badge_num').html(result.num);

                $('.noticebar .badge').html(result.num);
                $.get('/account/get_new_message_html/',function(result){

                    $('.noticebar-menu-view-all').before(result);
                });


            }

        }

    });

}

function bind_sendmessage(){
    //$('.send_message_btn').click(function(){
    $(".panel-body").delegate(".send_message_btn","click",function(){
        $('#sendMessageModal').modal('show');
        $('#recipient_type_id').val($(this).attr('data-message-type'));
        $('#recipient_id').val($(this).attr('data-message-id'));
        $('#reply_id').val($(this).attr('data-reply-id'));
        $('#message_id').val($(this).attr('rel'));
        $('#textarea-message').val("");
        $('#error_tip').hide();

        $('#submit_message_btn').click(function(){
            if(!is_sending){
                is_sending=true;
                var recipient_id=$('#recipient_id').val();
                var recipient_type_id=$('#recipient_type_id').val();
                var reply_id=$('#reply_id').val();
                var message_id=$('#message_id').val();
                var text=$('#textarea-message').val();
                if (text=="" && recipient_id==0) {
                    is_sending=false;
                    return false;
                }
                $.post("/account/send_message/",{recipient_id:recipient_id,recipient_type_id:recipient_type_id,reply_id:reply_id,content:text,message_id:message_id},function(result){
                    is_sending=false;
                    result=JSON.parse(result);
                    if(result.is_ok==1){
                        $('#sendMessageModal').modal('hide');
                    }
                    else{
                        $('#error_tip').show().html(result.message);
                    }

                });
            }
        });
    });
}

function bind_removemessage(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".remove_message_btn","click",function(){
        var _id=$(this).attr('rel');
        var _outblock=$(this).parent().parent();
        custom_confirm("Are you sure you want to delete the message?","New Message", function() {
            $.post("/account/remove_message/",{message_id:_id},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    _outblock.fadeOut();
                }
            });

        });
    });
}
function bind_readmessage(){
    //$('.see_message_btn').click(function(){
    $(".panel-body").delegate(".see_message_btn","click",function(){
        var _id=$(this).attr('rel');
        var _outblock=$(this).parent().parent();

        $.post("/account/read_message/",{message_id:_id},function(result){

            result=JSON.parse(result);

            if(result.is_ok==1){
                _outblock.fadeOut();

            }


        });
    });
}


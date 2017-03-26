var is_sending=false;
$(document).ready(function(){
    get_new_message();
    bind_sendmessage();
    bind_removemessage();
    bind_readmessage();
    bind_removemessagewithproject();
    bind_removemessagewithdemand();
    bind_removemessagewithperson();
    bind_showmessagemodelbtn();
    bind_deleter_person_message_all_btn();
    bind_deleter_project_message_all_btn();
})



function get_new_message(){

    $.get('/account/get_new_message_num/'+(new Date()).getTime(),function(result){
        result=JSON.parse(result);

        if(result.is_ok==1){
            if (result.num>0){
                $('#new_badge_num').show();
                /*$('#new_badge_num').html(result.num);

                $('.noticebar .badge').html(result.num);
                $.get('/account/get_new_message_html/',function(result){

                    $('.noticebar-menu-view-all').before(result);
                });*/
            }

        }

    });

}

function get_message_by_id(receiver_id,receiver_name,receiver_pic,sender_id,sender_name,sender_pic){
    $('.m_loader').show();
    $.get('/account/get_new_message_by_id/'+(new Date()).getTime(),{receiver_id:receiver_id,sender_id:sender_id},function(result){
        result=JSON.parse(result);
        $('.scoller_message_block ul').html("");
        if(result.is_ok==1){
            if (result.num>0){
                var fds = result.format_date;
                var _list=JSON.parse(result.new_message_list);

                for (var i=0;i<_list.length;i++){

                    if (_list[i].fields.sender==receiver_id){
                        var append_str="<li class=\"chat_left\">\
                     <div class=\"chat_member\">\
                       <span class=\"message-item-pic\">\
                        <img src=\""+receiver_pic+"\" style=\"width: 30px;\" />\
                      </span>\
                      <span class=\"chat_name\">"+receiver_name+"</span>\
                      <span class=\"chat_time\">"+fds[i]+"</span>\
                      </div>\
                      <span class=\"chat_content\">\
                        "+_list[i].fields.content+"\
                        <em class=\"zero\"></em>\
                      </span>\
                    </li>";

                    }else{

                        var append_str="<li class=\"chat_right\">\
                     <div class=\"chat_member\">\
                       <span class=\"message-item-pic\">\
                        <img src=\""+sender_pic+"\" style=\"width: 30px;\" />\
                      </span>\
                      <span class=\"chat_name\">"+sender_name+"</span>\
                      <span class=\"chat_time\">"+fds[i]+"</span>\
                      </div>\
                      <span class=\"chat_content\">\
                        "+_list[i].fields.content+"\
                        <em class=\"zero\"></em>\
                      </span>\
                    </li>";

                    }

                    $('.scoller_message_block ul').append(append_str);

                }

                //Terry 20150407
                $('.scoller_message_block').scrollTop($('.scoller_message_block ul').height());
                setTimeout("sett()", 1500)
                $('#message_txtbox').val("");

                $('.m_loader').hide();

            }

        }

    });

}

function sett() {
    $('.scoller_message_block').scrollTop($('.scoller_message_block ul').height());
}

function bind_showmessagemodelbtn(){
    //$('.send_message_btn').click(function(){
    $(".panel-body").delegate(".show_message_model_btn","click",function(){

        $('#showMessageModal').modal('show');
        var receiver_id=$(this).attr('data-receiver-id');
        $('#receiver_id').val(receiver_id);

        var receiver_pic=$(this).attr('data-receiver-pic');
        $('#receiver_pic').val(receiver_pic);

        var receiver_name=$(this).attr('data-receiver-name');
        $('#receiver_name').val(receiver_name);


        var sender_id=$(this).attr('data-sender-id');
        $('#sender_id').val(sender_id);

        var sender_pic=$(this).attr('data-sender-pic');
        $('#sender_pic').val(sender_pic);

        var message_id=$(this).attr('data-message-id');
        $('#message_id').val(message_id);

        var sender_name=$(this).attr('data-sender-name');
        $('#sender_name').val(sender_name);

        var receiver_type=$(this).attr('data-receiver-type');
        $('#recipient_type').val(receiver_type);


        var item_id=$(this).attr('data-item-id');
        $('#recipient_type_id').val(item_id);


        $('#message_txtbox').val("");
        //当用户点开未读消息后，将原先未读标记移除，同时查询其他是否还有未读标记，如果没有了，则右上角的未读标记也一并移除
        $("span[id='new_badge_num']").each(function() {
            if (item_id == $(this).attr("ref")) {
                $(this).remove();
                var havenotread = false;
                $("span[id='new_badge_num']").each(function() {
                    if (!$(this).hasClass("badge")) {
                        havenotread = true;
                        return false;
                    }
                });
                if (!havenotread) {
                    $("span[id='new_badge_num']").each(function() {
                        if ($(this).hasClass("badge")) {
                            $(this).remove();
                        }
                        return false;
                    });
                }
                return false;
            }
        });

        get_message_by_id(receiver_id,receiver_name,receiver_pic,sender_id,sender_name,sender_pic);

        $('#phrase_block li a').click(function(){
            $('#message_txtbox').val($(this).html());

        });

        $('#submit_message_btn').unbind("click");
        $('#submit_message_btn').click(function(){
            if(!is_sending){
                is_sending=true;
                var myDate = new Date();
                $("#submit_message_btn").prop("disabled", true);
                var m=$('#message_txtbox').val();
                if (m !=""){

                    $.post("/account/send_message/",{recipient_id:item_id,recipient_type_id:receiver_type,reply_id:receiver_id,content:m,message_id:message_id},function(result){
                        is_sending=false;
                        result=JSON.parse(result);
                        if(result.is_ok==1){
                            get_message_by_id(receiver_id,receiver_name,receiver_pic,sender_id,sender_name,sender_pic);
                        }
                        else{
                            alert(result.message);
                        }
                        $("#submit_message_btn").prop("disabled", false);
                    });

                }
            }
            is_sending=false;

        });


        $("#uploadFile").fileupload({
            url:"/services/upload_message_file",//文件上传地址，当然也可以直接写在input的data-url属性内
            dataType: 'text',
            acceptFileTypes:  /(\.|\/)(doc|docx|pdf|xls|xlsx|ppt|pptx|png|jpg)$/i,
            done: function (e, data) {
                result = jQuery.parseJSON(data.result);
                if (result.status == "success") {

                    $("#selectFileUploading").hide();

                    if(!is_sending){
                        is_sending=true;
                        var myDate = new Date();
                        var m="文件：<a href='"+result.path+"' target='_blank'>"+result.oldname+"</a>";
                        if (m !=""){

                            $.post("/account/send_message/",{recipient_id:receiver_id,recipient_type_id:0,reply_id:sender_id,content:m,message_id:0},function(result){
                                is_sending=false;
                                result=JSON.parse(result);
                                if(result.is_ok==1){
                                    get_message_by_id(receiver_id,receiver_name,receiver_pic,sender_id,sender_name,sender_pic);
                                }
                                else{
                                    alert(result.message);

                                }

                            });

                        }

                    }

                    is_sending=false;
                }
                else {
                    alert(result.message);
                }

            },
            progressall: function (e, data) {

                $("#selectFileUploading").show();

            }
        });



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
        var is_sending=false;
        $('#submit_message_btn').unbind("click");
        $('#submit_message_btn').click(function(){
            if(!is_sending){
                is_sending=true;
                $("#submit_message_btn").prop("disabled", true);
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
                    $("#submit_message_btn").prop("disabled", false);
                });
            }
        });
    });
}

function show_sendmessage(recipientType, recipientId, replyId, messageId){
    $('#sendMessageModal').modal('show');
    $('#recipient_type_id').val(recipientType);
    $('#recipient_id').val(recipientId);
    $('#reply_id').val(replyId);
    $('#message_id').val(messageId);
    $('#textarea-message').val("");
    $('#error_tip').hide();
    $('#submit_message_btn').unbind("click");
    $('#submit_message_btn').click(function(){
        if(!is_sending){
            is_sending=true;
            $("#submit_message_btn").prop("disabled", true);
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
                $("#submit_message_btn").prop("disabled", false);
            });
        }
    });
}

function bind_removemessage(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".remove_message_btn","click",function(){
        var _id=$(this).attr('rel');
        var _outblock=$(this).parent().parent();
        custom_confirm("确定要删除消息吗？","信息提示", function() {
            $.post("/account/remove_message/",{message_id:_id},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    _outblock.fadeOut();
                }
            });

        });
    });
}
function bind_removemessagewithperson(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".remove_message_with_person_btn","click",function(){
        var _id=$(this).attr('rel');
        var _outblock=$(this).parent().parent().parent().parent();
        custom_confirm("确定要删除消息吗？","信息提示", function() {
            $.post("/account/remove_message_person/",{message_id:_id},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    _outblock.fadeOut();
                }
            });

        });
    });
}
function bind_removemessagewithproject(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".remove_message_with_project_btn","click",function(){
        var _id=$(this).attr('rel');
        var _outblock=$(this).parent().parent().parent().parent();
        custom_confirm("确定要删除消息吗？","信息提示", function() {
            $.post("/account/remove_message_project/",{message_id:_id},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    _outblock.fadeOut();
                }
            });

        });
    });
}
function bind_removemessagewithdemand(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".remove_message_with_demand_btn","click",function(){
        var _id=$(this).attr('rel');
        var _outblock=$(this).parent().parent().parent().parent();
        custom_confirm("确定要删除消息吗？","信息提示", function() {
            $.post("/account/remove_message_demand/",{message_id:_id},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    _outblock.fadeOut();
                }
            });

        });
    });
}

function bind_deleter_person_message_all_btn(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".btn_deleter_person_message_all_btn","click",function(){

        custom_confirm("确定要删除消息吗？","信息提示", function() {

            var chk_value =new Array();
            $('input[name="check_message"]:checked').each(function(){
                chk_value.push($(this).val());
            });

            $.post("/account/remove_message_person_all/",{'message_list_up':chk_value.join(',')},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    for (var i =0 ; i<chk_value.length;i++){

                        $('#message_'+chk_value[i]).fadeOut();
                    }
                }
            });

        });

    });
}

function bind_deleter_project_message_all_btn(){
    //$('.remove_message_btn').click(function(){
    $(".panel-body").delegate(".btn_deleter_project_message_all_btn","click",function(){

        custom_confirm("确定要删除消息吗？","信息提示", function() {

            var chk_value =new Array();
            $('input[name="check_message"]:checked').each(function(){
                chk_value.push($(this).val());
            });

            $.post("/account/remove_message_project_all/",{'message_list_up':chk_value.join(',')},function(result){
                result=JSON.parse(result);
                if(result.is_ok==1){
                    for (var i =0 ; i<chk_value.length;i++){

                        $('#message_'+chk_value[i]).fadeOut();
                    }
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
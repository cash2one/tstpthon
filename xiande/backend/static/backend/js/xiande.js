function DoDelete(url, id) {
    if (confirm("你确认要删除该内容么?")) {
        jQuery.post(
            url, {id:id},
            function (msg) {
                if (msg == "success") {
                    alert("操作成功!");
                    location.reload();
                }
                else {
                    alert("操作错误，请联系系统管理员!");
//                    alert(msg);
                }
            },
            "text"
        );
       
    }
}

function DoDisapproved(url, id) {
    if (confirm("你确认审核不通过该内容么?")) {
        jQuery.post(
            url, {id:id},
            function (msg) {
                if (msg == "success") {
                    alert("操作成功!");
                    location.reload();
                }
                else {
                    alert("操作错误，请联系系统管理员!");
//                    alert(msg);
                }
            },
            "text"
        );
       
    }
}
function DoApproved(url, id) {
    if (confirm("你确认审核通过该内容么?")) {
        jQuery.post(
            url, {id:id},
            function (msg) {
                if (msg == "success") {
                    alert("操作成功!");
                    location.reload();
                }
                else {
                    alert("操作错误，请联系系统管理员!");
//                    alert(msg);
                }
            },
            "text"
        );
       
    }
}

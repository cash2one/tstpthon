var istudiobjstatistics={

    //scripts:document.getElementsByTagName("script"),
    script:(document.getElementsByTagName("script")[document.getElementsByTagName("script").length-1]),//因为当前dom加载时后面的script标签还未加载，所以最后一个就是当前的script
    img:"",

    getResolution:function(){/*用户分辩率*/
        return screen.width+"*"+screen.height;
    },
    getsrcurl:function(){
        var ref = '';
        if (document.referrer.length > 0) {
            ref = document.referrer;
        }
        try {
            if (ref.length == 0 && opener.location.href.length > 0) {
                ref = opener.location.href;
            }
        }catch (e) {}
        return ref;
    },

    getviewrect:function(){
        var winWidth,winHeight
        if (window.innerWidth)
            winWidth = window.innerWidth;
        else if ((document.body) && (document.body.clientWidth))
            winWidth = document.body.clientWidth;
        // 获取窗口高度
        if (window.innerHeight)
            winHeight = window.innerHeight;
        else if ((document.body) && (document.body.clientHeight))
            winHeight = document.body.clientHeight;
        // 通过深入 Document 内部对 body 进行检测，获取窗口大小
        if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth)
        {
            winHeight = document.documentElement.clientHeight;
            winWidth = document.documentElement.clientWidth;
        }
        return (winWidth+"*"+winHeight)
    },

    getScriptArgs:function(key){//获取多个参数
        src=istudiobjstatistics.script.src,
        reg=/(?:\?|&)(.*?)=(.*?)(?=&|$)/g,
        temp="",
        res={};
        while((temp=reg.exec(src))!=null) res[temp[1]]=decodeURIComponent(temp[2]);
        return res['ukey'];
    },

    go:function(et,ev){
        if(!et){
            et="PV"
            ev = ""
        }
        if(istudiobjstatistics.img==""){
            
            istudiobjstatistics.img = document.createElement("img");
            try{
                istudiobjstatistics.script.appendChild(istudiobjstatistics.img);
            }catch(e){
                document.write("<img width=0 height=0 style=‘display:block’ id='___cont' />");
                istudiobjstatistics.img=document.getElementById("___cont")
            }
            
            
        }
        var actionsrc = istudiobjstatistics.script.src.substr(0,istudiobjstatistics.script.src.lastIndexOf("/",istudiobjstatistics.script.src.indexOf("?")) );
        //alert(actionsrc)
        //alert(script.src)
        istudiobjstatistics.img.src=actionsrc+"/action/?$$name=monitor&ukeys="+istudiobjstatistics.getScriptArgs("ukey")+"&et="+et+"&ev="+ev+"&spu="+encodeURIComponent(istudiobjstatistics.getsrcurl())+"&sr="+istudiobjstatistics.getResolution()+"&vr="+istudiobjstatistics.getviewrect()+"&pageurl="+encodeURIComponent(location.href)
    }
}
istudiobjstatistics.go()
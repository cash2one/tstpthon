var language_cookie_name ="language";

function change_lang(lang){
	if(getCookie(language_cookie_name)!=""){
		deleteCookie(language_cookie_name);
		
	}
	addCookie(language_cookie_name,lang,24*30);

	window.location.reload(); 
}

function getCookie(name){
      var strCookie=document.cookie;
      var arrCookie=strCookie.split("; ");
      for(var i=0;i<arrCookie.length;i++){
            var arr=arrCookie[i].split("=");
            if(arr[0]==name) {
                if (arr[1] != "v") {
                    return arr[1];
                }
            }
      }
      return "";
}

function addCookie(name,value,expireHours){
      var cookieString=name+"="+escape(value);
      //判断是否设置过期时间
      if(expireHours>0){
             var date=new Date();
             date.setTime(date.getTime+expireHours*3600*1000);
             cookieString=cookieString+"; expire="+date.toGMTString()+";path=/";
      }
      document.cookie=cookieString;
}

function deleteCookie(name){
       var date=new Date();
       date.setTime(date.getTime()-10000);
       document.cookie=name+"=v; expire="+date.toGMTString();
}

function get_template_lang() {
    var lang = getCookie(language_cookie_name);
    if (lang == "") return "zh-cn";
    else return lang;
}
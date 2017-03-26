  var url_location = location.href;
  var url_bool = false;
  var url_search = ["/sales/search", "/purchase/search", "/news/search"];
  var url_project_recent = [];//["/sales/new", "/sales/detail"];
  var url_demand_recent = [];//["/purchase/new", "/purchase/detail"];
  var url_project_manage = ["/sales/mylist", "/sales/edit/", "/purchase/edit/", "/purchase/mylists"];
  var url_preference = ["/account/preference_project", "/account/preference_demand", "account/preference_news"];
  var url_favorite = [];//["/account/myfavorite", "/account/myfavorite_demand", "/account/myfavorite_data", "/account/myfavorite_news", "/account/myfavorite_company", "/account/myfavorite_member"];
  var urls = new Array(url_preference, url_project_manage, url_demand_recent, url_project_recent, url_favorite,url_search);
  jQuery("#ul_nav li a").each(function() {
      var nav_link = jQuery(this).attr("href");
      if(url_location.indexOf(nav_link) >= 0) {
          if (jQuery(this).parent().parent().parent()[0].tagName.toLowerCase() == "li") {
              jQuery(this).parent().parent().parent().addClass("active");
          }
          else {
              jQuery(this).parent().addClass("active");
          }
          url_bool = true;
          return false;
      }
  });
  if (!url_bool) {
      var breakloop = false;
      for (var i = 0; i < urls.length; i ++) {
          var url_sub = urls[i];
          var url_1 = url_sub[0];
          for (var j = 1; j < url_sub.length; j ++) {
              if (url_location.indexOf(url_sub[j]) > -1) {
                  jQuery("#ul_nav li a[href='" + url_1 + "']").parent().addClass("active");
                  breakloop = true;
                  break;
              }
          }
          if (breakloop) break;
      }
  }
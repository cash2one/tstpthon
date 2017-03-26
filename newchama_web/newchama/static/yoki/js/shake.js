 if (window.DeviceMotionEvent) {
              window.addEventListener('devicemotion',deviceMotionHandler, false);
    }

        
    var SHAKE_THRESHOLD = 800;
    var last_update = 0;
    var x, y, z, last_x, last_y, last_z;
       
    function deviceMotionHandler(eventData) {
        
      var acceleration =eventData.accelerationIncludingGravity;
      //alert(newDate().getTime());
      var curTime = new Date().getTime();
       
         // alert(curTime - last_update);
      if ((curTime - last_update)> 300) {
                
          var diffTime = curTime -last_update;
          last_update = curTime;
       
          x = acceleration.x;
          y = acceleration.y;
          z = acceleration.z;
       
          var speed = Math.abs(x +y + z - last_x - last_y - last_z) / diffTime * 10000;
          
               if (speed > SHAKE_THRESHOLD) {
                          //å†™æ™ƒåŠ¨äº‹ä»¶
                          $(".page9-happy").css("display","block"); 
                          $(".page9-lighton").css("display","none");
                          $(".page9-light").removeClass("page9-light-animate");
                          $(".page9-light").css("opacity","0");
                          $(".page9-shade").css("opacity","0");
                          $(".page9-jiantou").addClass("page9-jiantou-animate");
                          $(".page9-shake").removeClass("page9-shake-animate");
                          $(".page9-stars").css("display","block");
          }
          last_x = x;
          last_y = y;
          last_z = z;
        }
    } 
/**
 * Created by piratos on 7/19/14.
 */
$(document).ready(function(){
   $("#to_create").click(function(){
       $("#login").removeClass("active").addClass("fade");
       $("#create1").removeClass("fade").addClass("active").load("/talk/register/ #myform");
   });
});
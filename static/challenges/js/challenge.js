/**
 * Created by piratos on 7/31/14.
 */
$(document).ready(function(){  //TODO add DDos attack protection from multi-submitting
    $('#chk').click(function(){
        var flag = $('#flag').val();
        var id = $('#flag').attr('ch-data');
        $.get('/challenges/check/', {flag: flag, chid: id}, function(data){
           if (data == 'success'){
               $('#result').html('<p class="alert alert-success">correct flag ! challenge solved</p>');
               $('#submitFlag').hide();
           }
            else {
               $('#result').html('<p id="s" class="alert alert-danger">invalid flag ! try again</p>');
               $('#s').fadeOut(1500);
           }
        });
    });
});
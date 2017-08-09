$(function(){
    var $date = $('#date');
    var $submit = $('#submit');

    $date.on('blur', function(){
        var pattern = /^\d{1,2}\/\d{1,2}\/\d{2,4}$/;
       if($date.val().search(pattern) === -1){
           $submit.attr('disabled', 'true');
           $date.css('background-color', 'red');
       }else{
           $submit.removeAttr('disabled');
       }
    });

    $date.on('focus', function(){
       $date.css('background-color', '');
    });
});
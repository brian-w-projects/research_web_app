$(function(){
    var $submit = $('#submit');
    var $first = $('#first');
    var $last = $('#last');

    $first.add($last).on('input', function(){
       if($first.val().length > 0 && $last.val().length > 0){
           $submit.removeAttr('disabled');
       }else{
           $submit.attr('disabled', 'True');
       }
    });

    $submit.on('click', function(){
        $(this).button('loading');
    });

});
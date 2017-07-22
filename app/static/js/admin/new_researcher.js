$(function(){
    var $submit = $('#submit');
    var $email = $('#email');
    var pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    $email.on('input', function(){
       if($email.val().search(pattern) !== -1){
           $email.parent().addClass('has-success').removeClass('has-error');
           $email.next().addClass('glyphicon-ok').removeClass('glyphicon-remove');
           $submit.removeAttr('disabled');
       }else{
           $submit.attr('disabled', 'True');
           $email.parent().removeClass('has-success');
           $email.next().removeClass('glyphicon-ok');
       }
    });

    $submit.on('click', function(){
        $(this).button('loading');
    });

});
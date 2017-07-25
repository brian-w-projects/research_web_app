$(function(){

    var $submit = $('#submit');
    var $email = $('#email');
    var $password = $('#password');
    var pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    $email.on('input', function(){
       if($email.val().search(pattern) !== -1) {
           $email.parent().addClass('has-success').removeClass('has-error');
           $email.next().addClass('glyphicon-ok').removeClass('glyphicon-remove');
       }
    }).on('blur', function(){
        if($email.val().search(pattern) === -1) {
           $email.parent().addClass('has-error').removeClass('has-success');
           $email.next().addClass('glyphicon-remove').removeClass('glyphicon-ok');
       }
    });

    $password.on('input', function(){
       if($password.val().length >= 10){
           $password.parent().addClass('has-success').removeClass('has-error');
           $password.next().addClass('glyphicon-ok').removeClass('glyphicon-remove');
       }
    }).on('blur', function(){
        if($password.val().length < 10){
            $password.parent().addClass('has-error').removeClass('has-success');
            $password.next().addClass('glyphicon-remove').removeClass('glyphicon-ok');
        }
    });

    $email.add($password).on('input', function(){
       if($email.val().search(pattern) !== -1 && $password.val().length >= 10){
           $submit.removeAttr('disabled');
       }else{
           $submit.attr('disabled', true);
       }
    });
});
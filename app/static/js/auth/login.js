$(function(){

    var $email = $('#email');
    var $password = $('#password');

    $email.on('validate', function(evt, ret){
       ret.val = emailVerify(evt);
    });

    $password.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 10);
    });
});
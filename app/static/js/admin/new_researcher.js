$(function(){

    var $email = $('#email');

    $email.on('validate', function(evt, ret){
       ret.val = emailVerify(evt);
    });

});
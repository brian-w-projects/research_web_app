$(function(){
    var $email = $('#email');
    var $token = $('#token');
    var $firstName = $('#first_name');
    var $lastName = $('#last_name');
    var $password = $('#password');
    var $passwordConfirm = $('#password_confirm');

    $('[data-toogle="tooltip"]').tooltip();


    $password.on('focus', function(){
        $password.parent().tooltip('show');
    }).on('blur', function(){
        $password.parent().tooltip('hide');
    });

    $passwordConfirm.on('focus', function(){
        $passwordConfirm.parent().tooltip('show');
    }).on('blur', function(){
        $passwordConfirm.parent().tooltip('hide');
    });

    $token.on('validate', function(evt, ret){
       ret.val = true;
    });

    $email.on('validate', function(evt, ret){
       ret.val = true;
    });

    $firstName.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $lastName.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $password.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 10);
    });

    $passwordConfirm.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 10) &&  equalVerify(evt, $password);
    });


});
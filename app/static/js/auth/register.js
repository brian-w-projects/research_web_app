$(function(){

    var $form = $('form');
    var $email = $('#email');
    var $token = $('#token');
    var $firstName = $('#first_name');
    var $lastName = $('#last_name');
    var $password = $('#password');
    var $passwordConfirm = $('#password_confirm');

    $('[data-toogle="tooltip"]').tooltip();
    $form.formValidator();

    $password.on('focus', function(){
        $password.parent().tooltip('show');
    }).on('blur', function(){
        $password.parent().tooltip('hide');
    }).formRequire({'length': 10});

    $passwordConfirm.on('focus', function(){
        $passwordConfirm.parent().tooltip('show');
    }).on('blur', function(){
        $passwordConfirm.parent().tooltip('hide');
    }).formRequire({'length': 10, 'equal': $password});

    $firstName.formRequire({'length': 1});
    $lastName.formRequire({'length': 1});
});
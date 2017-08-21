$(function(){

    var $form = $('form');
    var $email = $('#email');
    var $password = $('#password');

    $form.formValidator();

    $email.formRequire({'email': true});
    $password.formRequire({'length': 10});
});
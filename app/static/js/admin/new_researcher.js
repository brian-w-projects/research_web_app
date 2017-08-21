$(function(){

    var $form = $('form');
    var $email = $('#email');

    $form.formValidator();

    $email.formRequire({'email': true});
});
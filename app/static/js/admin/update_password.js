$(function(){
    var $form = $('form');
    var $pw = $('#current_password');
    var $newpw = $('#new_password');
    var $conpw = $('#confirm_password');

    $('[data-toogle="tooltip"]').tooltip();
    $form.formValidator();


    $pw.on('focus', function(){
        $pw.parent().tooltip('show');
    }).on('blur', function(){
        $pw.parent().tooltip('hide');
    }).formRequire({'length': 10});

    $newpw.on('focus', function(){
        $newpw.parent().tooltip('show');
    }).on('blur', function(){
        $newpw.parent().tooltip('hide');
    }).formRequire({'length' : 10});

    $conpw.on('focus', function(){
        $conpw.parent().tooltip('show');
    }).on('blur', function(){
        $conpw.parent().tooltip('hide');
    }).formRequire({'length': 10, 'equal': $newpw});
});
$(function(){
    var $pw = $('#current_password');
    var $newpw = $('#new_password');
    var $conpw = $('#confirm_password');

    $('[data-toogle="tooltip"]').tooltip();


    $pw.on('focus', function(){
        $pw.parent().tooltip('show');
    }).on('blur', function(){
        $pw.parent().tooltip('hide');
    });

    $newpw.on('focus', function(){
        $newpw.parent().tooltip('show');
    }).on('blur', function(){
        $newpw.parent().tooltip('hide');
    });

    $conpw.on('focus', function(){
        $conpw.parent().tooltip('show');
    }).on('blur', function(){
        $conpw.parent().tooltip('hide');
    });

    $pw.on('validate', function(evt, ret){
        ret.val = lengthVerify(evt, 10);
    });

    $newpw.on('validate', function(evt, ret) {
        ret.val = lengthVerify(evt, 10);
    });

    $conpw.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 10) && equalVerify(evt, $newpw);
    });
});
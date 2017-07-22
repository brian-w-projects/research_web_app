$(function(){
    var $submit = $('#submit');
    var $firstName = $('#first_name').data({'valid': false});
    var $lastName = $('#last_name').data({'valid': false});
    var $password = $('#password').data({'valid': false});
    var $passwordConfirm = $('#password_confirm').data({'valid': false});

    $('[data-toogle="tooltip"]').tooltip();

    $firstName.add($lastName).on('input', function(){
        var $toProcess = $(this);
        if($toProcess.val().length > 0){
            $toProcess.parent().addClass('has-success');
            $toProcess.next().addClass('glyphicon-ok');
            $toProcess.valid = true;
        }else{
            $toProcess.parent().removeClass('has-success');
            $toProcess.next().removeClass('glyphicon-ok');
            $toProcess.valid = false;
        }
        submitValid();
    });

    $password.on('input', function(){
       if($password.val().length >= 10){
           $password.parent().addClass('has-success').tooltip('hide');
           $password.next().addClass('glyphicon-ok');
           $password.valid = true;
       }else{
           $password.parent().removeClass('has-success');
           $password.next().removeClass('glyphicon-ok');
           $password.valid = false;
       }
       submitValid();
    }).on('focus', function(){
        $password.parent().tooltip('show');
    });

    $passwordConfirm.add($password).on('input', function(){
       if($passwordConfirm.val() === $password.val()) {
           $passwordConfirm.parent().addClass('has-success').tooltip('hide');
           $passwordConfirm.next().addClass('glyphicon-ok');
           $passwordConfirm.valid = true;
       }else{
           $passwordConfirm.parent().removeClass('has-success');
           $passwordConfirm.next().removeClass('glyphicon-ok');
           $passwordConfirm.valid = false;
       }
       submitValid();
    }).on('focus', function(){
        $passwordConfirm.parent().tooltip('show');
    });

    $submit.on('click', function(){
        $(this).button('loading');
    });

    function submitValid(){
        var check = [$lastName.valid, $firstName.valid, $passwordConfirm.valid, $password.valid];
        var valid = true;
        check.forEach(function(ele){
            if (ele === false && valid === true) {
                valid = false;
                $submit.attr('disabled', 'true');
            }
        });
        if(valid === true){
            $submit.removeAttr('disabled');
        }
    }

});
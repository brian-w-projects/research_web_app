$(function(){
   var $submit = $('#submit');
   var $email = $('#email');
   var $token = $('#token');
   var pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

   $email.on('input', function() {
       if ($email.val().search(pattern) !== -1) {
           $email.parent().addClass('has-success').removeClass('has-error');
           $email.next().addClass('glyphicon-ok').removeClass('glyphicon-remove');
       }
   }).on('blur', function() {
        if($email.val().search(pattern) === -1) {
           $email.parent().addClass('has-error').removeClass('has-success');
           $email.next().addClass('glyphicon-remove').removeClass('glyphicon-ok');
       }
   });

   $token.on('input', function(){
      if($token.val().length > 0){
           $token.parent().addClass('has-success').removeClass('has-error');
           $token.next().addClass('glyphicon-ok').removeClass('glyphicon-remove');
      }
   });

   $(document).on('input', function(){
      if($email.val().search(pattern) !== -1 && $token.val().length > 0){
          $submit.removeAttr('disabled');
      } else{
          $submit.attr('disabled', true);
      }
   });

   $submit.on('click', function(){
        $(this).button('loading');
    });

});
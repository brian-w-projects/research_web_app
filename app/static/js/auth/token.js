$(function(){
   var $email = $('#email');
   var $token = $('#token');

   $token.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
   });

   $email.on('validate', function(evt, ret){
      ret.val = emailVerify(evt);
   });

});
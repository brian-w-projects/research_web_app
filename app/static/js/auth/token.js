$(function(){
   var $form = $('form');
   var $email = $('#email');
   var $token = $('#token');

   $form.formValidator();

   $token.formRequire({'length': 1});
   $email.formRequire({'email': true});
});
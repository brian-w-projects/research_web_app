$(function(){
   var $submit = $('#submit');
   var $token = $('#token');
   var $first = $('#first_name');
   var $last = $('#last_name');
   var $form = $('form');

   $form.on('input', function(){
       var valid = true;
       $first.add($last).add($token).each(function(){
          if($(this).val().length == 0) {
              valid = false;
          }
       });
       if(valid){
           $submit.removeAttr('disabled');
       }else{
           $submit.attr('disabled', 'True');
       }
   });

   $submit.on('click', function(){
      $(this).button('loading');
   });

});
$(function(){
   var $id = $('#patient_id');
   var $selects = $('.selectpicker');
   var $formType = $('#form_type');
   var $dataRequest = $('#data_request');
   var $submit = $('#submit');

   $selects.selectpicker('mobile');


   $id.add($formType).add($dataRequest).on('input', function(){
      if($id.val().length > 0 && $formType.val().length > 0 && $dataRequest.val().length > 0){
          $submit.removeAttr('disabled');
      }else{
          $submit.attr('disabled', 'True');
      }
   });

   $submit.on('click', function(){
       $('.alert').hide();
       $(this).button('loading');
   });

});
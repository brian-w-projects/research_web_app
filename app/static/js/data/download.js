$(function(){
   var $form = $('form');
   var $patientId = $('#patient_id');

   $form.formValidator();

   $patientId.formRequire({'length': 1});
});
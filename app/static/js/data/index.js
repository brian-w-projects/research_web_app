$(function(){
    var $form = $('form');
    var $selects = $('.selectpicker');
    var $id = $('#patient_id');
    var $formType = $('#form_type');
    var $dataRequest = $('#data_request');
    var $submit = $('#submitValidate');

    $form.formValidator();

    $selects.selectpicker('mobile').selectpicker('setStyle', 'btn-lg', 'add');
    $id.formRequire({'length': 1});
    $formType.formRequire({'length': 1});
    $dataRequest.formRequire({'length': 1});
});
$(function(){
    var $selects = $('.selectpicker');
    var $id = $('#patient_id');
    var $formType = $('#form_type');
    var $initial = $('#initial_data');
    var $dataRequest = $('#data_request');
    var $submit = $('#submit');

    $selects.selectpicker('mobile').selectpicker('setStyle', 'btn-lg', 'add');

    $id.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $formType.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $initial.on('validate', function(evt, ret){
        ret.val = true;
    });

    $dataRequest.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $submit.on('click', function(){
        $('.alert').hide();
    });

});
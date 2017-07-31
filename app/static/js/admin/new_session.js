$(function(){

    var $first = $('#first');
    var $last = $('#last');
    var $id = $('#patient_id');
    var $date = $('#date');
    var $formName = $('.selectpicker');

    $formName.selectpicker('mobile').selectpicker('setStyle', 'btn-lg', 'add');

    $date.datepicker({
        todayBtn: "linked",
        orientation: 'auto right',
        autoclose: true,
        todayHighlight: true
    });

    $first.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $last.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $id.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $date.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $formName.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });
});
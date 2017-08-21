$(function(){

    var $form = $('form');
    var $first = $('#first');
    var $last = $('#last');
    var $id = $('#patient_id');
    var $date = $('#date');
    var $formName = $('#form_name');

    $form.formValidator();

    $formName.selectpicker('mobile').selectpicker('setStyle', 'btn-lg', 'add').formRequire({'length' : 1});

    $date.datepicker({
        todayBtn: "linked",
        orientation: 'auto right',
        autoclose: true,
        todayHighlight: true
    }).formRequire({'length' : 1});

    $first.formRequire({'length': 1});
    $last.formRequire({'length': 1});
    $id.formRequire({'length' : 1});


});
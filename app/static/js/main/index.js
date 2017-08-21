$(function(){

    var $form = $('form');
    var $id = $('#patient_id');
    var $first = $('#first_name');
    var $last = $('#last_name');

    $form.formValidator();

    $first.formRequire({'length': 1});
    $last.formRequire({'length': 1})
    $id.formRequire({'length': 1})

});
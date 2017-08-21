$(function(){

    var $form = $('form');
    var $first = $('#first');
    var $last = $('#last');
    var $id = $('#patient_id');

    $form.formValidator();

    $first.formRequire({'length' : 1});
    $last.formRequire({'length' : 1});
    $id.formRequire({'length' : 1});
});
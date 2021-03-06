$(function(){

    var $form = $('form');
    var $first = $('#first');
    var $last = $('#last');
    var $id = $('#patient_id');
    var $group = $('#group');
    var $dob = $('#dob');

    $form.formValidator();

    $group.selectpicker('setStyle', 'btn-lg').formRequire({'length' : 1});
    $first.formRequire({'length' : 1});
    $last.formRequire({'length' : 1});
    $id.formRequire({'length' : 1});
    $dob.formRequire({'date': true});

});
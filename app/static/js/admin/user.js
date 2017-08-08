$(function(){
    var $first = $('#first');
    var $last = $('#last');
    var $id = $('#patient_id');
    var $group = $('#group');

    $group.selectpicker('setStyle', 'btn-lg');

    $first.on('validate', function(evt, ret){
        ret.val = lengthVerify(evt, 1);
    });

    $last.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $id.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $group.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

});
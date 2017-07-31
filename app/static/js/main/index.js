$(function(){

    var $id = $('#patient_id');
    var $first = $('#first_name');
    var $last = $('#last_name');

    $first.on('validate', function(evt, ret){
       ret.val = lengthVerify(evt, 1);
    });

    $last.on('validate', function(evt, ret){
        ret.val = lengthVerify(evt, 1);
    });

    $id.on('validate', function(evt, ret){
        ret.val = lengthVerify(evt, 1);
    });

});
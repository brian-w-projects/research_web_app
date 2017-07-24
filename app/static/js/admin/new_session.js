$(function(){

    var $first = $('#first');
    var $last = $('#last');
    var $id = $('#patient_id');
    var $date = $('#date');
    var $submit = $('#submit');
    var $formName = $('.selectpicker');

    $formName.selectpicker('mobile');

    $date.datepicker({
        todayBtn: "linked",
        orientation: 'auto right',
        autoclose: true,
        todayHighlight: true
    });

    $first.add($last).add($id).add($date.datepicker()).add($formName).on('input changeDate', function(){
       if($first.val().length > 0 && $last.val().length > 0 &&
            $id.val().length > 0 && $date.val().length > 0 && $formName.val().length > 0){
           $submit.removeAttr('disabled');
       }else{
           $submit.attr('disabled', 'True');
       }
    });

    $submit.on('click', function(){
        $(this).button('loading');
    });
});
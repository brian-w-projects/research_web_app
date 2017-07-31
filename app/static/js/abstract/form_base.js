$(function(){
   var $form = $('form');
   var $submit = $('#submitValidate');

   $form.on('input change', function(){
        var valid = true;
        $(this).find(':input').filter(':visible').not(':input[type=button]').not($submit).each(function(){
            var ret = {ret:true};
            $(this).trigger('validate', [ret]);
            if(!ret.val){
                valid = false;
            }
        });
        if(valid === true){
            $submit.removeAttr('disabled');
        }else{
            $submit.attr('disabled', 'True');
        }
    });

   $submit.on('click', function(){
      $(this).button('loading');
   });

});

function lengthVerify(evt, len){
    var toRet = $(evt.currentTarget).val().length >= len;
    iconUpdate(evt, toRet);
    return toRet;
}

function emailVerify(evt){
    var pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    var toRet = $(evt.currentTarget).val().search(pattern) !== -1;
    iconUpdate(evt, toRet);
    return toRet;
}

function equalVerify(evt, otr){
    var toRet = $(evt.currentTarget).val() === otr.val();
    iconUpdate(evt, toRet);
    return toRet;
}

function iconUpdate(evt, process){
    var $toProcess = $(evt.currentTarget);
    if(process){
        if($toProcess.hasClass('selectpicker')){
            $toProcess.selectpicker('setStyle', 'btn-success', 'add');
        }else {
            $toProcess.parent().addClass('has-success');
            $toProcess.next().addClass('glyphicon-ok');
        }
    }else{
        if($toProcess.hasClass('selectpicker')){
            $toProcess.selectpicker('setStyle', 'btn-success', 'remove');
        }else {
            $toProcess.parent().removeClass('has-success');
            $toProcess.next().removeClass('glyphicon-ok');
        }
    }
}
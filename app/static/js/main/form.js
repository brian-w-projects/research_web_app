$(function(){
    var $submit = $('#previous, #next');
    var $form = $('form');
    var $radios = $(':radio');
    var $radiosContainer = $radios.parent().parent();
    var $selectpicker = $('.selectpicker');
    var $warning = $('#warning');
    var wide = true;


    if($(document).width() <= 1400){
        $form.find(':radio').parent().parent().remove();
        $selectpicker.selectpicker('mobile');
        wide = false;
    }else{
        $form.find('.selectpicker').remove();
        wide = true;
    }

    $warning.on('click', function(){
        $(this).hide();
    });

    $.each($selectpicker.add($radios).add($(':checkbox')), function(e){
        feedback($(this));
    });

    $form.on('change', function(e){
        feedback($(e.target));
    });


    $submit.on('click', function(e){
        e.preventDefault();
        var toSubmit = true;
        if(wide) {
            $radiosContainer.each(function () {
                var $skip = $(this).parent().parent().find(':checkbox');
                var $validate = $(this);
                if (!$skip.is(':checked')) {
                    if (!$validate.closest(':checkbox').is(':checked') && !$validate.hasClass('has-success')) {
                        $validate.addClass('has-error').find('span').addClass('glyphicon-warning-sign');
                        toSubmit = false;
                        $warning.show();
                    }
                }
            });
        }else{
            $selectpicker.each(function(){
                var $skip = $(this).parent().parent().parent().find(':checkbox');
                if (!$skip.is(':checked')) {
                    if (!$(this).parent().find('button').hasClass('btn-success')) {
                        toSubmit = false;
                        $warning.show();
                        $(this).selectpicker('setStyle', 'btn-danger', 'add');
                    }
                }
            });
        }

        if(toSubmit){
            $warning.hide();
            $(this).button('loading');
            $.ajax({
                type: 'POST',
                contentType: 'application/json;charset=UTF-8',
                url: submitData,
                data: JSON.stringify(objectifyForm($form.serializeArray(), $(e.target))),
                beforeSend: function(xhr, settings){
                    if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                        xhr.setRequestHeader('X-CSRFToken', csrf_token);
                    }
                }
            }).done(function(data){
                if(data['code'] === '201'){
                    window.location.href = nextPage;
                }else{
                    window.location.href = loginPage;
                }
            });
        }
    });

    function feedback($target){
        if($target.is(':checkbox')){
            if($target.is(':checked')) {
                var $toProcess = $target.closest('td').siblings();
                $toProcess.find(':radio').prop('checked', false).attr('disabled', 'true')
                    .parent().parent().removeClass('has-error has-success').find('span')
                    .removeClass('glyphicon-warning-sign glyphicon-ok');
                $toProcess.find('textarea').val('').attr('disabled', 'true');
                $toProcess.find('select').selectpicker('setStyle', 'btn-success', 'remove')
                    .selectpicker('setStyle', 'btn-danger', 'remove')
                    .selectpicker('setStyle', 'picker-disabled').prop('disabled', true)
                    .selectpicker('val', 'Select').selectpicker('refresh');
            }else{
                $target.closest('td').siblings().find(':radio, textarea').removeAttr('disabled');
                $target.closest('td').siblings().find('select').removeAttr('disabled')
                    .selectpicker('setStyle', 'picker-disabled', 'remove').selectpicker('refresh');
            }
        } else if($target.is('input') && $target.is(':checked')) {
            $target.parent().parent().removeClass('has-error').addClass('has-success')
                .find('span').addClass('glyphicon-ok').removeClass('glyphicon-warning-sign');
        } else if($target.is('select') && $target.val() !== '' && $target.val() !== null){
            $target.selectpicker('setStyle', 'btn-danger', 'remove')
                .selectpicker('setStyle', 'btn-success');
        }
    }
});

function objectifyForm(formArray, $dir){
    var returnArray = {};
    returnArray['forward'] = $dir.is('#next');
    for(var i = 0; i < formArray.length; i++){
        if($.isNumeric(formArray[i]['name'])){
            returnArray[formArray[i]['name']] = 'skip';
        }else if(formArray[i]['name'] !== 'csrf_token') {
            var space = formArray[i]['name'].indexOf(' ');
            var question = parseInt(formArray[i]['name'].substr(0,space));
            var prefix = formArray[i]['name'].substr(space+1);
            var value = formArray[i]['value'];
            if(!(question in returnArray)){
                returnArray[question] = {};
            }
            returnArray[question][prefix] = value;
        }
    }
    return returnArray;
}
$(function(){
    var $submit = $('#submit');
    var $form = $('form');
    var $radios = $(':radio');
    var $radiosContainer = $radios.parent().parent();
    var $selectpicker = $('.selectpicker');
    var $warning = $('#warning');
    var wide = true;
    var $help = $('#help');
    var $helpSign = $('.help-sign');

    if($(document).width() <= 420){
        $.each($helpSign, function(){
            $(this).on('click', function(){
                var left = $(this).offset().left + 20 - $(window).scrollLeft();
                var top = $(this).offset().top + 20 - $(window).scrollTop();
                $help.css('left', left).css('top', top).toggle();
            });
        });
    }else{
         $.each($helpSign, function(){
            $(this).on('mouseover mouseout', function(){
                var left = $(this).offset().left + 10 - $(window).scrollLeft();
                var top = $(this).offset().top + 10 - $(window).scrollTop();
                $help.css('left', left).css('top', top).toggle();
            });
        });
    }


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

        if(!toSubmit){
            e.preventDefault();
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
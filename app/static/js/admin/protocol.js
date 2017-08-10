$(function(){
   var current = initialShow===0? 1 : initialShow;
   var $row = $('#add-row');
   var $removeRow = $('#remove-row');
   var $submit = $('#submit');
   var $form = $('form');
   var $protocolType = $('.protocol-type');

   for(var i = 0; i < initialShow; i++){
       $("#row-" + i).show();
   }

   for(var i = 0; i < 10; i++){
       var $toCheck = $('#'+i+'-protocol-type');
       if($toCheck.val() === '2ch' && $('#'+(i-1)+'-protocol-type').val() === '2ch'){
           $toCheck.prop('disabled', true).selectpicker('refresh');
       }
    }

   if(initialShow === 0){
       $removeRow.hide();
   }else if(initialShow === 10){
       $row.hide();
   }

   $protocolType.on('changed.bs.select', function(){
       if($(this).val() === '2ch'){
           addRow();
           $('#'+(current-1)+'-protocol-type').prop('disabled', true).selectpicker('refresh');
       }
   });

   $row.on('click', addRow);

   $removeRow.on('click', function(){
      if(current !== 0){
          current--;
          $('#'+current+'-protocol-type').prop('disabled', false).selectpicker('refresh');
          $('#row-' + current).hide();
          $row.show();
      }
      if(current === 0){
          $removeRow.hide();
      }
   });

   $submit.on('click', function(e){
        e.preventDefault();
        $(this).button('loading');
        $form.find(':input:disabled').removeAttr('disabled');
        $.ajax({
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            url: submitData,
            data: JSON.stringify($form.find(':input:not(:hidden)').serializeArray()),
            beforeSend: function(xhr, settings){
                if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                }
            }
        }).done(function(data){
            if(data['code'] === '201'){
                window.location.href = redirect;
            }
        });
    });

   function addRow(){
       if(current !== 10){
           copyRows(current-1);
           $('#row-' + current).show();
           current++;
           $removeRow.show();
       }
       if(current === 10){
           $row.hide();
       }
    }
});


function copyRows(current){
    $('#row-'+(current)).find(':input').not('button').each(function(){
        $('#' + (current+1) + $(this).attr("id").substring(1)).val($(this).val())
            .selectpicker('val', $(this).val());
    });
}


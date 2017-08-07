$(function(){
   var current = initialShow;
   var $row = $('#add-row');
   var $removeRow = $('#remove-row');
   var $submit = $('#submit');
   var $form = $('form');

   for(var i = 0; i < initialShow; i++){
       $("#row-" + i).show();
   }

   if(initialShow == 0){
       $removeRow.hide();
   }else if(initialShow == 5){
       $row.hide();
   }

   $row.on('click', function(){
       if(current !== 5){
           copyRows(current-1);
           $('#row-' + current).show();
           current++;
           $removeRow.show();
       }
       if(current === 5){
           $row.hide();
       }
   });

   $removeRow.on('click', function(){
      if(current !== 0){
          current--;
          $('#row-' + current).hide();
          $row.show();
      }
      if(current === 0){
          $removeRow.hide();
      }
   });

   $submit.on('click', function(e){
        e.preventDefault();
        // $(this).button('loading');
        $.ajax({
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            url: submitData,
            data: JSON.stringify($form.serializeArray()),
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
});


function copyRows(current){
    $('#row-'+(current)).find(':input').not('button').each(function(){
        $('#' + (current+1) + $(this).attr("id").substring(1)).val($(this).val())
            .selectpicker('val', $(this).val());
    });
}
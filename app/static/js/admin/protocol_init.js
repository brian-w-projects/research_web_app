$(function(){

   var $id = $('#patient_id');
   var $dates = $('#dates');
   var $flashes = $('#p-error');

   $flashes.hide();

   $('#form_id').selectpicker('setStyle', 'btn-lg', 'add');

   $id.on('change', function(){
      $.ajax({
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            url: ajaxPatient,
            data: JSON.stringify({'id': $id.val()}),
            beforeSend: function(xhr, settings){
                if(!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader('X-CSRFToken', csrf_token);
                }
            }
        }).done(function(data){
            if(data['code'] === '201'){
                $flashes.hide();
                $id.attr('readOnly', true);
                var toAdd = '<select class="selectpicker show-tick" title="Dates" id="form_id" name="form_id">';
                for(ele in data){
                    if(ele !== 'code'){
                        toAdd += '<option value="' + data[ele][0] + '">' + data[ele][1] + '</option>';
                    }
                }
                toAdd += '</select>';
                $dates.html(toAdd);
                $('#form_id').selectpicker('setStyle', 'btn-lg', 'add').selectpicker('refresh');
            }else{
                $flashes.show();
            }
        });
   });

});
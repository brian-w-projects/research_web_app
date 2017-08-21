$(function(){

    $.fn.formRequire = function(options){
        this.addClass('form-require').data('optionsx', options || {'length': 0}).validate();
        return this;
    };


    $.fn.validate = function(){
           var valid = true;
           var options = this.data('optionsx');
           for(var opt in options){
               switch(opt){
                   case 'length':
                       valid = valid && this.val().length >= options[opt];
                       break;
                   case 'email':
                       var pattern = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                       valid = valid && this.val().search(pattern) !== -1;
                       break;
                   case 'equal':
                       valid = valid && this.val() === options[opt].val();
                       break;
                   case 'date':
                       var pattern = /^\d{2}\/\d{2}\/\d{4}$/;
                       valid = valid && this.val().search(pattern) !== -1;
                       break;
                   default:
                       valid = false;
                       break;
               }

           }
           if(valid){
               if(this.hasClass('selectpicker')){
                   this.selectpicker('setStyle', 'btn-success', 'add');
               }else {
                   this.parent().addClass('has-success');
                   this.next().addClass('glyphicon-ok');
               }
           }else{
               if(this.hasClass('selectpicker')){
                   this.selectpicker('setStyle', 'btn-success', 'remove');
               }else {
                   this.parent().removeClass('has-success');
                   this.next().removeClass('glyphicon-ok');
               }
           }
           return(valid);
        };


    $.fn.formValidator = function(){
        $(this).find(':input').filter(':visible').not(':input[type=button]').each(function(){
            if($(this).is(':submit')){
                $(this).on('click', function(){
                    $(this).button('loading');
                });
            }else{
                $(this).formRequire();
            }
        });
        $(this).on('input change', function(){
            var valid = true;
            $(this).find(':input').filter(':visible').not(':input[type=button]').not(':submit').each(function(){
                valid = $(this).validate() && valid;
            });
            if(valid === true){
                $(':submit').removeAttr('disabled');
            }else{
                $(':submit').attr('disabled', 'True');
            }
        });
    };
});
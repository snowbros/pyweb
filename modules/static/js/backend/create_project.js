$(document).ready(function(){
    var dialog;

    var init_model = function(data, options){
        if(dialog){
            dialog.remove();
            $('.modal-backdrop').remove();
        }
        dialog = $(data);
        $('body').append(dialog);
        dialog.modal(options);
        model_after_work(dialog);
        project_ajax_submit(dialog.find('form'));
        return dialog;
    }

    $('.action_new_project').on('click', function(){
       $.ajax('/get_project_model', {
            type: 'GET',
            data: [],
            contentType: 'application/json',
            success: function(data, textStatus, jqXHR){
                init_model(data, {});
            },
            error: function(jqXHR, textStatus, errorThrown){
               console.log(errorThrown);
            }
        });
    });

    var project_ajax_submit = function(form){
        $(form).ajaxForm({
            beforeSubmit: function(formData, jqForm, options){
                var color = _.findWhere(formData, {'name': 'color'});
                if(color.value){
                    return true;
                }else{
                    $(form).find(".color-picker .color-require").removeClass('hidden');
                    return false;
                }
            },
            success:function(responseText, statusText, xhr, $form){
                try {
                    var response = JSON.parse(responseText);
                    window.location.pathname = response.redirect;
                }
                catch(err) {
                    var d = init_model(responseText, {});
                }
            } 
        }); 
    };
});

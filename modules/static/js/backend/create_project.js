$(document).ready(function(){
    var dialog;

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

    $('.action_edit_project').on('click', function(){
        $.ajax('/get_project_model/'+$(this).data('id'), {
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
    

    $('.action_new_task').on('click', function(e){
       var project_id = $(".project_id").data('project-id');
       var ajax_data = {}
       if (project_id ){
            ajax_data = {'project_id': project_id}
       }
       var target = $(e.currentTarget)
       if(target.data('state')){
            ajax_data['state'] = target.data('state')
       }

       $.ajax('/get_task_model', {
            type: 'GET',
            data: ajax_data,
            contentType: 'application/json',
            success: function(data, textStatus, jqXHR){
                init_model(data, {});
            },
            error: function(jqXHR, textStatus, errorThrown){
               console.log(errorThrown);
            }
        });
    });

    $('.action_edit_task').on('click', function(){
        var project_id = $(".project_id").data('project-id');
        var ajax_data = {}
        if (project_id ){
             ajax_data = {'project_id': project_id}
        }
        $.ajax('/get_task_model/'+$(this).data('id'), {
             type: 'GET',
             data: ajax_data,
             contentType: 'application/json',
             success: function(data, textStatus, jqXHR){
                 init_model(data, {});
             },
             error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
             }
         });
    });

    $('.dropdown-move').on('click', function(e){
       var url = $(e.currentTarget).data('href');
       $.ajax(url, {
            type: 'GET',
            data: [],
            contentType: 'application/json',
            success: function(data, textStatus, jqXHR){
                window.location.pathname = window.location.pathname;
            },
            error: function(jqXHR, textStatus, errorThrown){
               console.log(errorThrown);
            }
        });
    });

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

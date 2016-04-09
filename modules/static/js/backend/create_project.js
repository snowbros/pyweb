$(document).ready(function(){
    var dialog;
    $('.action_new_project').on('click', function(){
       $.ajax('/get_project_model', {
           type: 'GET',
           data: [],
           contentType: 'application/json',
           success: function(data, textStatus, jqXHR){
                if(dialog){
                    dialog.remove();
                }
                dialog = $(data);
                $('body').append(dialog);
                dialog.modal({});
                model_after_work(dialog);
           },
           error: function(jqXHR, textStatus, errorThrown){
               console.log(errorThrown);
           }
       });
    });
});

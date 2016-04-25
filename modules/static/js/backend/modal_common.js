function model_after_work(dialog){

    $('#wrapwrap').addClass('blur');

    $(dialog).on('hidden.bs.modal', function () {
        $('#wrapwrap').removeClass('blur');
    });

    $(dialog).find('.form-group-date').datetimepicker({
         icons: {
             time: "fa fa-clock-o",
             date: "fa fa-calendar",
             up: "fa fa-arrow-up",
             down: "fa fa-arrow-down"
         },
         keepInvalid: true
     });

    $(dialog).find('.color-picker .color').on('click', function() {
         var parent = $(this).parent('.color-picker');
         $(parent).find('.active').removeClass('active');
         $(this).addClass('active');
         $(parent).find('input').val($(this).data('action'));
     });
    var user_autocomplete = $(dialog).find(".autocomplete_user");
    var user_autocomplete_hidden = $(dialog).find(".autocomplete_user_hidden");
    if(user_autocomplete.length > 0){
        $.ajax("/autocomplete/users", {
             type: 'GET',
             data: [],
             contentType: 'application/json',
             success: function(data, textStatus, jqXHR){
                 data = JSON.parse(data);
                 $(user_autocomplete).autocomplete({
                     lookup: data,
                     width: 250,
                     dataType: 'json',
                     onSelect: function (suggestion) {
                         $(user_autocomplete_hidden).val(suggestion.data);
                     }
                 });
             },
             error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
             }
         });
    }

    $(dialog).find('.flotting_form_backend .form-control').on('focus blur', function (e) {
        $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
        $(this).parents('.input-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
    }).trigger('blur');

};
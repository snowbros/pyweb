function model_after_work(dialog){

    $('#wrapwrap').addClass('blur');

    $(dialog).on('hidden.bs.modal', function () {
        $('#wrapwrap').removeClass('blur');
    });

    $(dialog).find('.flotting_form_backend .form-control').on('focus blur', function (e) {
        $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
        $(this).parents('.input-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
    }).trigger('blur');

    $(dialog).find('.form-group-date').datetimepicker({
         icons: {
             time: "fa fa-clock-o",
             date: "fa fa-calendar",
             up: "fa fa-arrow-up",
             down: "fa fa-arrow-down"
         }
     });

    $(dialog).find('.color-picker .color').on('click', function() {
         var parent = $(this).parent('.color-picker');
         $(parent).find('.active').removeClass('active');
         $(this).addClass('active');
         $(parent).find('input').val($(this).data('action'));
     });

};
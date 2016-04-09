$(document).ready(function() {
    // speed in milliseconds
    var scrollSpeed = 40;

    // set the direction
    var direction = 'h';

    // set the default position
    var current = 0;
    var current_y = 0;

    var bgscroll = function() {
        // 1 pixel row at a time
        current -= 1;
        if (Math.abs(current) % 2) {
            current_y -= 1;
        }

        // move the background with backgrond-position css properties
        $('.bg_pattern').css("background-position", current + "px " + current_y + "px");

    }

    //Calls the scrolling function repeatedly
    var init = setInterval(bgscroll, scrollSpeed);

    $('.flotting_form .form-control').on('focus blur', function (e) {
        $(this).parents('.form-group').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
    }).trigger('blur');
});
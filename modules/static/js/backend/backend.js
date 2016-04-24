$(document).ready(function(){
    model_after_work(document);
    $(document).trigger('hidden.bs.modal');
    _.each($('.moment_format_ago'), function(el){
        $(el).text(moment($(el).data('date')).fromNow(true) + ' ago'); 
    });
    var f_height = 0;
    _.each($('.same_height'), function(e){
        if(f_height < $(e).height()){
            $('.same_height').height($(e).height());
        }
    });

});
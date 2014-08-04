$(document).ajaxStart(function() {
   console.log('doing ajax');
    $(".loading_overlay").show();
});
$(document).ajaxComplete(function() {
   console.log('stopping ajax');
    $(".loading_overlay").hide();
});
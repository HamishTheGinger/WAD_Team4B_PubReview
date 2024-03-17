$(document).ready(function(){
    $(".recommend").on('click', function() {
        if(confirm("Do you want to recommend this pub?")) {
            location.href = $(this).data('uri');
        }
    });
});
$(document).ready(function(){
    $(".delete").on('click', function() {
        if(confirm("Do you want to delete it?")) {
            location.href = $(this).data('uri');
        }
    });
});
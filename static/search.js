$(document).ready(function(){
    $(".page-link").on('click', function() {
        $("#page").val($(this).data("page"));
        $("#searchForm").submit();
    });

    $("#btn_search").on('click', function() {
        $("#kw").val($(".kw").val());
        $("#page").val(1);
        $("#searchForm").submit();
    });

    $(".so").on('change', function() {
        $("#so").val($(this).val());
        $("#page").val(1);
        $("#searchForm").submit();
    });
});
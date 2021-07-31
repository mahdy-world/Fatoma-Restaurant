/**
 * Created by amk on 07/07/18.
 */

/* Fix Forms */
$('select').addClass('select2');
$('.select2').select2();
$('.select2-container').addClass('form-control');
$(':input:not(:checkbox, button)').addClass('form-control');
$("form").submit(function (e) {
    $("#submit_btn").attr("disabled", true);
});

$('.confirm-delete').on('click', function () {
    confirm('هل أنت متأكد من حذف هذا العنصر؟');
});
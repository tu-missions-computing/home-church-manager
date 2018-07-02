$(document).ready(function () {
    $('#checkbox1').change(function () {
        if (!this.checked) {
            $('.content').fadeOut('slow');
        } else {
            $('.content').fadeIn('slow');
        }
    });
});

// For smooth scrolling
$('a[href^="#"]').on('click', function (event) {
    var target = $(this.getAttribute('href'));
    if (target.length) {
        event.preventDefault();
        $('html, body').stop().animate({
            scrollTop: target.offset().top
        }, 1000);
    }
});

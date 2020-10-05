

$(document).ready(function () {
    $(".navbar-nav>li a").each(function () {
        // console.log("a",$this)
        if ($($(this))[0].href == String(window.location))
            $(this).parent().addClass('active');
    });

    $(".navbar-nav>li>div>a").each(function () {
        // console.log("a",$(this).parent().parent());
        if ($($(this))[0].href == String(window.location))
            $(this).parent().parent().addClass('active');

    });
});
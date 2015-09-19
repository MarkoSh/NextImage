$("#loginform input[type=submit]").click(function (e) {
    e.preventDefault();
    $("#loginform input[type=text], #loginform input[type=password]").each(function (idx, elem) {
        if ($(elem).val().length < 3) {
            $(elem).animate({
                backgroundColor: 'rgba(200, 80, 80, 0.8);'
            }, 100);
        }
        else {
            $(elem).animate({
                backgroundColor: 'rgba(255, 255, 255, 0.8);'
            }, 100);
        }
    });
});
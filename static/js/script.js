var feed = document.getElementsByClassName('feed')[0];
for (var i = 0; i < 128; i++) {
    feed.innerHTML += '<div class="inbody"></div>';
}
var inbodies = document.getElementsByClassName('inbody');
window.onscroll = function () {
    var scrolled = window.pageYOffset || document.documentElement.scrollTop;
    var wh = window.innerHeight;
    for (var i = 0; i < inbodies.length; i++) {
        if (!inbodies[i].innerHTML || inbodies[i].innerHTML == "undefined") {
            var elClientRec = inbodies[i].getBoundingClientRect();
            if (elClientRec.top < wh) {
                var postId = Math.floor(Math.random() * (500 - 1) + 1);
                inbodies[i].innerHTML = '<a href="/' + postId + '" class="postlink"><span class="icons"><i class="material-icons">photo</i></span><img src="http://lorempixel.com/330/200/?' + postId + '" />';
                inbodies[++i].innerHTML = '<a href="/' + postId + '" class="postlink"><span class="icons"><i class="material-icons">play_arrow</i><i class="material-icons">hd</i></span><img src="http://lorempixel.com/330/200/?' + (++postId) + '" />';
                inbodies[++i].innerHTML = '<a href="/' + postId + '" class="postlink"><span class="icons"><i class="material-icons">play_arrow</i></span><img src="http://lorempixel.com/330/200/?' + (++postId) + '" />';
            }
        }
    }
};
window.onresize = window.onscroll;
window.onscroll();
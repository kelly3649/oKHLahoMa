var scrolldown = function(element){
    var rect = element.getBoundingClientRect();
    var offsetTop = rect.top;
    console.log(offsetTop);
    window.scrollBy(offsetTop);
};

var link = document.getElementById("linkToAbout");

link.onclick = function(){
    var about = document.getElementById("about");
    scrolldown(about);
    return false;
};

/* js for the link to the about
 * will move the screen down to the about section
 * seems as if you went to a whole new page! (but you didn't)
*/

var scrolldown = function(element){
    var rect = element.getBoundingClientRect();
    var offsetTop = rect.top;
    window.scrollBy(offsetTop);
};

var link = document.getElementById("linkToAbout");

link.onclick = function(){
    var about = document.getElementById("about");
    scrolldown(about);
    return false;
};

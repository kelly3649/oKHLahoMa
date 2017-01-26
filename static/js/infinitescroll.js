var nextPageToLoad = 1;
var hasMore = true;


/* runs every time user scrolls
 * checks if user reached the bottom
 * if not, do nothing
 * if so, use ajax to call the function to get more posts
   * append the posts to the page HTML
   * if function returns no posts then no more posts to be displayed, 
     hasMore = false,
     next time user reaches the bottom, don't bother calling the ajax anymore 
     because you know you finished fetching all the posts
*/
var loadMore = function(){
    
    if (hasMore && window.innerHeight + document.body.scrollTop >= document.body.clientHeight){
	var loadingGIF = document.getElementById("loading");
	loadingGIF.style.display = "block"; /* unhide loading gif */
	var ownprofile = document.getElementById("ownprofile").innerHTML;
	var user = document.getElementById("profileLabel").innerHTML;
	if (user == "")
	    var type = "feed";
	else
	    var type = "profile";
	
	var input = {
	    'type': type,//feed or profile
	    'user': user,
	    'page': nextPageToLoad
	};
	
	$.ajax({
	url: '/loadMore',
	type: 'GET',
	data: input,
	success: function( d ) {
	    d = JSON.parse(d);
	    var postArea = document.getElementById("thePosts");
	    if (d.length == 0){
		hasMore = false;
	    }
	    else {
		for (var key in d){
		    var entry = d[key];

		    var img = '<img class="img-responsive" src="' + entry['photo_link']  + '" alt="' + entry['caption'] + '">';

		    var authorTag = '<a href="/profile/' + entry['author'] + '">' + entry['author'] + '</a>';
		    
		    var caption = '<i>' + entry['caption'] + '</i>';

		    var deleteButton = "";

		    if (ownprofile == "ownprofile"){
			deleteButton += '<form action="delete" method="POST">\
<input name="postid" type="hidden" value="' + entry['post_id'] + '"/>\
<input class="btn" type="submit" value="Delete Post"/>\
</form>'
		    }

		    
		    var post = img + '<br>by ' + authorTag + ' on ' + entry['uploadDate'] + '<br>' + caption + deleteButton + '<br><hr><br><br>';

		    postArea.innerHTML = postArea.innerHTML + post;

		}
	    }
	    
	    nextPageToLoad += 1;
	    loadingGIF.style.display = "none"; /* hide loading gif */
	}

     });
	
    }
	
}

var attach = function(){
    window.addEventListener("scroll", loadMore);
    loadMore(); //run the fxn in case the user is at the bottom once the page loads
}

/* only allow this to happen once page is loaded*/
window.onload = attach;

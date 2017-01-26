var nextPageToLoad = 1;
var hasMore = true;

var loadMore = function(){
    
    if (hasMore && window.innerHeight + document.body.scrollTop >= document.body.clientHeight){
	var loadingGIF = document.getElementById("loading");
	loadingGIF.style.display = "block"; /* unhide loading gif */
	
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
	url: '/loadMoreFollowed',
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

		    var post = img + '<br>by ' + authorTag + ' on ' + entry['uploadDate'] + '<br>' + caption + '<br><hr><br><br>';

		    postArea.innerHTML = postArea.innerHTML + post;

		}
	    }
	    
	    nextPageToLoad += 1;
	    loadingGIF.style.display = "none"; /* hide loading gif */
	}

     });
	
    }
	
}

window.addEventListener("scroll", loadMore);

var nextPageToLoad = 1;

var loadMore = function(){
    
    if (window.innerHeight + document.body.scrollTop >= document.body.clientHeight){
	var loadingGIF = document.getElementById("loading");
	loadingGIF.style.display = "block"; /* unhide loading gif */
	console.log("success.");

	
	var input = {
	    'type': 'feed',//feed or profile
	    'user': '',
	    'page': nextPageToLoad
	};
	
	$.ajax({
	url: '/loadMore',
	type: 'GET',
	data: input,
	success: function( d ) {
	    d = JSON.parse(d);
	    var postArea = document.getElementById("thePosts");
	    console.log("this is d")
	    console.log(d)
	    for (var key in d){
		var entry = d[key];

		var img = '<img class="img-responsive" src="' + entry['photo_link']  + '" alt="' + entry['caption'] + '">';

		var authorTag = '<a href="/profile/' + entry['author'] + '">' + entry['author'] + '</a>';
		    
		var caption = '<i>' + entry['caption'] + '</i>';

		var post = img + '<br>by ' + authorTag + ' on ' + entry['uploadDate'] + '<br>' + caption + '<br><hr><br><br>';
		console.log(post);

		postArea.innerHTML = postArea.innerHTML + post;
		
	    }

	    loadingGIF.style.display = "none";
	}

     });
	
    }
    else
	console.log("failure");
}

window.addEventListener("scroll", loadMore);

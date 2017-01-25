var nextPageToLoad = 1;
var hasMore = true;

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
		    console.log(post);

		    postArea.innerHTML = postArea.innerHTML + post;

		}
	    }
	    
	    nextPageToLoad += 1;
	    loadingGIF.style.display = "none"; /* hide loading gif */
	}

     });
	
    }
    else {
	console.log("fail");
    }
	
}

var attach = function(){
    window.addEventListener("scroll", loadMore);
    loadMore();
}

window.onload = attach;

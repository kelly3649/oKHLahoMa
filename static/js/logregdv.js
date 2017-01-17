var usernameAvailable = function(username) {
    var input = { 'text' : username};

    $.ajax({
	url: '/checkUser',
	type: 'GET',
	data: input,
	success: function( d ) {
	    d = JSON.parse(d);
	    available = d['available'];
	    var place = document.getElementById("usernameTaken");
	    if (! available){
		place.innerHTML = "Username taken.";
	    }
	    else {
		place.innerHTML = "<br>";
	    };
	    return available;
	}

    });
};


var validateLogin = function(){
    console.log("validateIsRunning");
    var username = document.forms["login"]["username"].value;
    var pass1 = document.forms["login"]["password"].value;
    var alertmsg = "";

    if (username == ""){
	alertmsg += "* Please enter your username.<br>";
    }

    if (pass1 == ""){
	alertmsg += "* Please enter your password.<br>";
    }

    if (alertmsg != ""){
	alertmsg += "<br>";
	var error = document.getElementById("loginerror");
	error.innerHTML = alertmsg;
	return false;
    }
};

var validateRegister = function(){
    var success = true;
    
    var username = document.forms["register"]["username"].value;
    var pass1 = document.forms["register"]["password"].value;
    var pass2 = document.forms["register"]["confirm_password"].value;
    var alertmsg = "";
    
    if (! usernameAvailable(username)){
	success = false;
    }

    if (username == ""){
	alertmsg += "* Username required.<br>";
    }
    
    if (pass1 == "" || pass2 == ""){
	alertmsg += "* Both password fields required.<br>";
    }
    else if (pass1 != pass2){
	alertmsg += "* Passwords do not match.<br>";
    };
    if (pass1.length < 10){
	alertmsg += "* Password must be at least 10 characters long.<br>";
    };
    if (alertmsg != ""){
	alertmsg += "<br>";
	var error = document.getElementById("regerror");
	error.innerHTML = alertmsg;
	success = false;
    };
    return success;
};



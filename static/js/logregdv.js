
/* uses ajax to check if username is available (for register)*/
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
	}
    });
};

/* checks that username and password fields filled in */
var validateLogin = function(){
    var username = document.forms["login"]["username"].value;
    var pass1 = document.forms["login"]["password"].value;
    var alertmsg = "";

    if (username == ""){
	alertmsg += "* Please enter your username.<br>";
    }

    if (pass1 == ""){
	alertmsg += "* Please enter your password.<br>";
    }

    var error = document.getElementById("loginerror");
    
    if (alertmsg == ""){
	error.innerHTML = "<br>";
    }
    else {
	alertmsg += "<br>";
	error.innerHTML = alertmsg;
	return false;
    }
};

/* checks register form: 
   * all fields filled in
   * password meets 10 char req 
   * username is available 
*/

var validateRegister = function(){
    var success = true;

    var username = document.forms["register"]["username"].value;
    var pass1 = document.forms["register"]["password"].value;
    var pass2 = document.forms["register"]["confirm_password"].value;


    var error = document.getElementById("regerror");
    error.innerHTML = "";
    
    var alertmsg = "";

    usernameAvailable(username);

    var unameTaken = document.getElementById("usernameTaken");
    
    if (unameTaken.innerHTML != "<br>"){
	success = false;
    }
    
    if (username == ""){
	error.innerHTML = error.innerHTML + "* Username required.<br>";
	success = false;
    }
   
    if (pass1 == "" || pass2 == ""){
	error.innerHTML = error.innerHTML + "* Both password fields required.<br>";
	success = false;	
    }
    else if (pass1 != pass2){
	error.innerHTML = error.innerHTML + "* Passwords do not match.<br>";
	success = false;	
    };

    if (pass1.length < 10){
	error.innerHTML = error.innerHTML + "* Password must be at least 10 characters long.<br>";
	success = false;	
    };

    return success;
};

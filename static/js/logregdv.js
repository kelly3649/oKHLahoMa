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
    if (alertmsg != ""){
	alertmsg += "<br>";
	var error = document.getElementById("loginerror");
	error.innerHTML = alertmsg;
	return false;
    }
};

var validateRegister = function(){
    var username = document.forms["register"]["username"].value;
    var pass1 = document.forms["register"]["password"].value;
    var pass2 = document.forms["register"]["confirm_password"].value;
    var alertmsg = "";
    if (username == ""){
	alertmsg += "* Username required.<br>";
    }
    
    if (pass1 == "" || pass2 == ""){
	alertmsg += "* Both password fields required.<br>";
    }
    else if (pass1 != pass2){
	alertmsg += "* Passwords do not match.<br>";
    }
    if (pass1.length < 10){
	alertmsg += "* Password must be at least 10 characters long.<br>";
    }
    if (alertmsg != ""){
	alertmsg += "<br>";
	var error = document.getElementById("regerror");
	error.innerHTML = alertmsg;
	return false;
    }
    
};

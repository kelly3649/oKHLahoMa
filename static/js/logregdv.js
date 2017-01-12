var showValidationError = function(text){
    var error = document.getElementById("dverror");
    error.innerHTML = text;
};

var validateRegister = function(){
    var username = document.forms["register"]["username"].value;
    var pass1 = document.forms["register"]["password"].value;
    var pass2 = document.forms["register"]["confirm_password"].value;
    var alertmsg = "";
    if (username == ""){
	alertmsg += "Username required.\n";
    }
    
    if (pass1 == "" || pass2 == ""){
	alertmsg += "Both password fields required.\n";
    }
    if (pass1 != pass2){
	alertmsg += "Passwords do not match.\n";
    }
    if (pass1.length < 10){
	alertmsg += "Password must be at least 10 characters long.";
    }
    if (alertmsg != ""){
	showValidationError(alertmsg);
	return false;
    }
    
};


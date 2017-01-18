var filenoodle = document.getElementById("noot");
var labelnoodle = document.getElementById("file-label");

filenoodle.onchange = function() {
    console.log("DOG");
    labelnoodle.innerHTML = this.value.substr(12);
};

var loadPhoto = function() {
    var formnoodle = document.getElementById("datform");
    formnoodle.removeChild(document.getElementById("temporary"));
    var file = document.getElementById("noot").files[0];
    var reader = new FileReader();
    reader.onload = function(imgfile) {
	document.getElementById("lul").value = imgfile.target.result;
	var submitButton = document.createElement("INPUT");
	submitButton.setAttribute("type", "submit");
	submitButton.className += "btn btn-default";
	formnoodle.appendChild(submitButton);
    };
    reader.readAsDataURL(file);
};

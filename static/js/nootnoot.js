var printPhoto = function() {
    document.getElementById("check").innerHTML = "hold on";
    
    var file = document.getElementById("noot").files[0];
    
    var reader = new FileReader();

    reader.onload = function(imgfile) {
	document.getElementById("lul").value = imgfile.target.result;
	document.getElementById("check").innerHTML = "done with a size of " + lul.value.length + " bytes";
    };

    reader.readAsDataURL(file);
};

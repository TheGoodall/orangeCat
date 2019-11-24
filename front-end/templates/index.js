function toggleCentreSearch(){
    
}

document.addEventListener("DOMContentLoaded", function(){
    
    var modalTutor = document.getElementById("signUpTutor");
    var modalTutee = document.getElementById("signUpTutee");

    window.onclick = function(event) {
        if(event.target == modalTutor){
            modalTutor.style.display = "none";
        }else if(event.target == modalTutee){
            modalTutee = "none";
        }
    }
});
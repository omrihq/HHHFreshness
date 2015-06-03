window.onload = function(){
    var a = false;
    
    document.getElementById('redspan').onclick = function() {
        if(a == false) {
            document.getElementById('frame1').style.height = "166px";
            a = true;
        } else {
            document.getElementById('frame1').style.height = "0px";
            a = false;
    }
    
    }
}
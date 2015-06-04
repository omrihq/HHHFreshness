/*window.onload = function(){
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
}*/

function reply_click(clicked_id){
    var a = false
    alert(clicked_id)
    if(a == false) {
        var idtofind = clicked_id + "-frame"
        document.getElementById(idtofind).style.height = "166px";
        a = true;
    } else {
        document.getElementById(idtofind).style.height = "0px";
        a = false;
    }
    
}
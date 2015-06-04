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
    if(document.getElementById(clicked_id).getAttribute("value") == "off") {
        console.log(document.getElementById(clicked_id).getAttribute("value"))
        var idtofind = clicked_id + "-frame"
        document.getElementById(idtofind).style.height = "166px";
        document.getElementById(clicked_id).setAttribute("value", "on")
    } else {
        var idtofind = clicked_id + "-frame"
        document.getElementById(idtofind).style.height = "0px";
        document.getElementById(clicked_id).setAttribute("value", "off")
    }
}
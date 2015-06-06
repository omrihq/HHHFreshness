

function reply_click(clicked_id){
    if(document.getElementById(clicked_id).getAttribute("value") == "off") {
        var idtofind = clicked_id + "-frame"
        document.getElementById(idtofind).style.height = "166px";
        document.getElementById(clicked_id).setAttribute("value", "on")
    } else {
        var idtofind = clicked_id + "-frame"
        document.getElementById(idtofind).style.height = "0px";
        document.getElementById(clicked_id).setAttribute("value", "off")
    }
}

function donate() {
    window.open("https://www.booksforafrica.org/donate/funds.html")
}

function github() {
    window.open("https://github.com/omrihq/HHHFreshness")
}

function reddit() {
    window.open("http://www.reddit.com/r/hiphopheads")
}
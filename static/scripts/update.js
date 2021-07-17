/**
 * Updates elements on the home page.
 */
function update_home(){
    interval = 0;
    setInterval(function(){ 
        let date = new Date();
        $("#time").text((date.getHours()>12?date.getHours()-12:date.getHours()) + ":" + (date.getMinutes()<10?'0':'') + date.getMinutes());

        //Get temperature every 60 seconds
        if(interval == 60000){
            interval = 0;
            $.getJSON($SCRIPT_ROOT + '/update_home', {
            }, function(data) {
                $("#temp").text(data.weather +"°");
            }); 
        }
        interval++;
    }, 1000); 
}

if(location.href != "/" && location.href != "/invis"){
    window.addEventListener("load", timeout, true);
    document.onmouseout = function(){
        timeout();
    }
}

function timeout(){
    clearTimeout(time);
    var time = setTimeout(function(){ 
        location.href = '/invis';
    }, 300000);
}
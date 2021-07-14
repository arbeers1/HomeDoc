const date = new Date();
/**
 * Updates elements on the home page.
 */
function update_home(){
    interval = 0;
    setInterval(function(){ 

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
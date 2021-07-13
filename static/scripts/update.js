/**
 * Updates elements on the home page.
 */
function update_home(){
    interval = 0;
    get_weather = false;
    setInterval(function(){ 
        if(interval == 60000){
            get_weather = true;
            interval = 0;
        }else{
            get_weather = false;
        }
        interval++;

        //Get request for time/weather. Weather only updates once every 5 mins.
        $.getJSON($SCRIPT_ROOT + '/update_home', {
            weather: get_weather
        }, function(data) {
          $("#time").text(data.time);
          if(get_weather){
              $("#temp").text(data.weather +"°");
          }
        });    
    }, 1000); 
}
/**
 * Builds the html page for the given number of lights.
 * @param {*} num - the number of buttons to create
 */
function populate_buttons(num){
    for(var i = 0; i < num; i++){
        (function(){
            //Create Light Buttons
            var element = document.getElementById("button_container");
            var button = document.createElement("button");
            button.innerHTML = 'Button '+i;
            button.id = i + 'b';
            element.appendChild(button);
            button.className = "lights";
            button.addEventListener ("click", function() {
               if(menu.style.height == '30vh'){
                    menu.style.height = '0vh'
                    chooser.style.visibility = 'hidden';
                    power.style.visibility = 'hidden';
                    slider.style.visibility = 'hidden';
               }else{
                    menu.style.height = '30vh';
               }
            });

            //Div for power and color controls
            var power_container = document.createElement("div");
            power_container.className = "power_container";

            //Light dialogue
            var chooser = document.createElement("input");
            chooser.type = "color";
            chooser.className = "chooser";
            chooser.id = i;
            chooser.addEventListener("input", function(){set_color(chooser);});

            //Power button
            var power = document.createElement("label");
            power.className = "power";
            power.innerHTML = ""; 
            power.style.color = "#f01b24";
            power.addEventListener("click", function(){
                if(power.style.color == "rgb(240, 27, 36)"){
                    power.style.color = "#3ab64a";
                }else{
                    power.style.color = "#f01b24";
                }
            });

            //Brightness div
            var bri_container = document.createElement("div");

            //Brightness slider
            var slider = document.createElement("input");
            slider.className = "slider"
            slider.type = "range";
            slider.min = 1;
            slider.max = 100;

            //Slide Down Menu 
            var menu = document.createElement("div");
            element.appendChild(menu);
            menu.className = "light_info";
            menu.id = i;
            menu.addEventListener("transitionend", function(){
                if(menu.style.height == '30vh'){
                    chooser.style.visibility = 'visible';
                    power.style.visibility = 'visible';
                    slider.style.visibility = 'visible';
                }
            });

            menu.appendChild(power_container);
            menu.appendChild(bri_container);
            power_container.appendChild(chooser);
            power_container.appendChild(power);
            bri_container.appendChild(slider);
        })();
    }
}

function set_color(chooser){
    document.getElementById(chooser.id + 'b').style = "background-color: " + chooser.value;
}
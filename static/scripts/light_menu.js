function get_lights(){
    $.getJSON($SCRIPT_ROOT + '/update_lights', {
    }, function(data) {
        populate_buttons2(data);
    }); 
}

function dynamic_update(){
    setInterval(function(){
        $.getJSON($SCRIPT_ROOT + '/update_lights', {
        }, function(data) {
            for(var i = 0; i < data.main.length; i++){
                $('#' + i).val(data.main[i][3]);
                var col = data.main[i][2]?"#3ab64a":"#f01b24";
                $('#' + i + 'p').css('color', col);
                button_col = data.main[i][2]?data.main[i][3]:'#373737';
                $('#' + i + 'b').css('background-color', button_col);
                $('#' + i + 's').val(data.main[i][4] / 255 * 100);
            }   
        }); 
    }, 1000);
}

function populate_buttons2(light_data){
    for(var i = 0; i < light_data.main.length; i++){
        (function(){
            //Sub-Menu container
            var $power_container = $('<div class="power_container"></div>');

            light_col = light_data.main[i][3];
            //Color dialogue
            var $chooser = $('<input/>',{
                type: "color",
                class: 'chooser',
                id: i,
                value: light_col
            });
            $chooser.on('input', function(){
                $button.css("background-color", $chooser.val());
                $.post($SCRIPT_ROOT + '/update_lights', {
                    id: parseInt($chooser.attr('id')) + 1,
                    state: false,
                    state_val: null,
                    color: true,
                    color_val: $chooser.val(),
                    bri: false,
                    bri_val: null
                }, function(data) {}); 
            });
            
            //Power button
            var col = light_data.main[i][2]?"#3ab64a":"#f01b24";
            var $power = $('<label/>', {
                text: "",
                class: "power",
                id: i + 'p',
                style: "color: " + col,
                click: function(){
                    col = col == "#3ab64a"?"#f01b24":"#3ab64a";
                    $power.css("color", col)
                    var state_setting = col=="#3ab64a"?true:false;
                    var button_color = state_setting?$chooser.val():'#373737';
                    $button.css("background-color", button_color);
                    $.post($SCRIPT_ROOT + '/update_lights', {
                        id: parseInt($chooser.attr('id')) + 1,
                        state: true,
                        state_val: state_setting,
                        color: false,
                        color_val: null,
                        bri: false,
                        bri_val: false
                    }, function(data) {}); 
                }
            });

            //Brightness slider
            var $bri_container = $('<div/>');
            var $slider = $('<input/>', {
                type: "range",
                class: "slider",
                id: i + 's',
                min: 1,
                max: 100,
                val: light_data.main[i][4] / 255 * 100
            });

            $slider.on('input', function(){
                $.post($SCRIPT_ROOT + '/update_lights', {
                    id: parseInt($chooser.attr('id')) + 1,
                    state: false,
                    state_val: null,
                    color: false,
                    color_val: null,
                    bri: true,
                    bri_val: $slider.val()
                }, function(data) {}); 
            });

            //Slide down menu
            var $menu = $('<div/>', {
                id: "m"+i,
                class: 'light_info',
            });
            $menu.on("transitionend", function(){
                if($menu.height() > 0){
                    $chooser.css('visibility', 'visible');
                    $power.css('visibility', 'visible');
                    $slider.css('visibility', 'visible');
                }
            });

            button_col = light_data.main[i][2]?light_col:'#373737';
            //Create a button for each light
            var $button = $('<button/>', {
                text: light_data.main[i][1], //set text 1 to 10
                id: i+'b',
                class: 'lights',
                style: 'background-color: ' + button_col,
                click: function () { 
                    if($menu.height() > 0){
                        $menu.height('0vh');
                        $chooser.css('visibility', 'hidden');
                        $power.css('visibility', 'hidden');
                        $slider.css('visibility', 'hidden');
                    }else{
                        $menu.height("30vh");
                    }
                }
            });

            $button.appendTo($("#button_container"));
            $menu.appendTo($("#button_container"));
            $power_container.appendTo($menu);
            $bri_container.appendTo($menu);
            $chooser.appendTo($power_container);
            $power.appendTo($power_container);
            $slider.appendTo($bri_container);          
        })();
    }

    dynamic_update();
}

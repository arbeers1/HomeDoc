var play = true;
var device_vis = false;

function set_device(device=null){
    if(device_vis){
        document.getElementById("drop_menu").style = "visibility: hidden;";
    }else{
        document.getElementById("drop_menu").style = "visibility: visible;";
    }
    device_vis = !device_vis;
}

function set_control(){
    if(play){
        document.getElementById("play").innerText = "";
    }else{
        document.getElementById("play").innerText = "";
    }
    play = !play;
}

function populate_playlists(num){
    for(var i = 0; i < num; i++){
        (function(){
            var element = document.getElementById("navigation");
            var button = document.createElement("button");
            button.innerHTML = 'Button '+i;
            button.id = i + 'b';
            button.className = "nav_selector";
            element.appendChild(button);
            button.addEventListener("click", function(){ populate_songs(button, num, 15); });
        })();
    }
}

function populate_songs(button, num, num_songs){
    document.getElementById("inner_title").innerText = button.innerText
    document.getElementById("song_back").style = "visibility: visible;"
    for(var i = 0; i < num; i++){
        document.getElementById(i + 'b').remove();
    }
    for(var i = 0; i < num_songs; i++){
        var element = document.getElementById("navigation");
        var button = document.createElement("button");
        button.innerHTML = 'song';
        button.id = i + 'b';
        button.className = "nav_selector";
        element.appendChild(button);
    }
}

function back(){
    songs = document.getElementsByClassName("nav_selector");
    remove(songs, songs.length);
    populate_playlists(5);
    document.getElementById("inner_title").innerText = "Playlists"
    document.getElementById("song_back").style = "visibility: hidden;"
}

function remove(songs, i){
    if(i > 0){
        songs[i - 1].remove();
        remove(songs, i - 1);
    }
}

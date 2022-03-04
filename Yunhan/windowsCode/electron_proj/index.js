document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var video_port = 8000;
var server_addr = "192.168.3.14";   // the IP address of your Raspberry PI

// The general function to send data to the server
function send_command(cmd){
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send command
        
        client.write(cmd);
        
    });


    // get the data from the server
    client.on('data', (data) => {
        data = data.toString()
        console.log(data);
        document.getElementById("bluetooth").innerHTML = data;
        console.log(data.toString());
        if (data.substr(0, 11) == "temperature")
        {
            document.getElementById("temperature").innerHTML = data.substr(11);
        }


        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '38') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_command("38")
    }
    else if (e.keyCode == '40') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_command("40")
    }
    else if (e.keyCode == '37') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_command("37")
    }
    else if (e.keyCode == '39') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_command("39")
    }
}


// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}


// update data for every 50ms
function update_cmd(){

    /*
    setInterval(function(){
        // get image from python server
        var cmd = document.getElementById("message").value;
        send_command(cmd);
    }, 50);
    */
    var cmd = document.getElementById("message").value;
    send_command(cmd);
}

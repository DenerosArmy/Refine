console.log("Opening WS connection");
var connection = new WebSocket('ws://198.61.194.98:9000/get_sf_updates')

// When the connection is open, send some data to the server
connection.onopen = function () {
    connection.send("Jifi");
};

// Do stuff based on message
connection.onmessage = function (msg) {
    var data = JSON.parse(msg.data);

    if (data['op'] == '+') {
        console.log('Adding card');
        addCard(data);
    }
    else if (data['op'] == '-') {
        console.log('Removing card');
        removeCards(data);
    }
    setTimeout(connection.onopen, 100);
};

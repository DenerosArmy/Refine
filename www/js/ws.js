console.log("Opening WS connection");
var connection = new WebSocket('ws://198.61.194.98:9000/get_airport_updates')

// When the connection is open, send some data to the server
connection.onopen = function () {
    connection.send("Jifi");
};

// Do stuff based on message
connection.onmessage = function (msg) {
    var data = JSON.parse(msg.data);

    if (data['op'] == '+') {
        //addCard(data);
    }
    else if (data['op'] == '-') {
        //removeCards(data);
    }
    setTimeout(connection.onopen, 100);
};

DATA = {
    destination: "Miami, FL",
    display_name:  "Richie Z.",
    flight_gate: "G45",
    flight_number: "UA 456",
    departure_time: "11:24 AM",
    arrival_time: "5:31 PM",
    op: "+",
    profile_image_url: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc1/372355_590037593_561933968_q.jpg",
    type: "flight_info",
    user_name: "richie_zeng",
}


TYPE_TO_TITLE = {
    'flight_info': 'Flight Details',
}

cardStack = {}


function addCard(data) {
    console.log(data);
    if (data['type'] == 'flight_info') {
        var card = buildFlightCard(data);
    }
    else {
        var card = buildCardWithHeader(data);
    }
    var id = data['user_name'] + '-' + data['type'];

    document.getElementById('card-column').appendChild(card);

    if (!cardStack[data['user_name']]) {
        cardStack[data['user_name']] = []
    }

    cardStack[data['user_name']].push(id);

    setTimeout(function () {
        $('div#' + id + '.card').removeClass('hidden');
    }, 0);
}


function removeCards(data) {
    if (cardStack[data['user_name']].length != 0) {
        var id = cardStack[data['user_name']].pop();

        setTimeout(function () {
            $('div#' + id + '.card').addClass('hidden');
            removeCards(data);
        }, 200);
    }

    setTimeout(function (){
        var column = document.getElementById('card-column')
        while (column.hasChildNodes()) {
            column.removeChild(column.lastChild);
        }
    }, 1000);
}

function buildCardWithHeader(data) {
    var id = data['user_name'] + '-' + data['type'];
    
    var card = document.createElement('div');
    card.setAttribute('class', 'card hidden');
    card.setAttribute('id', id);

    var cardHeader = document.createElement('div');
    cardHeader.setAttribute('class', 'card-header');
    cardHeader.setAttribute('id', id);
    card.appendChild(cardHeader);

    var cardImageContainer = document.createElement('div');
    cardImageContainer.setAttribute('class', 'card-image-container');
    cardHeader.appendChild(cardImageContainer);

    var cardImage = document.createElement('div');
    cardImage.setAttribute('class', 'card-image');
    cardImage.setAttribute('style', "background-image:url('" + data['profile_image_url'] + "')");
    cardImageContainer.appendChild(cardImage);

    var cardTitle = document.createElement('p');
    cardTitle.setAttribute('class', 'card-title');
    cardTitle.innerHTML = TYPE_TO_TITLE[data['type']]
    cardHeader.appendChild(cardTitle);

    var personName = document.createElement('p');
    personName.setAttribute('class', 'person-name');
    personName.innerHTML = data['display_name'];
    cardHeader.appendChild(personName);

    return card;
}

function buildFlightCard(data) {
    var card = buildCardWithHeader(data);

    var cardContent = document.createElement('div');
    cardContent.setAttribute('class', 'card-content');
    card.appendChild(cardContent);
    
    var flightInfo = document.createElement('p');
    flightInfo.setAttribute('class', 'flight-info');
    flightInfo.innerHTML = "United Airlines flight <em>" + data['flight_number'] + "</em> to <em>" + data['destination'] + "</em>";
    cardContent.appendChild(flightInfo);

    var flightDeparture = document.createElement('div');
    flightDeparture.setAttribute('class', 'departure');
    flightDeparture.innerHTML = "<p class='title'>Departure</p> <p class='info'>Gate 48 &nbsp;&nbsp;<em>" + data['departure_time'] + "</em></p>";

    var flightArrival = document.createElement('div');
    flightArrival.setAttribute('class', 'arrival');
    flightArrival.innerHTML = "<p class='title'>Arrival</p> <p class='info'>Gate 24 &nbsp;&nbsp;<em>" + data['arrival_time'] + "</em></p>";

    cardContent.appendChild(flightDeparture);
    cardContent.appendChild(flightArrival);


    return card
}

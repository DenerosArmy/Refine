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

DATA2 = {
    destination: "Miami, FL",
    display_name:  "Jian L.",
    flight_gate: "G45",
    flight_number: "UA 456",
    departure_time: "11:24 AM",
    arrival_time: "5:31 PM",
    op: "+",
    profile_image_url: "https://lh6.googleusercontent.com/-TpuvTBw3vx8/UQM7IOmkmBI/AAAAAAAAAbI/DzNehhnVEWE/w256-h257-no/375563_10151168765508994_657905193_n.jpeg",
    type: "flight_info",
    user_name: "jian_leong",
}

RENTAL_DATA = {
    cars: [{
            model: "Honda Accord 2012",
            price: "$30.09",
            img: "../img/accord.jpg"
        }, {
            model: "Toyota Camry 2009",
            price: "$24.09",
            img: "../img/camry.jpg"
        }, {
            model: "Mitsubishi Evolution X",
            price: "$36.09",
            img: "../img/evo.jpg"
        }
    ]
}


TYPE_TO_TITLE = {
    'flight_info': 'Flight Details',
    'places': 'Places to Visit',
    'rentals': 'Car Rentals',
}

cardStack = {}
// cardStack = {<user_name>: {"column": <column_elem>, "cards": [<cards>,]}}

jQuery.fn.center = function () {
    //this.css("position","absolute");
    var top = ( $(window).height() - this.height() ) / 2+$(window).scrollTop() + "px",
        left = ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px";
    this.animate({top: top, left: left});
    return this;
}

function addCard(data) {
    if (data['type'] == 'flight_info') {
        data['title'] = TYPE_TO_TITLE[data['type']];
        var card = buildFlightCard(data);
    }
    else if (data['type'] == 'places') {
        data['title'] = "Hollywood Beach";
        var card = buildPlaceCard(data);
    }
    else if (data['type'] == 'rentals') {
        data['title'] = TYPE_TO_TITLE[data['type']];
        data['cars'] = RENTAL_DATA['cars'];
        var card = buildRentalCard(data);
    }
	else if (data['type'] == 'restaurants-veggie') {
        
        var card = buildRestaurantCard1(data);
    }
	else if (data['type'] == 'restaurants-meat') {
        
        var card = buildRestaurantCard2(data);
    }
    else {
        var card = buildCardWithHeader(data);
    }

    var id = data['user_name'] + '-' + data['type'];

    if (!cardStack[data['user_name']]) {
        var username = data['user_name'];
        console.log("Creating column "+username+'-column');
        var column = document.createElement('div');
        column.setAttribute('class', 'card-column');
        column.setAttribute('id', username + '-column');
        var usernames = Object.keys(cardStack);
        if (usernames.length > 0) { // If there's already a column
          var i = 0;
          while (usernames[i] == username) i++;
          console.log(Object.keys(cardStack));
          console.log(cardStack);
          var old_user = Object.keys(cardStack)[i];
          cardStack[old_user]['column'].setAttribute('style', 'float:left');
          column.setAttribute('style', 'float:right');
        } else {
          column.setAttribute('style', 'margin-left:auto;margin-right:auto');
        }
        document.getElementById('card-container').appendChild(column);
        cardStack[username] = {};
        cardStack[username]['column'] = column;
        cardStack[username]['cards'] = [];
    }

    cardStack[data['user_name']]['column'].appendChild(card);
    cardStack[data['user_name']]['cards'].push(id);

    setTimeout(function () {
        console.log($('div#' + id + '.card'));
        $('div#' + id + '.card').removeClass('hidden');
    }, 0);

}

function removeCards(data) {
    console.log("Called");
    var username = data['user_name'];
    if (cardStack[username]['cards'].length != 0) {
        var id = cardStack[username]['cards'].pop();

        setTimeout(function () {
            $('div#' + id + '.card').addClass('hidden');
            removeCards(data);
        }, 200);
    }

    setTimeout(function (){
        var column = document.getElementById(data['user_name'] + '-column');
        document.getElementById('card-container').removeChild(column);
        var usernames = Object.keys(cardStack);
        if (usernames.length > 0) { // If there's already a column
          var i = 0;
          while (usernames[i] == username) i++;
          var old_user = Object.keys(cardStack)[i];
          cardStack[old_user]['column'].setAttribute('style', 'margin-left:auto;margin-right:auto');
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
    cardTitle.innerHTML = data['title']
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
    cardContent.setAttribute('style', "background-image: url('../img/miami.jpg');");
    card.appendChild(cardContent);

    var blackOverlay = document.createElement('div');
    blackOverlay.setAttribute('class', 'card-content-bg-overlay');
    cardContent.appendChild(blackOverlay);

    var contentContainer = document.createElement('div');
    contentContainer.style.paddingLeft = "10px";
    contentContainer.style.paddingTop = "5px";
    blackOverlay.appendChild(contentContainer);

    var flightInfo = document.createElement('p');
    flightInfo.setAttribute('class', 'info-header');
    flightInfo.innerHTML = "United Airlines flight <em>" + data['flight_number'] + "</em> to <em>" + data['destination'] + "</em>";
    contentContainer.appendChild(flightInfo);

    var flightDeparture = document.createElement('div');
    flightDeparture.setAttribute('class', 'departure');
    flightDeparture.innerHTML = "<p class='title'>Departure</p> <p class='info'>Gate 48 &nbsp;&nbsp;<em>" + data['departure_time'] + "</em></p>";

    var flightArrival = document.createElement('div');
    flightArrival.setAttribute('class', 'arrival');
    flightArrival.innerHTML = "<p class='title'>Arrival</p> <p class='info'>Gate 24 &nbsp;&nbsp;<em>" + data['arrival_time'] + "</em></p>";

    contentContainer.appendChild(flightDeparture);
    contentContainer.appendChild(flightArrival);

    return card
}

function buildPlaceCard(data) {
    var id = data['user_name'] + '-' + data['type'];
    var card = buildCardWithHeader(data);

    var cardContent = document.createElement('div');
    cardContent.setAttribute('class', 'card-content');
    cardContent.setAttribute('style', "background-image: url('../img/hollywood-beach.jpg');");
    card.appendChild(cardContent);

    var contentContainer = document.createElement('div');
    contentContainer.style.paddingLeft = "10px";
    contentContainer.style.paddingTop = "5px";
    cardContent.appendChild(contentContainer);

    card.getElementsByClassName('card-title')[0].innerHTML += " &mdash; 1.5 mi";

    return card;
}

function buildRestaurantCard1(data) {
	data['title'] = "Loving Hut";
    var id = data['user_name'] + '-' + data['type'];
    var card = buildCardWithHeader(data);

    var cardContent = document.createElement('div');
    cardContent.setAttribute('class', 'card-content');
    cardContent.setAttribute('style', "background-image: url('../img/veggie.jpg');");
    card.appendChild(cardContent);

    var contentContainer = document.createElement('div');
    contentContainer.style.paddingLeft = "10px";
    contentContainer.style.paddingTop = "5px";
    cardContent.appendChild(contentContainer);

    card.getElementsByClassName('card-title')[0].innerHTML += " &mdash; 4 stars";

    return card;
}

function buildRestaurantCard2(data) {
	data['title'] = "Sorabol Korean Restaurant";
    var id = data['user_name'] + '-' + data['type'];
    var card = buildCardWithHeader(data);

    var cardContent = document.createElement('div');
    cardContent.setAttribute('class', 'card-content');
    cardContent.setAttribute('style', "background-image: url('../img/bbq.jpg');");
    card.appendChild(cardContent);

    var contentContainer = document.createElement('div');
    contentContainer.style.paddingLeft = "10px";
    contentContainer.style.paddingTop = "5px";
    cardContent.appendChild(contentContainer);

    card.getElementsByClassName('card-title')[0].innerHTML += "&mdash; 3 stars";

    return card;
}

function buildRentalCard(data) {
    var card = buildCardWithHeader(data);

    var cardContent = document.createElement('div');
    cardContent.setAttribute('class', 'card-content');
    cardContent.style.marginTop = "10px";
    cardContent.style.height = "auto";
    card.appendChild(cardContent);


    for (var i=0; i < data['cars'].length; i++) {
        var carInfo = data['cars'][i];

        var carInfoContainer = document.createElement('div');
        carInfoContainer.setAttribute('class', 'car-option-container');
        carInfoContainer.innerHTML = "<img src='" + carInfo['img'] + "' width='100%' border='1'>"
        cardContent.appendChild(carInfoContainer);

        var carModel = document.createElement('p');
        carModel.setAttribute('class', 'car-model');
        carModel.innerHTML = carInfo['model'];
        carInfoContainer.appendChild(carModel);

        var carPrice = document.createElement('p');
        carPrice.setAttribute('class', 'car-price');
        carPrice.innerHTML = carInfo['price'];
        carInfoContainer.appendChild(carPrice);
    }
    return card;
}

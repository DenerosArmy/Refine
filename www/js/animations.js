DATA = {
    destination: "Miami, FL",
    display_name:  "Richie Z.",
    flight_gate: "G45",
    flight_number: "UA 456",
    flight_time: "2045",
    op: "+",
    profile_image_url: "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-frc1/372355_590037593_561933968_q.jpg",
    type: "flight_info",
    user_name: "richie_zeng",
}


TYPE_TO_TITLE = {
    'flight_info': 'Flight Details',
}


function addCard(data) {
    if (data['type'] == 'flight_info') {
        console.log(data);
        var card = buildFlightCard(DATA);
        document.getElementById('card-column').appendChild(card);

        setTimeout(function () {
            $('div.card').removeClass('hidden');
        }, 0);
    }
}

function buildFlightCard(data) {
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

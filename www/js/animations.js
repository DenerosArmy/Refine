DATA = {
    'type': 'flight_info',
    'user_name': 'richie'
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
    cardImage.setAttribute('style', "background-image:url('https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash4/c327.4.546.546/s160x160/215356_10151641982947594_144941694_n.jpg')");
    cardImageContainer.appendChild(cardImage);

    var cardTitle = document.createElement('p');
    cardTitle.setAttribute('class', 'card-title');
    cardTitle.innerHTML = "Flight Details";
    cardHeader.appendChild(cardTitle);

    var personName = document.createElement('p');
    personName.setAttribute('class', 'person-name');
    personName.innerHTML = "Richie Z.";
    cardHeader.appendChild(personName);

    return card;
}

const game_Id = JSON.parse(document.getElementById('game_id').textContent);

const gameSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/game/'
    + game_Id
    + '/'
);

gameSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(new Date($.now()) + " : " + e.data);

    if(data.message)
    {
        document.querySelector('#game-log').value += (data.message + '\n');
    }

    // load game log
    try {
        $('#game-log').text(data['log']);
        $('#game-log').scrollTop($('#game-log')[0].scrollHeight);
        // .scrollTop($('#game-log')[0].scrollHeight);​​​
    } catch (e) { }

    // game model
    try {
        const game_model = JSON.parse(data["model"]);
        if($("#players_lobby li").length != game_model.players.length)
        {
            $('#players_lobby').empty();
            for(let i = 0; i < game_model.players.length; i++) {
                $('#players_lobby').append('<li class="pl-3 list-inline-item" id="' + game_model.players[i] + '"><i class="fas fa-user-astronaut"></i> ' + game_model.players[i] + '</li>');
            }
        }
    } catch (e) { }

    // choose character modal
    try {
        let canPickCharacter = data["pick_character"];
        let availableCharacters = data["available_characters"];
        displayCharacterModal(canPickCharacter, availableCharacters);
    } catch (e) { }

    try {
        let player_select = data["update_character_section"];
        updateGamePieceSection(player_select);
    } catch (e) { }

    try {
        let cards = data["your_cards"];
        updateYourCardsSection(cards);
    } catch (e) { }

    try {
        let locations = data["update_location"];
        updatePlayersLocation(locations);
    } catch (e) { }

    try {
        let winner = data["winner"];
        displayWinnerAlert(winner);
    } catch (e) { }

    try {
        let gameStatus = data["game_status"];
        updateGameStatus(gameStatus);
    } catch (e) { }

    try {
        let incorrectNoti = data["incorrect_accused_notification"];
        dispalyIncorrectAccusedNotification(incorrectNoti);
    } catch (e) { }

    try {
        let enableBtns = data["enable_btn"];
        let availableMoves = data["available_moves"];
        let currentPosition = data["current_location"];
        enableButtons(enableBtns, availableMoves, currentPosition);
    } catch (e) { }

    try {
        let currentPosition = data["current_location"];
        updateSuggestionRoom(currentPosition);
    } catch (e) { }

    try {
        let cardsApproveDisapprove = data["cards_to_approve_disapprove"];
        let playersOwnerCards = data["player_owner_cards"];
        let suggestMsg = data["suggest_msg"];
        let suggesterName = data["suggester_name"];
        displayApprovalDisapproval(cardsApproveDisapprove, suggestMsg, playersOwnerCards, suggesterName);
    } catch (e) { }

    try {
        let approvedCards = data["choose_approved_cards"];
        let suggesterName = data["approved_cards_suggester"];
        displayApprovedCardsPickOne(approvedCards, suggesterName);
    } catch (e) { }

};

gameSocket.onclose = function(e) {
    console.error('game socket closed unexpectedly');
};

//////////// displayWinnerAlert
function displayWinnerAlert(winner){
    if(typeof winner === 'undefined') {
        return;
    }

    if(winner['bool']) {
        $('#winner').empty();
        $('#winner').append('\n' +
            '<div class="alert bg-success text-white" role="alert">\n' +
            '  Congratulations! You are a winner!\n' +
            '</div>');
    } else {
        $('#winner').append('\n' +
            '<div class="alert bg-danger text-white" role="alert">\n' +
            '  Unfortunately, ' + winner['user']  + ' accused correctly and won the game. \n' +
            '</div>');
    }

}

//////////// displayWinnerAlert
function dispalyIncorrectAccusedNotification(incorrectNoti){
    if(typeof incorrectNoti === 'undefined') {
        return;
    }

    if(incorrectNoti) {
        $('#incorrect-noti').empty();
        $('#incorrect-noti').append('<div class="alert bg-danger text-white" role="alert">\n' +
            'Unfortunately, your accusation is incorrect and no longer can make moves, suggestions, or accusation. You poor guy. \n' +
            '</div>');
    } else {
        $('#incorrect-noti').empty();
    }

}

//////////// Update Game Status
function updateGameStatus(status) {
    $('#game-status').empty();
    $('#game-status').append('<i class="fa fa-hourglass-start"></i> ' + status);
}

//////////// Display Character Model
function displayCharacterModal(canPickCharacter, availableCharacters) {
    if(canPickCharacter) {
        showAvailableCharacters(availableCharacters);

        // show modal
        $('#chooseCharacterModal').modal('show');
        $('#chooseCharacterModal').modal({backdrop: 'static', keyboard: false})
    } else if(canPickCharacter == false) {
        // do not show modal
        $('#chooseCharacterModal').modal('hide');
        $('#chooseCharacterModal').remove();
    } else if(typeof canPickCharacter === 'undefined' && typeof availableCharacters != 'undefined'){
        showAvailableCharacters(availableCharacters);
    }
}

function showAvailableCharacters(availableCharacters) {
    $('#charactersRadios').empty();
    for(var i = 0; i < availableCharacters.length; i++) {
        let imageName = availableCharacters[i].replace(" ", "");
        let radioHTML = '<div class="form-check pt-2">' +
            '<input class="form-check-input mt-3" type="radio" name="characterChosen" id="' + imageName + '" value="' + availableCharacters[i] + '"/>' +
            '<img class="rounded" src="/static/images/' + imageName + '.png" width="50" height="50"></img>' +
            '<label class="form-check-label pl-2" for="' + imageName + '"> ' + availableCharacters[i] + ' </label></div>';

        $('#charactersRadios').append(radioHTML);
    }
}

//////////// Update "Game Piece Character" section
function updateGamePieceSection(player_select) {
    if(typeof player_select === 'undefined') {
        return;
    }

    let imageName = player_select.replace(" ", "");
    $('#game_piece_character').empty();
    let liHTML = '<img class="rounded" src="/static/images/' + imageName + '.png" width="50" height="50"></img>' +
        '<label class="form-check-label pl-2" for="' + imageName + '">' + player_select + '</label></div>';
    $('#game_piece_character').append(liHTML);
}

//////////// Update "Your Cards" Section
function updateYourCardsSection(cards) {
    if(typeof cards === 'undefined') {
        return;
    }

    $('#your_cards').empty();
    $('#your_cards').append('<li class="list-group-item text-center">Your Cards</li>');
    for(var i = 0; i < cards.length; i++){
        let cardHTML = '<li id="player_card_person" class="list-group-item"><img class="rounded" src="/static/images/' + cards[i].replace(" ", "") + '.png" width="50" height="50"></img>' +
        '<label class="form-check-label pl-2"> ' + cards[i] + ' </label></div></li>';
        $('#your_cards').append(cardHTML);
    }
}

//////////// Update "Players Location" section
function updatePlayersLocation(locations) {
    if(typeof locations == 'undefined') {
        return;
    }

    $('#players_location').empty();
    $('#players_location').append('<li class="list-group-item text-center">Current Players Locations</li>');

    // player, location
    for (const [key, value] of Object.entries(locations)) {
        let liHTML = '<li class="list-group-item">' + key + ' @ ' + value + '</li>'
        $('#players_location').append(liHTML);
    }

}

//////////// Enable or Disable Buttons
function enableButtons(enableBtns, availableMoves, currentLocation) {
    if(typeof enableBtns === 'undefined' && typeof availableMoves === 'undefined' && typeof currentLocation === 'undefined'
           && typeof next_turn === 'undefined') {
        return;
    }
    for (const [key, value] of Object.entries(enableBtns)) {
        if(key === 'move') {
            if(value) {
                $('#game-show-moves-modal').removeClass("btn btn-secondary disabled").addClass("btn btn-primary text-white");

                // available_moves
                $('#availableMovesOptions').empty()
                for(let i = 0; i < availableMoves.length; i++){
                    $('#availableMovesOptions').append('<option value="' + availableMoves[i] + '">' + availableMoves[i] + '</option>');
                }

                $('#current_position').text(currentLocation);
            } else {
                $('#game-show-moves-modal').removeClass().addClass("btn btn-secondary disabled");
            }
        } else if(key === "accuse") {
            if(value) {
                $('#game-accuse-modal').removeClass("btn btn-secondary disabled").addClass("btn btn-primary text-white");
            } else {
                $('#game-accuse-modal').removeClass().addClass("btn btn-secondary disabled");
            }
        } else if(key === "suggest") {
            if(value) {
                $('#game-show-suggestion-modal').removeClass("btn btn-secondary disabled").addClass("btn btn-primary text-white");
            } else {
                $('#game-show-suggestion-modal').removeClass().addClass("btn btn-secondary disabled");
            }
        } else if(key === "end_turn") {
            if(value) {
                $('#game-end-turn-submit').removeClass("btn btn-secondary disabled").addClass("btn btn-success text-white");
            } else {
                $('#game-end-turn-submit').removeClass().addClass("btn btn-secondary disabled");
            }
        }
    }
}

//////////// Update Suggestion Room Location
function updateSuggestionRoom(currentLocation) {
    if(typeof currentLocation === 'undefined') {
        return;
    }

    $('#suggest_room').text(currentLocation);
}

//////////// Show Approver/Disapprover a Modal
function displayApprovalDisapproval(cardsApproveDisapprove, suggestMsg, playersOwnerCards, suggesterName) {
    if(typeof cardsApproveDisapprove === 'undefined' || suggestMsg === 'undefined' || playersOwnerCards === 'undefined'
        || suggesterName == 'undefined') {
        return;
    }

    $('#approveDisapproveModal').modal({backdrop: 'static', keyboard: false})
    $('#approveCheckboxes').empty();
    $('#suggestMsg').text(suggestMsg);
    $('#suggesterName').text(suggesterName);
    $('#playersOwnerCards').text(playersOwnerCards);
    for(let i = 0; i < cardsApproveDisapprove.length; i++) {
        let checkBoxHTML = '<div class="form-check">\n' +
            '<input name="approved_cards_checkbox" type="checkbox" class="form-check-input" value="' + cardsApproveDisapprove[i] + '">\n' +
            '<label class="form-check-label" for="exampleCheck1">' + cardsApproveDisapprove[i] + '</label>\n' +
            '</div>';
        $('#approveCheckboxes').append(checkBoxHTML);
    }
}

//////////// Allow a player to pick one card to show to suggester (ONLY IF IT'S TRUE)
function displayApprovedCardsPickOne(approvedCards, suggesterName) {
    if(typeof approvedCards === 'undefined' || suggesterName === 'undefined') {
        return;
    }

    $('suggesterNamePickOne').text(suggesterName);
    $('#chooseOneApprovedCardModal').modal({backdrop: 'static', keyboard: false})
    $('#approvedCardsRadios').empty();
    for(var i = 0; i < approvedCards.length; i++) {
        let radioHTML = '<div class="form-check pt-2">' +
            '<input class="form-check-input" type="radio" name="approvedCardsChosen" id="' + approvedCards + '" value="' + approvedCards[i] + '"/>' +
            '<label class="form-check-label pl-2" for="' + approvedCards + '"> ' + approvedCards[i] + ' </label></div>';

        $('#approvedCardsRadios').append(radioHTML);
    }
}

$('#game-move-selection-submit').click(function() {
    let nextMove = $("#availableMovesOptions").val();
    gameSocket.send(JSON.stringify({
        'type': 'select_move',
        'move_to': nextMove
    }));
    $('#showAvailableMoves').modal('hide');
});

$('#game-suggest-selection-submit').click(function() {
    let suspectSelect = $("#suggest_suspect").val();
    let roomSelect = $("#suggest_room").text();
    let weaponSelect = $("#suggest_weapon").val();
    gameSocket.send(JSON.stringify({
        'type': 'select_suggestion',
        'suggest': {'suspect': suspectSelect, 'room': roomSelect, 'weapon': weaponSelect}
    }));
    $('#makeSuggestionModal').modal('hide');
});

$('#game-accuse-submit').click(function() {
    let suspectSelect = $("#suspect_options").val();
    let roomSelect = $("#room_options").val();
    let weaponSelect = $("#weapon_options").val();
    gameSocket.send(JSON.stringify({
        'type': 'select_accuse',
        'accused': {'suspect': suspectSelect, 'room': roomSelect, 'weapon': weaponSelect}
    }));
    $('#accuseModal').modal('hide');
});

$('#game-end-turn-submit').click(function() {
    gameSocket.send(JSON.stringify({
        'type': 'end_turn',
    }));
});

$('#game-submit-approval').click(function() {
    var approvedCards = [];
    $("input:checkbox[name='approved_cards_checkbox']:checked").each(function() {
        approvedCards.push($(this).val());
    });

    let owner_cards = $('#playersOwnerCards').text();
    let suggester_name = $('#suggesterName').text();
    gameSocket.send(JSON.stringify({
        'type': 'approved_cards',
        'owner_cards': owner_cards,
        'approved_cards': approvedCards,
        'suggester': suggester_name
    }));

    $('#approveDisapproveModal').modal('hide');
});

$('#game-show-one-card-submit').click(function() {
    console.log("here?");
    let oneCard = $("input[name='approvedCardsChosen']:checked").val();
    let suggester_name = $('#suggesterNamePickOne').text();
    gameSocket.send(JSON.stringify({
        'type': 'show_one_card',
        'what_card_to_show': oneCard,
        'suggester': suggester_name
    }));
});


//////////// Let the server know that the user select a character
$('#game-player-chosen-submit').click(function() {
    let playerCharacter = $("input[name='characterChosen']:checked").val();
    gameSocket.send(JSON.stringify({
        'player_select': playerCharacter
    }));
});



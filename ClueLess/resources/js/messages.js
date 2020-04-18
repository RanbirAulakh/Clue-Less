
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

    if(data.message)
    {
        document.querySelector('#game-log').value += (data.message + '\n');
    }

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
    } catch (e) {
        console.log("Game_Model is missing")
    }
};

gameSocket.onclose = function(e) {
    console.error('game socket closed unexpectedly');
};

document.querySelector('#game-message-input').focus();
document.querySelector('#game-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#game-message-submit').click();
    }
};

document.querySelector('#game-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#game-message-input');
    const message = messageInputDom.value;
    gameSocket.send(JSON.stringify({
        'message': message
    }));
    messageInputDom.value = '';
};


$('#game-move-submit').click(function() {
    gameSocket.send(JSON.stringify({
        'type': 'move'
    }));
});

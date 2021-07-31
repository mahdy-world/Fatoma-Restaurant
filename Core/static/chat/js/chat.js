var text_box = '<div class="direct-chat-msg right">' +
        '<div class="direct-chat-infos clearfix">' +
        '<span class="direct-chat-name float-right">{sender}</span>'+
        '<span class="direct-chat-timestamp float-left">23 Jan 2:05 pm</span>'+
        '</div>'+
        '<div class="direct-chat-text">'+
        '{message}' +
        '</div>'
        '</div>';

function scrolltoend() {
    $('#board').stop().animate({
        scrollTop: $('#board')[0].scrollHeight
    }, 800);
}

function send(sender, receiver, message) {
    $.post('/chat/api/messages/', '{"sender": "'+ sender +'", "receiver": "'+ receiver +'","message": "'+ message +'" }', function (data) {
        console.log(data);
        var box = text_box.replace('{sender}', "You");
        box = box.replace('{message}', message);
        $('#board').append(box);
        scrolltoend();
    })
}

function receive() {
     $.get('/chat/api/messages/'+ sender_id + '/' + receiver_id + '/', function (data) {
    
        console.log(data);
        if (data.length !== 0)
        {
            for(var i=0;i<data.length;i++) {
                console.log(data[i]);
                var box = text_box.replace('{sender}', data[i].sender);
                box = box.replace('{message}', data[i].message);
                box = box.replace('right', 'left blue lighten-5');
                $('#board').append(box);
                scrolltoend();
            }
        }

       


    })
}

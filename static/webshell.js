var socket;
    $(document).ready(function(){
    socket = io.connect('http://' + location.hostname + ':' + location.port + '/shell');
    socket.on('connect', function() {
        socket.emit('joined');
    });

    //conect_msg
    socket.on('status', function(data) {
        $('#shell').val($('#shell').val() + '<' + data.msg + '>\n');
        $('#shell').scrollTop($('#shell')[0].scrollHeight);
    });

    socket.on('show', function(data) {
        $('#shell').val($('#shell').val() + data.msg + '\n'); //show
        $('#shell').scrollTop($('#shell')[0].scrollHeight); //roll to bottom
    });
    
    $('#command_box').keypress(function(e) {
        var presskey = e.keyCode || e.which;
        if (presskey == 13) { //enter -> 13
            command = $('#command_box').val();
            $('#command_box').val('');
            socket.emit('command_event', {msg: command});     
        }
    });

    $('#togglemodeButton').click(function() {
        socket.emit('togglemodeButton_pressed');
    });

    socket.on("refresh_mode",function(data){
        $('#modeLabel').text("現在模式: " + data.mode)
    })
});

var numberOfNodes = 0;

const sio = require('socket.io')(3000);
const redis = require('socket.io-redis');
sio.adapter(redis({ host: 'REDIS URL', port: 6379 }));

sio.on('connection', function (socketio) {
    sio.of('/').adapter.clients((err, clients) => {
        sio.emit("totalNodes",clients);
        console.log("New node connected " + clients.length);
    });

    socketio.on('storeChunk', function(data) {
        socketio.broadcast.emit('storageRequest', data);
        console.log("Request to store data - " + data);
    });

    socketio.on('searchChunk', function(data) {
        socketio.broadcast.emit('searchRequest', data);
        console.log("Request to search data " + data);
    });

    socketio.on('searchResponse', function(data) {
        socketio.to(data.id).emit('searchResponse', data);
        console.log("Response of search - " + data + " sending to " + data.id);
    });

    socketio.on('disconnect', function () {
        sio.of('/').adapter.clients((err, clients) => {
            sio.emit("totalNodes",clients);
            console.log("A node disconnected " + clients.length);
        });
   });
});


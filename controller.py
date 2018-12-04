import socketio
import eventlet
from flask import Flask, render_template
import redis
import socket

eventlet.monkey_patch()
url = 'redis://sdm-demo.11nrcb.ng.0001.use2.cache.amazonaws.com:6379/0'
sio = socketio.Server(client_manager=socketio.RedisManager(url))
app = Flask(__name__)

global counter
counter=0
@app.route('/')
def index():
    return render_template('abc.html')

@sio.on('checkCounter')
def totalnodes(data):
    print("total nodes received -- ", data)
    #sio.emit("total_nodes",counter)

@sio.on('connect')
def connect(sid, environ):
    global counter
    counter=counter+1
    demo=socket.gethostbyname(socket.gethostname())
    sio.emit("totalNodes",str(demo)+"#"+str(counter))
    print('connect '+str(counter)+demo, sid)

@sio.on('checkLatestCount')
def latestCount(sid, data):
    print("Request for latest count ")
    demo=socket.gethostbyname(socket.gethostname())
    sio.emit("latestCount",str(demo)+"#"+str(counter))
    print('connect '+str(counter)+demo, sid)

@sio.on('storeChunk')
def message(sid, data):
    print('storeChunk request received ', data)
    sio.emit('storageRequest', data)

@sio.on('searchChunk')
def message(sid, data):
    print('searchChunk ', data)
    sio.emit('searchRequest', data)

@sio.on('searchResponse')
def message(sid, data):
    print('searchChunk response ' + sid, data['id'])
    sio.emit('searchResponse', data, data['id'])

@sio.on('disconnect')
def disconnect(sid):
    global counter
    counter=counter-1
    demo=socket.gethostbyname(socket.gethostname())
    sio.emit("totalNodes",str(demo)+"#"+str(counter))
    print('disconnect '+str(counter), sid)

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 3000)), app)

from flask import Flask, request, Response, json
from lib import MusicCtl

app = Flask(__name__)
player = MusicCtl.MusicCtl().playerThread

play_queue = []


def make_response(error, msg=None, data=None):
    response = {
        'error': 0,
        'message': msg,
        'data': data
    }
    return Response(json.dumps(response), content_type='application/json')


@app.route('/')
def hello_world():
    return make_response(0, 'Music Console API is activated.')


@app.route('/control', methods=['POST'])
def control():
    req = request.form
    if req['action'] == 'play':
        if play_queue:
            player.play('./BIOTONIC - onoken.mp3')
        else:
            return make_response(-1, 'Empty playlist', play_queue)
    elif req['action'] == 'stop':
        player.stop()
    elif req['action'] == 'pause':
        player.pause()
    elif req['action'] == 'resume':
        player.resume()
    return make_response(0, 'ok', request.form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

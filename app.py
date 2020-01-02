import os
from flask import Flask, request, Response, json
from lib import MusicCtl

app = Flask(__name__)
player = MusicCtl.MusicCtl().playerThread
upload_path_prefix = 'uploads'

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


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    upload_path = os.path.join(os.path.dirname(__file__), upload_path_prefix, f.filename)
    f.save(upload_path)
    return make_response(0, 'Upload success', {
        "save_path": upload_path
    })


@app.route('/control', methods=['POST'])
def control():
    req = request.form
    if req['action'] == 'play':
        if int(req['isPlaylist']) == 1:
            print('- Fuck you! Playlist is not developed yet!! るさい!!! Even u wanna play [%s]' % req['mark'])
        else:
            player.play(os.path.join(os.path.dirname(__file__), upload_path_prefix, r'%s' % req['mark']))
            print('Single song [%s] will play for u.' % req['mark'])
    elif req['action'] == 'stop':
        player.stop()
    elif req['action'] == 'pause':
        player.pause()
    elif req['action'] == 'resume':
        player.resume()
    return make_response(0, 'ok', request.form)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

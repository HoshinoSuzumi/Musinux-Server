import os
import time
import math
import threading
from flask import Flask, request, Response, json
from flask_cors import CORS
from lib import MusicCtl

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
player = MusicCtl.MusicCtl().playerThread
upload_path_prefix = 'uploads'

play_queue = []
play_position = 0


def make_response(error, msg=None, data=None):
    error_list = {
        0: 'ok',
        10001: 'File is not exists',
        10002: 'File is already exists',
        20001: 'Unknown action',
    }
    if not data:
        data = {}
    data['timestamp'] = int(time.time())
    response = {
        'error': error,
        'message': msg or error_list.get(error),
        'data': data,
    }
    return Response(json.dumps(response), content_type='application/json', headers={"Server": "Moe Music Console"})


def getMusicList():
    return os.listdir(os.path.join(os.path.dirname(__file__), upload_path_prefix))


class QueueManagerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        pass


@app.route('/')
def root():
    return make_response(0, 'Music Console API is activated.')


@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('file')
    music_list = getMusicList()
    player.updatePlaylist()
    upload_result = {
        'total': len(files),
        'failed': 0,
        'exists_files': [],
        # 'musics': None
    }
    for file in files:
        if music_list.count(file.filename) > 0:
            upload_result['exists_files'].append(file.filename)
            upload_result['failed'] += 1
        else:
            upload_path = os.path.join(os.path.dirname(__file__), upload_path_prefix, file.filename)
            file.save(upload_path)
    # upload_result['musics'] = getMusicList()
    return make_response(0, 'Upload success', upload_result)


@app.route('/control', methods=['POST'])
def controller():
    req = request.form
    if req.get('action') == 'play':
        if req.get('isPlaylist', type=int) == 1:
            print('- Fuck you! Playlist is not developed yet!! るさい!!! Even u wanna play [%s]' % req['mark'])
        else:
            status = -1
            startIn = req.get('start', type=float, default=None)
            if startIn:
                status = player.play(os.path.join(os.path.dirname(__file__), upload_path_prefix, r'%s' % req.get('mark')),
                                     start=startIn)
            else:
                status = player.play(os.path.join(os.path.dirname(__file__), upload_path_prefix, r'%s' % req.get('mark')))
            print('Single song [%s] will play for u with status code [%s]' % (req.get('mark'), status))
            if status != 0:
                return make_response(status)
            else:
                return make_response(0, data={'meta': player.meta})
    elif req.get('action') == 'stop':
        player.stop()
        return make_response(0, 'ok')
    elif req.get('action') == 'pause':
        player.pause()
        return make_response(0, 'ok')
    elif req.get('action') == 'resume':
        player.resume()
        return make_response(0, 'ok')
    elif req.get('action') == 'vol':
        player.vol(req.get('mark', type=int))
        return make_response(0, 'ok', data={'vol': req.get('mark', type=int)})
    else:
        return make_response(20001)


@app.route('/fetch', methods=['POST'])
def fetcher():
    req = request.form
    if req['type'] == 'musics':
        music_list = getMusicList()
        return make_response(0, data={'musics': music_list})
    elif req['type'] == 'playlists':
        pass
    elif req['type'] == 'status':
        status = {
            'isPlaying': player.isPlaying,
            'meta': player.meta if player.isPlaying or player.paused else None,
            'progress': player.play_progress if player.isPlaying or player.paused else None,
            'vol': player.volume
        }
        return make_response(0, data=status)
    else:
        return make_response(20001)


if __name__ == '__main__':
    app.run(host='0.0.0.0')

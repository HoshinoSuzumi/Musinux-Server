# coding: utf-8

import os
import math
import json
import ffmpeg
import subprocess
import threading


class MusicCtl:
    def __init__(self):
        self.__playerQueue = []
        self.__playerPosition = 0
        self.playerThread = PlayerThread()
        self.playerThread.start()
        self.playerThread.play('../BIOTONIC - onoken.mp3')
        print('init musicCtl')

    def queue_join(self, meta):
        pass


class PlayerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.meta = None
        self.__playing = False
        self.__process = None
        self.__play_progress = 0.0
        self.__playing_path = ''
        os.popen('amixer set Master 100%')

    def run(self) -> None:
        while True:
            if self.__process:
                line = self.__process.stdout.readline()
                line = line.strip()
                if line:
                    progress = 0.0
                    try:
                        progress = float(line.split(' ')[0])
                    except ValueError:
                        pass
                    if progress:
                        if not math.isnan(progress):
                            self.__play_progress = progress
                print(self.__process.poll())

    def play(self, path, start=0.0):
        self.stop()
        path = os.path.abspath(path)
        self.meta = ffmpeg.probe(path)['format']
        # print(json.dumps(self.meta, indent=4))
        if not self.__playing and self.__process is None and os.path.isfile(path):
            self.__playing = True
            self.__playing_path = path
            self.__process = subprocess.Popen('ffplay "%s" -nodisp -autoexit -ss %s' % (path, start),
                                              shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                              stderr=subprocess.STDOUT, encoding='utf-8')
            return 0
        else:
            return -1

    def stop(self):
        self.__playing = False
        if self.__process:
            self.__process.kill()
            self.__process = None

    def pause(self):
        self.stop()

    def resume(self):
        if self.__playing_path is not '' and self.__playing_path:
            self.play(self.__playing_path, self.__play_progress)

    def progress_adj(self, progress):
        self.play(self.__playing_path, progress)


if __name__ == '__main__':
    mctl = MusicCtl()

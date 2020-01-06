# coding: utf-8

import os
import math
import ffmpeg
import subprocess
import threading


class MusicCtl:
    def __init__(self):
        self.playerThread = PlayerThread()
        self.playerThread.start()


class PlayerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.meta = None
        self.isPlaying = False
        self.play_progress = 0.0,
        self.volume = 100
        self.paused = False
        self.__process = None
        self.__playing_path = ''
        self.vol(100)

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
                            self.play_progress = progress
                if self.__process.poll() is not None:
                    self.stop()
                else:
                    self.isPlaying = True

    def vol(self, vol: int):
        self.volume = vol
        os.popen('amixer set Master %i%%' % vol)

    def play(self, path, start=0.0):
        self.paused = False
        self.stop()
        path = os.path.abspath(path)
        if os.path.isfile(path):
            self.meta = ffmpeg.probe(path)['format']
            print(self.meta)
            if not self.isPlaying:
                self.isPlaying = True
                self.__playing_path = path
                self.__process = subprocess.Popen('ffplay "%s" -nodisp -autoexit -ss %s' % (path, start),
                                                  shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                  stderr=subprocess.STDOUT, encoding='utf-8')
            return 0
        else:
            return 10001

    def stop(self):
        self.isPlaying = False
        if self.__process:
            self.__process.kill()

    def pause(self):
        self.paused = True
        self.stop()

    def resume(self):
        if self.__playing_path is not '' and self.__playing_path and self.paused:
            self.play(self.__playing_path, self.play_progress)
            self.paused = False

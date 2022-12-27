from configparser import ConfigParser
import subprocess
from os import listdir, path
from threading import Thread
import time

conf = ConfigParser()
conf.read("setup.conf")
SECRET = conf["SETTINGS"]["key"]

def getDuration(filename: str):
    # Возвращает длительность файла (неточно!)
    popen = subprocess.Popen(
        ("ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-i", filename),
        stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    output = str(output)
    output = output[output.find("duration") + len("duration") + 1: output.rfind("FORMAT") - 6]
    return (int(round(float(output) + 0.5)))

def streamFragment(afilename: str, vfilename: str):
    # Совмещает видео с музыкой и стримит на Ютуб
    add = '-movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"'.split() if vfilename[-4:] == ".gif" else ''
    vdur, adur = getDuration(f"video/{vfilename}"), getDuration(f"audio/{afilename}")
    args = ["ffmpeg", "-v", "quiet", "-stream_loop", f"{round(float(adur / vdur) + 0.5)}", "-re",
            "-i", f"video/{vfilename}", *add, "-ss", "0", "-t", f"{adur}", 
            "-i", f"audio/{afilename}", "-af", f"afade=t=in:st=0:d=3,afade=t=out:st={adur-3}:d=3",
            "-f", "flv", "rtmp://a.rtmp.youtube.com/live2/" + SECRET]
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

def readFiles(directory: str):
    # Возвращает список всех файлов в папке
    return [f for f in listdir(directory) if path.isfile(directory + f)]

def streamQueue(aqueue: list, vqueue: list):
    # Поочереди (асинхронно) стримит всю музыку
    aqueue.sort() # Это можно убрать, просто мне так удобнее плейлист проигрывать
    vqueue.sort() # И это тоже
    print("[OK] Started streaming the queue")
    sstream = Thread(target=streamFragment, args=(aqueue[0], vqueue[0],))
    sstream.start()
    print(f"[OK] Streaming element #1: {aqueue[0]}")
    delay = getDuration(f"audio/{aqueue[0]}") - 2.5 # Необходимо откалибровать
    for afile in range(1, len(aqueue)):
        print(f"[INFO] Delaying next element by {delay} seconds")
        time.sleep(delay)
        nstream = Thread(target=streamFragment, args=(aqueue[afile], vqueue[0],))
        nstream.start()
        print(f"[OK] Streaming element #{afile + 1}: {aqueue[afile]}")
        delay = getDuration(f"audio/{aqueue[afile]}") # Необходимо откалибровать
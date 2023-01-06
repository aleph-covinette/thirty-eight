import subprocess
from os import listdir, path, getcwd
from threading import Thread
import time

def getDuration(filename: str):
    # Вычисляет длительность файла
    popen = subprocess.Popen(
        ("ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-i", 'media/' + filename),
    stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    output = str(output)
    output = output[output.find("duration") + len("duration") + 1: output.rfind("FORMAT") - 6]
    return int(round(float(output) + 0.5))

def streamFragment(afilename: str, vfilename: str, secret: str):
    # Совмещает видео с музыкой и стримит на Ютуб
    add = '-movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"'.split() if vfilename[0][-4:] == ".gif" else ''
    vdur, adur = vfilename[1], afilename[1]
    args = ["ffmpeg", "-v", "-quiet","-stream_loop", f"{round(float(adur / vdur) + 0.5)}", "-re",
            "-i", f"media/{vfilename[0]}", *add, "-ss", "0", "-t", f"{adur}", 
            "-i", f"media/{afilename[0]}", "-af", f"afade=t=in:st=0:d=3,afade=t=out:st={adur-3}:d=3",
            "-f", "flv", "rtmp://a.rtmp.youtube.com/live2/" + secret]
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

def streamQueue(aqueue: list, vqueue: list, secret: str):
    # Поочереди (асинхронно) стримит всю музыку
    print("[OK] Started streaming the queue")
    sstream = Thread(target=streamFragment, args=(aqueue[0], vqueue[0], secret))
    sstream.start()
    print(f"[OK] Streaming element #1: {aqueue[0][0]}")
    delay = aqueue[0][1] - 2.5 # Необходимо откалибровать
    for afile in range(1, len(aqueue)):
        print(f"[INFO] Delaying next element by {delay} seconds")
        time.sleep(delay)
        nstream = Thread(target=streamFragment, args=(aqueue[afile], vqueue[0], secret,))
        nstream.start()
        print(f"[OK] Streaming element #{afile + 1}: {aqueue[afile][0]}")
        delay = aqueue[afile][1] # Необходимо откалибровать

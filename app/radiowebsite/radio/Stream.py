import subprocess
from os import listdir, path, getcwd, remove
from threading import Thread
import time

def getDuration(filename: str):
    # Вычисляет длительность файла
    popen = subprocess.Popen(
        ('ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-i', 'media/' + filename),
    stdout=subprocess.PIPE)
    popen.wait()
    output = popen.stdout.read()
    output = str(output)
    output = output[output.find('duration') + len('duration') + 1: output.rfind('FORMAT') - 6]
    return int(round(float(output) + 0.5))

def prepareVideo(filename: str):
    # Небольшие преобразования видео которые лучше выполнить заранее
    add = '-movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"'.split() if filename[0][-4:] == '.gif' else ''
    args = ['ffmpeg', '-v', 'quiet', '-i', f'media/{filename}', *add, '-codec:v', 'libx264', '-profile:v', 'high',
            '-preset', 'veryslow', '-b:v', '2500k', '-maxrate', '2500k', '-bufsize', '5000k', '-threads', '0', f'media/cached/{filename}']
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()


def streamFragment(afilename: (str, int), vfilename: (str, int), secret: str):
    # Совмещает видео с музыкой и стримит на Ютуб
    vdur, adur = vfilename[1], afilename[1]
    args = ['ffmpeg', '-v', 'quiet', '-stream_loop', f'{adur // vdur}', '-re',
            '-i', f'media/cached/{vfilename[0]}', '-i', f'media/{afilename[0]}', '-af', 
            f'afade=t=in:st=0:d=3,afade=t=out:st={vdur * (adur // vdur) - 3}:d=3', '-codec:v', 'libx264',
            '-ss', '0', '-t', f'{vdur * (adur // vdur)}',
            '-f', 'flv', 'rtmp://a.rtmp.youtube.com/live2/' + secret]
    popen = subprocess.Popen(args, stdout=subprocess.PIPE)
    popen.wait()

def streamQueue(aqueue: list, vqueue: list, secret: str):
    # Поочереди (асинхронно) стримит всю музыку
    print(f'[XI] Производится предварительное транскодирование, подождите...')
    for video in vqueue:
        try:
            remove(getcwd() + '/media/cached/' + video[0])
        except FileNotFoundError:
            pass
        prepareVideo(video[0])
    print(f'[XI] Стрим запущен успешно, ключ: {secret}')
    sstream = Thread(target=streamFragment, args=(aqueue[0], vqueue[0], secret))
    sstream.start()
    print(f'[XI] Номер проигрываемого трека: 1 ({aqueue[0][0]})')
    delay = vqueue[0][1] * (aqueue[0][1] // vqueue[0][1]) - 1
    for afile in range(1, len(aqueue)):
        time.sleep(delay)
        nstream = Thread(target=streamFragment, args=(aqueue[afile], vqueue[0], secret,))
        nstream.start()
        print(f"[XI] Номер проигрываемого трека: {afile + 1} ({aqueue[afile][0]})")
        delay = vqueue[0][1] * (aqueue[afile][1] // vqueue[0][1])
    nstream.join()
    for video in vqueue:
        remove(getcwd() + '/media/cached/' + video[0])
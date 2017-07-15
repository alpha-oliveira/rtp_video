from tkinter import *
from tkinter import ttk, filedialog
from bs4 import BeautifulSoup
import requests
import re


def fetch_url():
    url = _url.get()
    to_statusbar('Procurando...')
    try:
        page = requests.get(url)
    except requests.RequestException as rex:
        to_statusbar(str(rex))
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        html = str(soup.html)
        url_video = fetch_url_video(html)
        if url_video:
            to_statusbar('Descarregando...')
            fetch_video(url_video)
        else:
            to_statusbar('Não foi encontrado um vídeo na página..')


def fetch_url_video(html):
    base_url = 'https://streaming-ondemand.rtp.pt/'
    matches = re.search(r'fileKey: "(.*).mp4"', html, re.MULTILINE)
    if matches:
        return base_url + matches.group(1) + '.mp4'
    else:
        return None


def fetch_video(url):
    filename = filedialog.asksaveasfilename(
        initialfile='video.mp4',
        filetypes=[('MP4', '.mp4')])
    video_data = requests.get(url).content
    with open(filename, 'wb') as f:
                f.write(video_data)
    to_statusbar('Terminou o download')


def to_statusbar(msg):
    _status_msg.set(msg)


if __name__ == "__main__":
    _root = Tk()
    _root.title('RTP Video')

    # mainframe
    _mainframe = ttk.Frame(_root, padding='5 5 5 5')
    _mainframe.grid(row=0, column=0, sticky=(E, W, N, S))
    # url frame
    _url_frame = ttk.LabelFrame(
        _mainframe, text='URL', padding='5 5 5 5')
    _url_frame.grid(row=0, column=0, sticky=(E, W))
    _url_frame.columnconfigure(0, weight=1)
    _url_frame.rowconfigure(0, weight=1)
    _url = StringVar()
    _url.set('http://www.rtp...')
    _url_entry = ttk.Entry(
        _url_frame, width=40, textvariable=_url)
    _url_entry.grid(row=0, column=0, sticky=(E, W, S, N), padx=5)
    _fetch_btn = ttk.Button(
        _url_frame, text='Descarregue', command=fetch_url)
    _fetch_btn.grid(row=0, column=1, sticky=W, padx=5)

    # status frame
    _status_frame = ttk.Frame(
        _root, relief='sunken', padding='2 2 2 2')
    _status_frame.grid(row=1, column=0, sticky=(E, W, S))
    _status_msg = StringVar()
    _status_msg.set('Insira o URL da página da RTP')
    _status = ttk.Label(
        _status_frame, textvariable=_status_msg, anchor=W)
    _status.grid(row=0, column=0, sticky=(E, W))
    _root.mainloop()

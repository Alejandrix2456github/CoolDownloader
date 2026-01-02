import requests
import yt_dlp
import os

def download_file(url, dest_path, progress_callback=None):
    is_youtube = "youtube.com" in url or "youtu.be" in url
    
    if is_youtube:
        return _download_youtube(url, dest_path, progress_callback)
    else:
        return _download_standard(url, dest_path, progress_callback)

def _download_standard(url, dest_path, progress_callback):
    try:
        response = requests.get(url, stream=True)
        total = int(response.headers.get('content-length', 0))
        downloaded = 0
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback and total > 0:
                    progress_callback(downloaded / total)
        return True
    except: return False

def _download_youtube(url, dest_path, progress_callback):
    def hook(d):
        if d['status'] == 'downloading' and progress_callback:
            p = d.get('_percent_str', '0%').replace('%','')
            progress_callback(float(p)/100)

    ydl_opts = {
        'format': 'best',
        'outtmpl': dest_path,
        'progress_hooks': [hook],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except: return False

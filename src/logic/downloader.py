import yt_dlp
import requests
import os
from PySide6.QtCore import QObject, Signal, QThread


class MetadataWorker(QObject):
    finished = Signal(dict) 
    error = Signal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                self.finished.emit(info)
        except Exception as e:
            self.error.emit(str(e))


class DownloadWorker(QObject):
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)
    log = Signal(str)

    def __init__(self, url, format_id, output_dir):
        super().__init__()
        self.url = url
        self.format_id = format_id
        self.output_dir = output_dir
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True

    def run(self):
        def progress_hook(d):
            if self.is_cancelled:
                raise Exception("Download cancelled by user")
                
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                speed = d.get('speed', 0)
                if total > 0:
                    self.progress.emit(int(downloaded / total * 100))
                
                speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "N/A"
                self.log.emit(f"[download] {downloaded/1024/1024:.1f}MB / {total/1024/1024:.1f}MB @ {speed_str}")
            elif d['status'] == 'finished':
                self.progress.emit(100)
                self.log.emit(f"[download] Finished downloading, merging files...")
        
        ydl_opts = {
            'format': self.format_id,
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [progress_hook],
            'quiet': False,
            'no_warnings': False,
            'verbose': False,
        }
        try:
            self.log.emit(f"[yt-dlp] Starting download: {self.url}")
            self.log.emit(f"[yt-dlp] Format: {self.format_id}")
            self.log.emit(f"[yt-dlp] Output: {self.output_dir}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                filename = ydl.prepare_filename(info)
                self.log.emit(f"[yt-dlp] Saved: {filename}")
                self.finished.emit(filename)
        except Exception as e:
            if "cancelled by user" in str(e):
                self.log.emit("[info] Download cancelled.")
            else:
                self.log.emit(f"[ERROR] {str(e)}")
                self.error.emit(str(e))


def fetch_thumbnail(url, save_path):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return save_path
    except Exception:
        return None


def get_formats_list(info):
    formats = []
    
    formats.append({"id": "bestvideo+bestaudio/best", "label": "Best Quality (Video + Audio)"})
    formats.append({"id": "bestaudio/best", "label": "Best Audio Only"})
    
    seen_heights = set()
    for f in info.get('formats', []):
        height = f.get('height')
        vcodec = f.get('vcodec', 'none')
        acodec = f.get('acodec', 'none')
        
        if height and vcodec != 'none' and height not in seen_heights:
            ext = f.get('ext', 'mp4')
            format_id = f.get('format_id', '')
            formats.append({
                "id": f"bestvideo[height<={height}]+bestaudio/best[height<={height}]",
                "label": f"{height}p ({ext.upper()})"
            })
            seen_heights.add(height)
    
    video_formats = [f for f in formats[2:]]
    video_formats.sort(key=lambda x: int(x['label'].split('p')[0]) if x['label'][0].isdigit() else 0, reverse=True)
    
    return formats[:2] + video_formats[:5]

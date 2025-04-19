from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from PIL.ExifTags import TAGS
import os
import shutil
import datetime

class ImageHandler(FileSystemEventHandler):
    def __init__(self, target_dir):
        self.target_dir = target_dir
        
    def on_created(self, event):
        if not event.is_directory:
            self.process_image(event.src_path)

    def get_exif_date(self, path):
        try:
            img = Image.open(path)
            exif = img._getexif()
            if exif:
                for tag, value in exif.items():
                    if TAGS.get(tag) == 'DateTimeOriginal':
                        return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception:
            return None

    def process_image(self, src_path):
        date = self.get_exif_date(src_path) or datetime.datetime.now()
        dest_dir = os.path.join(self.target_dir, date.strftime("%Y/%m/%d"))
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(src_path, dest_dir)
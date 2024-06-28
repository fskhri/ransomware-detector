import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os

# Direktori yang akan dipantau
watched_dir = "/path/to/watched/directory"
backup_dir = "/path/to/backup/directory"

class RansomwareDetector(FileSystemEventHandler):
    def on_modified(self, event):
        # Logika deteksi modifikasi file
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            self.create_backup(event.src_path)

    def on_created(self, event):
        # Logika deteksi pembuatan file
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.create_backup(event.src_path)

    def on_deleted(self, event):
        # Logika deteksi penghapusan file
        if not event.is_directory:
            print(f"File deleted: {event.src_path}")
            self.create_backup(event.src_path)

    def create_backup(self, file_path):
        # Membuat cadangan file
        if os.path.exists(file_path):
            shutil.copy(file_path, backup_dir)
            print(f"Backup created for: {file_path}")

if __name__ == "__main__":
    event_handler = RansomwareDetector()
    observer = Observer()
    observer.schedule(event_handler, path=watched_dir, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

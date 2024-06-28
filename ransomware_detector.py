import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
import subprocess

# Direktori yang akan dipantau
watched_dir = "/path/to/watched/directory"
backup_dir = "/path/to/backup/directory"

class RansomwareDetector(FileSystemEventHandler):
    def __init__(self):
        self.suspicious_files = []

    def on_modified(self, event):
        if not event.is_directory:
            print(f"File modified: {event.src_path}")
            self.detect_ransomware(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            print(f"File created: {event.src_path}")
            self.detect_ransomware(event.src_path)

    def detect_ransomware(self, file_path):
        # Cek apakah file terenkripsi dengan metode yang mencurigakan
        if self.is_suspicious(file_path):
            self.suspicious_files.append(file_path)
            self.take_action(file_path)

    def is_suspicious(self, file_path):
        # Deteksi sederhana untuk file yang mungkin terenkripsi
        # Misalnya, deteksi perubahan ekstensi atau konten file yang tidak bisa dibaca
        return file_path.endswith('.encrypted')  # Sederhana, ubah sesuai kebutuhan

    def take_action(self, file_path):
        # Ambil tindakan jika ransomware terdeteksi
        print(f"Suspicious file detected: {file_path}")
        # Mengunci sistem file atau mengambil tindakan lain
        subprocess.call(['chmod', '000', watched_dir])
        print("Directory locked to prevent further damage")

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

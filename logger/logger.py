import os
import time
from datetime import datetime


class Logger:
    def __init__(self, log_dir='logs', log_file='latest.log', max_bytes=10 * 1024):
        self.log_dir = log_dir
        self.log_file = self.log_dir + "/" + log_file
        self.max_bytes = max_bytes
        os.makedirs(self.log_dir, exist_ok=True)

    def _get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _get_backup_filename(self):
        # until_20250807_17h_12m_11s.log
        log_timestamp_format = f"until_{datetime.now().strftime('%Y%m%d_%Hh_%Mm_%Ss')}"
        return os.path.join(self.log_dir, f"{log_timestamp_format}.log")

    def _rotate_if_needed(self):
        if os.path.exists(self.log_file) and os.path.getsize(self.log_file) >= self.max_bytes:
            backup_file = self._get_backup_filename()
            os.rename(self.log_file, backup_file)
            self._zip_if_needed()

    def _zip_if_needed(self):
        log_files = []
        for filename in os.listdir(self.log_dir):
            if filename.startswith('until') and filename.endswith('.log'):
                log_files.append(os.path.join(self.log_dir, filename))
        log_files.sort()

        if len(log_files) < 2:
            return

        for i in range(len(log_files) - 1):
            old_path = log_files[i]
            base, ext = os.path.splitext(old_path)
            new_path = base + '.zip'
            os.rename(old_path, new_path)

    def print(self, header, body):
        self._rotate_if_needed()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{self._get_timestamp()}] {header:<30} : {body}" + '\n')

import os
import time
from datetime import datetime


class Logger:
    def __init__(self, log_file='latest.log', log_dir='logs', max_bytes=10 * 1024):
        self.log_file = log_file
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        os.makedirs(self.log_dir, exist_ok=True)

    def _get_timestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def _get_backup_filename(self):
        # until_20250807_17h_12m_11s.log
        timestamp_format = datetime.now().strftime('%Y%m%d_%Hh_%Mm_%Ss')
        log_timestamp_format = f"until_{timestamp_format}"

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
        if len(log_files) > 1:
            for i in range(len(log_files) - 1):
                old_path = log_files[i]
                base, ext = os.path.splitext(old_path)
                new_path = base + '.zip'
                os.rename(old_path, new_path)

    def print(self, header, body):
        timestamp = self._get_timestamp()
        log_entry = f"[{timestamp}] {header:<30} : {body}"

        # 로그 파일 기록
        self._rotate_if_needed()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

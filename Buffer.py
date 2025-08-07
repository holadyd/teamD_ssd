import os
import shutil


class Buffer:

    def __init__(self):
        self._dir_path = "buffer"
        self._buffer = []
        os.makedirs(self._dir_path, exist_ok=True)

        files = os.listdir(self._dir_path)
        if len(files) != 5:
            self._make_empty_file()

    def _make_empty_file(self):
        os.makedirs(self._dir_path, exist_ok=True)
        for i in range(1,6):
            with open(os.path.join(self._dir_path, f"{i}_empty"), "w", encoding="utf-8") as f:
                pass

    def read_buffer(self):
        self._buffer = os.listdir(self._dir_path)
        self._buffer.sort()

    def write_buffer(self, command):
        self.read_buffer()

        # update

        buf_idx = self._find_empty()

        flush = []
        if buf_idx == 5:
            flush = self.flsuh_buffer()
            buf_idx = 0



        command = command.replace(" ", "_")
        self._buffer[buf_idx] = f"{buf_idx + 1}_{command}"

        self._erase_files()
        os.makedirs(self._dir_path, exist_ok=True)
        for file_name in self._buffer:
            with open(os.path.join(self._dir_path, file_name), "w", encoding="utf-8") as f:
                pass


        return flush

    def update_buffer(self):
        pass

    def flsuh_buffer(self):
        self.read_buffer()
        buffer = self._buffer
        self._reset_buffer()
        return buffer
    #
    # def __del__(self):
    #     if os.path.exists(self._dir_path):
    #         shutil.rmtree(self._dir_path)

    def _find_empty(self):
        for idx in range(len(self._buffer)):
            if "empty" in self._buffer[idx]:
                return idx
        return 5

    def _reset_buffer(self):
        self._erase_files()
        self._make_empty_file()
        self._buffer = []
        for idx in range(1,6):
            self._buffer.append(f"{idx}_empty")

    def _erase_files(self):
        if os.path.exists(self._dir_path):
            shutil.rmtree(self._dir_path)

    def fast_read(self, command):
        pass


import os
import shutil


class Buffer:

    def __init__(self):
        self._dir_path = "buffer"
        self._initial_data = "0x00000000"
        self._buffer = []
        os.makedirs(self._dir_path, exist_ok=True)

        files = os.listdir(self._dir_path)
        if len(files) != 5:
            self._make_empty_file()

    def _make_empty_file(self):
        os.makedirs(self._dir_path, exist_ok=True)
        for i in range(1, 6):
            with open(os.path.join(self._dir_path, f"{i}_empty"), "w", encoding="utf-8") as f:
                pass

    def read_buffer(self):
        self._buffer = os.listdir(self._dir_path)
        self._buffer.sort()

    def write_buffer(self, command) -> list[str]:
        self.read_buffer()

        self.update_buffer()
        self.read_buffer()

        buf_idx = self._find_empty()

        flush = []
        if buf_idx == 5:
            flush = self.flush_buffer()
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
        self.read_buffer()
        buf_list = [None] * 100
        self.update_buf_list(buf_list)

        merged_commands = []
        self.merge_commands(buf_list, merged_commands)
        merged_commands.sort()

        self.update_buffer_memory(merged_commands)

    def update_buffer_memory(self, merged_commands):
        self._erase_files()
        os.makedirs(self._dir_path, exist_ok=True)
        for cmd_idx in range(len(merged_commands)):
            with open(os.path.join(self._dir_path, f'{cmd_idx + 1}_{merged_commands[cmd_idx].replace(" ", "_")}'), "w",
                      encoding="utf-8") as f:
                pass
        files = len(os.listdir(self._dir_path))
        while files != 5:
            files += 1
            with open(os.path.join(self._dir_path, f"{files}_empty"), "w", encoding="utf-8") as f:
                pass

    def merge_commands(self, buf_list, merged_commands):
        same_next = -1
        for i in range(100):
            if buf_list[i] == None:
                if same_next == -1:
                    continue
                else:
                    merged_commands.append(f"E {i - same_next} {same_next}")
                    same_next = -1
            elif buf_list[i] != self._initial_data:
                if same_next == 10:
                    merged_commands.append(f"E {i - same_next} {same_next}")
                    same_next = -1
                elif 0 < same_next < 10:
                    same_next += 1
                elif same_next != -1:
                    same_next += 1
                merged_commands.append(f"W {i} {buf_list[i]}")
            elif buf_list[i] == self._initial_data:
                if same_next == -1:
                    same_next = 1
                elif same_next < 10:
                    same_next += 1
                elif same_next == 10:
                    merged_commands.append(f"E {i - same_next} {same_next}")
                    same_next = 1

    def update_buf_list(self, buf_list):
        for buf in self._buffer:
            if "empty" not in buf:
                cmd = buf.split("_")
                if cmd[1] == "W":
                    lba = int(cmd[2])
                    value = cmd[3]
                    buf_list[lba] = value
                elif cmd[1] == "E":
                    cur_lba = int(cmd[2])
                    range_siz = int(cmd[3])
                    for idx in range(abs(int(range_siz))):
                        buf_list[cur_lba] = self._initial_data
                        cur_lba += 1 if range_siz > 0 else -1

    def flush_buffer(self) -> list[str]:
        self.read_buffer()
        buffer = self._buffer
        self._reset_buffer()
        return buffer

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
        for idx in range(1, 6):
            self._buffer.append(f"{idx}_empty")

    def _erase_files(self):
        if os.path.exists(self._dir_path):
            shutil.rmtree(self._dir_path)

    def fast_read(self, lba) -> list[str] | None:
        self.read_buffer()

        buf_dict = dict()

        for buf in self._buffer:
            if "empty" not in buf:
                cmd = buf.split("_")
                if cmd[1] == "W":
                    cmd_lba = cmd[2]
                    cmd_value = cmd[3]
                    buf_dict[cmd_lba] = cmd_value
                elif cmd[1] == "E":
                    cur_lba = int(cmd[2])
                    range_siz = int(cmd[3])
                    for idx in range(abs(int(range_siz))):
                        buf_dict[str(cur_lba)] = self._initial_data
                        cur_lba += 1 if range_siz > 0 else -1

        try:
            return buf_dict[lba]
        except:
            return None

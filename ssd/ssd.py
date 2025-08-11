import argparse
import json
import os
from contextlib import contextmanager
from typing import Literal

from settings import ROOT_DIR
from ssd.ssd_command import *
from ssd_buffer.buffer import Buffer


class SSD:
    def __init__(self, buffer: Buffer = None):
        self.nand_file = f"{ROOT_DIR}\\ssd_nand.txt"
        self.output_file = f"{ROOT_DIR}\\ssd_output.txt"
        self.buffer: Buffer = buffer
        self._initiate_nand_output()

    def _initiate_nand_output(self):
        self.initial_data = "0x00000000"

        if not os.path.exists(self.nand_file):
            self._init_nand_file()

        if not os.path.exists(self.output_file):
            self._init_output_file()

    def _init_output_file(self):
        initial_data_dict = {}
        initial_data_dict["0"] = self.initial_data
        with open(self.output_file, "w") as f:
            json.dump(initial_data_dict, f, indent=2)

    def _init_nand_file(self):
        initial_data_dict = {}
        for i in range(100):
            key = str(i)

            initial_data_dict[key] = self.initial_data
        with open(self.nand_file, "w") as f:
            json.dump(initial_data_dict, f, indent=2)

    def process_cmd(self, cmd: SSDCommand):
        if not cmd.validate():
            self._write_value_to_ssd_output("ERROR")
            return

        if isinstance(cmd, ReadCommand):
            self.process_read_cmd(cmd)
            return

        if isinstance(cmd, FlushCommand):
            self.process_flush_cmd()
            return

        if isinstance(cmd, WriteCommand):
            cmd = self.process_write_cmd(cmd)
            if cmd is None:
                return

        if isinstance(cmd, EraseCommand):
            self.process_erase_cmd(cmd)

    def process_erase_cmd(self, cmd):
        cmd.lba = cmd.convert_number_to_decimal(cmd.lba)
        cmd.data_size = cmd.convert_number_to_decimal(cmd.data_size)
        cmd_list = self.buffer.write_buffer(cmd.make_string())
        self.excute_flushed_command_list(cmd_list)

    def process_write_cmd(self, cmd):
        cmd.value = cmd.convert_number_to_hex(cmd.value)
        cmd.lba = cmd.convert_number_to_decimal(cmd.lba)
        if int(cmd.value, 0) == 0:
            cmd = CommandFactory.create(["E", cmd.lba, "1"])
            cmd.validate()
            return cmd
        cmd_list = self.buffer.write_buffer(cmd.make_string())
        self.excute_flushed_command_list(cmd_list)
        return None

    def process_read_cmd(self, cmd):
        cmd.lba = cmd.convert_number_to_decimal(cmd.lba)
        read_cmd = self.buffer.fast_read(str(cmd.lba))
        if read_cmd is None:
            self.execute_cmd(cmd)
        else:
            self._write_value_to_ssd_output(read_cmd)
        return

    def excute_flushed_command_list(self, cmd_list):
        if cmd_list is None:
            return
        for each_cmd in cmd_list:
            if 'empty' in each_cmd:
                continue
            _, *args = each_cmd.split('_')
            flushed_cmd = CommandFactory.create(args)
            flushed_cmd.validate()
            self.execute_cmd(flushed_cmd)

    def execute_cmd(self, cmd: SSDCommand):
        if isinstance(cmd, WriteCommand):
            self.write(cmd.lba, cmd.value)
        elif isinstance(cmd, ReadCommand):
            self.read(cmd.lba)
        elif isinstance(cmd, EraseCommand):
            self.erase(cmd.lba, cmd.data_size)
        else:
            pass

    def read(self, lba):
        lba_int = int(lba)
        key = str(lba_int)

        with open(self.nand_file, "r") as f:
            nand_data = json.load(f)
        value = nand_data.get(key)

        self._write_value_to_ssd_output(value)

        return value

    def _write_value_to_ssd_output(self, value: str):
        with open(self.output_file, "w") as f:
            json.dump({"0": value}, f, indent=2)

    def process_flush_cmd(self):
        try:
            cmd_list = self.buffer.flush_buffer()

            self.excute_flushed_command_list(cmd_list)
        except Exception as e:
            raise e

    def write(self, lba, value):

        try:
            nand_data = None

            with self._open_file(self.nand_file, 'r') as f:
                nand_data = json.load(f)

            converted_value = self.convert_value_to_hex(value)

            with self._open_file(self.nand_file, 'w') as f:
                nand_data[str(lba)] = converted_value
                json.dump(nand_data, f, indent=2)
        except Exception as e:
            raise e

    def convert_value_to_hex(self, value):
        str_value = str(value)
        if not str_value.startswith('0x'):
            str_value = hex(int(str_value, 0))
        converted_value = str_value[:2] + f'0000000{str_value[2:]}'[-8:].upper()
        return converted_value

    def erase(self, lba, size):

        lba = int(lba)
        size = int(size)
        try:
            nand_data = None
            with self._open_file(self.nand_file, 'r') as f:
                nand_data = json.load(f)
            for i in range(lba, lba + size):
                nand_data[str(i)] = self.convert_value_to_hex(0)
            with self._open_file(self.nand_file, 'w') as f:
                json.dump(nand_data, f, indent=2)

        except Exception as e:
            raise e

    @contextmanager
    def _open_file(self, file_path, mode: Literal['r', 'w']):
        f = None
        try:
            f = open(file_path, mode)
            yield f
        finally:
            if f:
                f.close()

    def has_lba(self, command: SSDCommand) -> bool:
        return hasattr(command, 'lba')


def main():
    parser = argparse.ArgumentParser(description='SSD 스크립트 실행을 위한 매개변수')

    parser.add_argument('args', type=str, nargs='*', help='가변 매개변수')
    args_result = parser.parse_args()

    buffer = Buffer()
    ssd = SSD(buffer)
    command = CommandFactory.create(args_result.args)
    ssd.process_cmd(command)


if __name__ == '__main__':
    main()

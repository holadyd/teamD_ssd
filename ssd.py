import argparse
import json
import os
from contextlib import contextmanager
from typing import Literal

from Buffer import Buffer
from ssd_command import *


class SSD:
    def __init__(self, buffer: Buffer = None):
        self.nand_file = "ssd_nand.txt"
        self.output_file = "ssd_output.txt"
        self.buffer: Buffer = buffer

    def process_cmd(self, cmd: SSDCommand):
        if not cmd.validate():
            self._write_value_to_ssd_output("ERROR")
            return
        if isinstance(cmd, WriteCommand):
            if int(cmd.data) == 0:
                cmd = CommandFactory.create("E", cmd.lba, "1")

        if isinstance(cmd, ReadCommand): #Fast Read판단
            read_cmd = self.buffer.fast_read(cmd.make_string())
            if read_cmd is None:
                self.execute_cmd(cmd)
        else:
            cmd_list = self.buffer.write_buffer(cmd.make_string())
            if not cmd_list is None:
                for each_cmd in cmd_list:
                    _, command,lba,data = each_cmd.split('_')
                    flushed_cmd = CommandFactory.create(command,lba,data)
                    self.execute_cmd(flushed_cmd)

    def execute_cmd(self, cmd: SSDCommand):
        if isinstance(cmd, WriteCommand):
            self.write(cmd.lba, cmd.data)
        elif isinstance(cmd, ReadCommand):
            self.read(cmd.lba)
        elif isinstance(cmd, EraseCommand):
            self.erase(cmd.lba, cmd.data_size)
        else:
            pass

    def read(self, lba):
        lba_int = int(lba)
        key = str(lba_int)  # JSON은 문자열 키 사용
        # ssd_nand.txt 읽기
        with open(self.nand_file, "r") as f:
            nand_data = json.load(f)
        value = nand_data.get(key)

        # ssd_output.txt에 읽은 값 저장
        self._write_value_to_ssd_output(value)

        return value

    def _write_value_to_ssd_output(self, value: str):
        with open(self.output_file, "w") as f:
            json.dump({"0": value}, f, indent=2)

    def write(self, lba, value):
        # if not self._check_parameter_validation(lba, value):
        #     self._write_value_to_ssd_output("ERROR")
        #     return
        try:
            nand_data = None
            # 파일 핸들러를 사용해 'r' 모드로 파일 열기
            with self._open_file(self.nand_file, 'r') as f:
                nand_data = json.load(f)

            converted_value = self.convert_value_to_hex(value)

            # 파일 핸들러를 사용해 'w' 모드로 파일 열기
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

def main():
    # argparse.ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description='SSD 스크립트 실행을 위한 매개변수')

    # 매개변수 추가
    parser.add_argument('command', type=str, help='첫 번째 매개변수 CMD')
    parser.add_argument('lba', type=str, help='두 번째 매개변수 SSD LBA주소')
    parser.add_argument('value', type=str, nargs='?', help='세 번째 매개변수 SSD Write시 Value', default=None)
    args = parser.parse_args()

    buffer = Buffer()
    ssd = SSD(buffer)
    command = CommandFactory.create(args.command,args.lba,args.value)
    ssd.process_cmd(command)


if __name__ == '__main__':
    main()

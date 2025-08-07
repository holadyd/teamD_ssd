import argparse
import json
import os
from contextlib import contextmanager
from typing import Literal

from Buffer import Buffer
from ssd_command import *

class SSD:
    def __init__(self, buffer:Buffer=None):
        self.nand_file = "ssd_nand.txt"
        self.output_file = "ssd_output.txt"
        self.buffer:Buffer = buffer

    def process_cmd(self, cmd: SSDCommand):
        if not cmd.validate():
            self._write_value_to_ssd_output("ERROR")
            return
        cmd_list = self.buffer.write_buffer(cmd)
        if not cmd_list is None:
            for each_cmd in cmd_list:
                self.execute_cmd(each_cmd)

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
        is_valid = self._check_parameter_validation(lba=lba)
        if not is_valid:
            self._write_value_to_ssd_output("ERROR")
            return "ERROR"

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
        if not self._check_parameter_validation(lba, value):
            self._write_value_to_ssd_output("ERROR")
            return

        try:
            nand_data = None
            # 파일 핸들러를 사용해 'r' 모드로 파일 열기
            with self._open_file(self.nand_file, 'r') as f:
                nand_data = json.load(f)

            str_value = str(value)
            if not str_value.startswith('0x'):
                str_value = hex(int(str_value, 0))
            converted_value = str_value[:2] + f'0000000{str_value[2:]}'[-8:].upper()

            # 파일 핸들러를 사용해 'w' 모드로 파일 열기
            with self._open_file(self.nand_file, 'w') as f:
                nand_data[str(lba)] = converted_value
                json.dump(nand_data, f, indent=2)
        except Exception as e:
            raise e

    def erase(self, lba, size):
        ...

    @contextmanager
    def _open_file(self, file_path, mode: Literal['r', 'w']):
        f = None
        try:
            f = open(file_path, mode)
            yield f
        finally:
            if f:
                f.close()

    def _check_parameter_validation(self, lba, value=None) -> bool:
        # value  invalid Check
        if value is not None:
            try:
                int(value, 0)  # 0이면 0x면 16진수, 0o면 8진수, 아니면 10진수

            except ValueError:
                return False

            if not (0x0 <= int(value, 0) <= 0xFFFFFFFF):
                return False

        # lba invalid Check
        # 1. int 인지 체크
        try:
            int(lba)
        except (ValueError, TypeError):
            return False

        # 2. 0~ 99 인지 체크
        if 0 <= int(lba) <= 99:
            return True
        return False


def main():
    # argparse.ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description='SSD 스크립트 실행을 위한 매개변수')

    # 매개변수 추가
    parser.add_argument('command', type=str, help='첫 번째 매개변수 CMD')
    parser.add_argument('lba', type=str, help='두 번째 매개변수 SSD LBA주소')
    parser.add_argument('value', type=str, nargs='?', help='세 번째 매개변수 SSD Write시 Value', default=None)
    args = parser.parse_args()

    # print(f"첫 번째 매개변수 (명령어 : W): {args.command}")
    # print(f"두 번째 매개변수 (주소 : LBA): {args.lba}")
    # print(f"세 번째 매개변수 (값 : VALUE): {args.value}")

    # 'value'가 있는지 확인하고 처리
    # 인자 개수 조건 검사 (예: command + address + optional value)

    if args.command is None or args.lba is None:
        ssd = SSD()
        ssd._write_value_to_ssd_output("ERROR")
        raise Exception("필수 인자가 누락되었습니다.")

    if args.command == "R":
        ssd = SSD()
        if args.value is not None:
            ssd._write_value_to_ssd_output("ERROR")
            raise Exception("R 명령어에는 value 인자가 필요없습니다.")
        ssd.read(args.lba)
    elif args.command == "W":
        ssd = SSD()
        if args.value is None:
            ssd._write_value_to_ssd_output("ERROR")
            raise Exception("W 명령어에는 value 인자가 필요합니다.")
        ssd.write(lba=args.lba, value=args.value)
    elif args.command == 'E':
        ssd = SSD()
        if args.value is None:
            ssd._write_value_to_ssd_output("ERROR")
            raise Exception('E 명령어에는 value(size) 인자가 필요합니다.')
        ssd.erase(lba=args.lba, size=args.value)
    else:
        ssd = SSD()
        ssd._write_value_to_ssd_output("ERROR")
        raise Exception("CMD가 잘못 되었습니다.")


if __name__ == '__main__':
    main()

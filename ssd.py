import argparse
import json
import os
from contextlib import contextmanager
from typing import Literal


class SSD:
    def __init__(self):
        self.nand_file = "ssd_nand.txt"
        self.output_file = "ssd_output.txt"
        self.initial_data = "0x00000000"

        # init ssd_nand.txt file
        if not os.path.exists(self.nand_file):
            initial_data_dict = {}

            for i in range(100):
                key = str(i)  # json key는 string
                # 모든 lba value를 "0x00000000"로 초기화
                initial_data_dict[key] = self.initial_data  # 딕셔너리에 추가

            with open(self.nand_file, "w") as f:  # file에 작성
                json.dump(initial_data_dict, f, indent=2)

        # init ssd_output.txt file
        if not os.path.exists(self.output_file):
            initial_data_dict = {}
            initial_data_dict["0"] = self.initial_data  # 딕셔너리에 추가

            with open(self.output_file, "w") as f:  # file에 작성
                json.dump(initial_data_dict, f, indent=2)

    def read(self, lba):
        try:
            lba_int = int(lba)
        except ValueError:
            # LBA 값을 int화하지 못하는 경우 ssd_output.txt에 "ERROR" 저장
            self._write_value_to_ssd_output("ERROR")
            return "ERROR"

        if lba_int < 0 or lba_int > 99:
            # invalid LBA일 경우 ssd_output.txt에 "ERROR" 저장
            self._write_value_to_ssd_output("ERROR")
            return "ERROR"

        key = str(lba_int)  # JSON은 문자열 키 사용

        # ssd_nand.txt 읽기
        with open(self.nand_file, "r") as f:
            nand_data = json.load(f)

        value = nand_data.get(key, self.initial_data)

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

        nand_data = None
        # 파일 핸들러를 사용해 'r' 모드로 파일 열기
        with self._open_file(self.nand_file, 'r') as f:
            nand_data = json.load(f)

        # 파일 핸들러를 사용해 'w' 모드로 파일 열기
        with self._open_file(self.nand_file, 'w') as f:
            nand_data[str(lba)] = value
            json.dump(nand_data, f)

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

            if not str(value).startswith("0x"):
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


if __name__ == '__main__':
    # argparse.ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description='SSD 스크립트 실행을 위한 매개변수')

    # 매개변수 추가
    parser.add_argument('command', type=str, help='첫 번째 매개변수 (예: W)')
    parser.add_argument('address', type=int, help='두 번째 매개변수 (정수)')
    parser.add_argument('--value', type=str, nargs='?', help='세 번째 매개변수 (16진수 값)', default=None)

    args = parser.parse_args()

    print(f"첫 번째 매개변수 (명령어 : W): {args.command}")
    print(f"두 번째 매개변수 (주소 : LBA): {args.address}")

    # 'value'가 있는지 확인하고 처리
    if args.value:
        print(f"세 번째 매개변수 (값 : VALUE): {args.value}")
    else:
        pass

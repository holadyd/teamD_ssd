import argparse
import json
import os
from contextlib import contextmanager
from typing import Literal


class SSD:
    nand_file_path = 'ssd_nand.txt'

    def read(self, lba):
        with open(self.nand_file_path, 'r') as f:
            nand_data: dict = json.load(f)
            return nand_data.get(str(lba), 0)

    def _initialize_nand_if_not_exists(self):
        if not os.path.exists(self.nand_file_path):
            with self._open_file(self.nand_file_path, 'w') as f:
                init_values = {str(v): 0 for v in range(100)}
                json.dump(init_values, f)

    def write(self, lba, value):
        nand_data = None
        # 파일 핸들러를 사용해 'r' 모드로 파일 열기
        with self._open_file(self.nand_file_path, 'r') as f:
            nand_data = json.load(f)

        # 파일 핸들러를 사용해 'w' 모드로 파일 열기
        with self._open_file(self.nand_file_path, 'w') as f:
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

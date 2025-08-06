import argparse
import json
import os


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

            with open(self.nand_file, "w") as f:    # file에 작성
                json.dump(initial_data_dict, f, indent=2)


    def read(self, lba):
        pass

    def write(self, lba, value):
        pass


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

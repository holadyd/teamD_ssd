import argparse


class SSD:
    def read(self, lba):
        pass

    def write(self, lba, value):
        pass

    def _check_paramter_validation(self, lba, value=None) -> bool:
        return True


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

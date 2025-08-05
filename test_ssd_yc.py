import pytest
from pytest_mock import MockFixture
from ssd import SSD
import sys


@pytest.mark.parametrize("args", [
    ['W', '68', '0x51D0C3A9'],
    ['W', '9', '0xC6F89B2E'],
    ['W', '22', '0x03A4E5F6'],
    ['W', '77', '0xF9B1C2A3'],
    ['W', '41', '0x7D8E9A0B'],
    ['W', '50', '0x2B3C4D5E'],
    ['W', '88', '0xE1F2A3B4'],
    ['W', '1', '0x9C8D7E6F'],
    ['W', '95', '0x3F4A5B6C'],
    ['W', '3', '0xA1B2C3D4']
])
def test_write_basic_flow_with_value(args):
    '''
    2번째 매개변수는 0-99 값이 들어오는 경우 값을 기록 후 Read하고 비교한다.
    :param args: ['W',lba,value]
    :return: lba 주소에 value를 write 후 lab 주소의 값이 정상적으로 read 동작하는지 확인
    '''
    _, lba, value = args
    # ssd 클래스 생성
    ssd = SSD()
    ssd.write(lba, value)
    # 캡처된 출력에 예상 메시지가 포함되어 있는지 검증
    assert ssd.read(lba) == value


@pytest.mark.skip
def test_write_3nd_arg_is_valid(): ...


@pytest.mark.skip
def test_write_valid_does_not_append_output(): ...


@pytest.mark.skip
def test_write_read_ssd_nand_file(): ...


@pytest.mark.skip
def test_write_create_ssd_nand_file(): ...

import pytest
from pytest_mock import MockFixture
from ssd import SSD
import sys
from unittest import mock


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
def test_write_3nd_arg_is_valid(args):
    '''

    :param args: 'W','LBA','VALUE
    :return: 3번째 매개변수는 0x0000000 형태인 경우 read value 값을 정상 읽어온다.
    '''
    op, lba, value = args
    ssd = SSD()
    assert op == 'W'
    ssd.write(lba, value)
    assert ssd.read(lba) == value


@pytest.mark.parametrize("args", [
    ['W', '68', '0x51D0'],  # 숫자 8자리 x
    ['W', '9', '0xC6F89'],  # 숫자 8자리 x
    ['W', '22', '0x05F6'],  # 숫자 8자리 x
    ['W', '77', 'F9B1C2A3'],  # 0x없는 경우
    ['W', '41', '7D8E9A0B'],  # 0x없는 경우
    ['W', '50', '2B3C4D5E'],  # 0x없는 경우
])
def test_write_3nd_arg_is_invalid(args):
    '''

    :param args: 'W','LBA','VALUE
    :return: 3번째 매개변수는 0x0000000 형태 가 아닌 경우 read value로 'ERROR'반환
    '''
    op, lba, value = args
    ssd = SSD()
    assert op == 'W'
    ssd.write(lba, value)
    assert ssd.read(lba) == 'ERROR'


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
def test_write_valid_does_not_append_output(args):
    '''
    ssd.write 를 valid한 값으로 수행시 ssd_output.txt에 하나의 데이터만 저장됨을 유지해야 한다.
    :param args : 'W','LBA','VALUE
    :return: 개행이 포함되지 않은 값을 return (1개의 값만이 ssd_output.txt에 저장됨)
    '''
    op, lba, value = args
    ssd = SSD()
    ssd.write(lba, value)
    assert '\n' not in ssd.read(lba)


def test_write_read_ssd_nand_file(mocker: MockFixture):
    '''
    ssd_nand 파일 읽는 함수를 호출한다.
    :param mocker: Mocker
    :return: builtin open 했는지?
    '''
    mock_file = mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data="Mocked file content")
    )
    ssd = SSD()
    ssd.write(99, '0xFFFFFFFF')
    mock_file.assert_called_once_with('ssd_nand.txt', 'r')


def test_write_create_ssd_nand_file(mocker: MockFixture):
    '''
    ssd_nand 파일 읽는(쓰는모드) 함수를 호출한다.
    :param mocker: Mocker
    :return: builtin open(write모드) 했는지?
    '''
    mock_file = mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data="Mocked file content")
    )
    ssd = SSD()
    ssd.write(99, '0xFFFFFFFF')
    mock_file.assert_called_once_with('ssd_nand.txt', 'w')

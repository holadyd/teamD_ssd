import os
import pytest
from ssd import SSD
from pytest_mock import MockFixture, MockerFixture


# ssd_u1
def test_console_not_print(capsys):
    ssd = SSD()

    ssd.read(50)
    ssd.write(50, '0x12345678')

    captured = capsys.readouterr()
    assert captured.out == ""


# ssd_u2
def test_read_1_args():
    ssd = SSD()
    result = ssd.read(42)

    assert result.startswith("0x") and len(result) == 10


# ssd_u3
@pytest.mark.parametrize("args", [
    (),  # 인자 0개
    (1, 2),  # 인자 2개
    (1, 2, 3),  # 인자 3개
])
def test_read_not_1_args(args):
    ssd = SSD()
    with pytest.raises(ValueError):
        ssd.read(*args)


# ssd_u4
def test_output_file_exist():
    ssd = SSD()

    assert os.path.exists('ssd_output.txt'), 'ssd_output.txt 파일이 존재하지 않습니다.'


# ssd_u15
def test_nand_file_exit():
    ssd = SSD()

    assert os.path.exists('ssd_nand.txt'), 'ssd_nand.txt 파일이 존재하지 않습니다.'


# ssd_u5
def test_read_2nd_invalid_args():
    ## Arrange
    command_line1 = "R 100"
    command_line2 = "R -1"

    command_split1 = command_line1.split()
    command_split2 = command_line2.split()

    lba1 = command_split1[1]
    lba2 = command_split2[1]

    ssd = SSD()

    ## act
    ret1 = ssd.read(lba1)
    ret2 = ssd.read(lba2)

    ## assert
    assert ret1 == "ERROR"
    assert ret2 == "ERROR"


# ssd_u6
def test_read_when_not_written():
    ## Arrange
    command_line1 = "R 99"
    command_line2 = "R 33"

    command_split1 = command_line1.split()
    command_split2 = command_line2.split()

    lba1 = command_split1[1]
    lba2 = command_split2[1]

    ssd = SSD()

    ## act
    ret1 = ssd.read(lba1)
    ret2 = ssd.read(lba2)

    # assert
    assert ret1 == "0x00000000"
    assert ret2 == "0x00000000"


# ssd_u7
def test_read_value_store_only_one_data():
    ## arrange
    ssd = SSD()

    ## act
    ret1 = ssd.read(0)
    ret2 = ssd.read(99)

    list_ret1 = ret1.split("\n")
    list_ret2 = ret2.split("\n")

    ## assert
    assert len(list_ret1) == 1
    assert len(list_ret2) == 1


# ssd_u8
def test_write_3_args():
    ## Arrange
    command_line1 = "W 10 0x00000001 abc"
    command_line2 = "W 11 "

    command_split1 = command_line1.split()
    command_split2 = command_line2.split()

    ## act
    ret1 = len(command_split1)
    ret2 = len(command_split2)

    ## assert
    assert ret1 == 3
    assert ret2 == 3


# ssd_u9
def test_write_2nd_invalid_args():
    ## Arrange
    command_line1 = "W -1 0x00000001"
    command_line2 = "W 100 0x00000002"

    command_split1 = command_line1.split()
    command_split2 = command_line2.split()

    ssd = SSD()

    lba1 = command_split1[1]
    lba2 = command_split2[1]

    value1 = command_split1[2]
    value2 = command_split2[2]

    ## act & assert
    ssd.write(lba1, value1)
    ret1 = ssd.read(lba1)
    assert ret1 == "ERROR"

    ssd.write(lba2, value2)
    ret2 = ssd.read(lba2)
    assert ret2 == "ERROR"


# ssd_u10
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
    op, lba, value = args
    # ssd 클래스 생성
    assert op == 'W'
    ssd = SSD()
    ssd.write(lba, value)
    # 캡처된 출력에 예상 메시지가 포함되어 있는지 검증
    assert ssd.read(lba) == value


# ssd_u16
@pytest.mark.parametrize("args", [
    ['W', '144', '0x51D0C3A9'],
    ['W', '2535', '0xC6F89B2E'],
    ['W', '-11', '0x03A4E5F6'],
    ['W', '666', '0xF9B1C2A3'],
    ['W', '224', '0x7D8E9A0B'],
    ['W', '10591', '0x2B3C4D5E'],
    ['W', '-988', '0xE1F2A3B4'],
    ['W', '-551', '0x9C8D7E6F'],
    ['W', '-95', '0x3F4A5B6C'],
    ['W', '243', '0xA1B2C3D4']
])
def test_write_invalid_lba(args):
    '''
    2번째 매개변수(lab)는 0-99 외의 값이 들어오는 경우 값을 기록 후 ERROR 반환.
    :param args: ['W',lba,value]
    :return: invalid 한 lba 주소에 쓰기 동작할때 ERROR 를 return
    '''
    op, lba, value = args
    # ssd 클래스 생성
    assert op == 'W'
    ssd = SSD()
    ssd.write(lba, value)
    # 캡처된 출력에 예상 메시지가 포함되어 있는지 검증
    assert ssd.read(lba) == 'ERROR'


# ssd_u11
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


# ssd_u17
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


# ssd_u12
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


# ssd_u13
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


# ssd_u14
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


# ssd_u18
@pytest.mark.parametrize("lba", [-1, -100, -9999, 9999, 100])
def test_lba_invalid(lba):
    # arrange
    ssd = SSD()

    # act
    ret = ssd._check_paramter_validation(lba)

    # assert
    assert ret is False


# ssd_u19
@pytest.mark.parametrize("lba, value", [
    ("W", "0x0000000H"),
    ("W", "0xFFFFFZZZ"),
    ("W", "ABCD"),
    ("W", "000000000")
])
def test_value_invalid_when_write(lba, value, mocker: MockerFixture):
    # arrange
    # ssd = SSD()
    ssd = mocker.Mock(spec=SSD)
    ssd._check_paramter_validation.return_value = True

    # act
    ret = ssd._check_paramter_validation(lba, value)

    # assert
    assert ret is False


# ssd_u22
@pytest.mark.parametrize("lba", [i for i in range(100)])
def test_lba_valid(lba, mocker: MockerFixture):
    # arrange
    # ssd = SSD()
    ssd = mocker.Mock(spec=SSD)
    ssd._check_paramter_validation.return_value = False

    # act
    ret = ssd._check_paramter_validation(lba)

    # assert
    assert ret is True


# ssd_23
@pytest.mark.parametrize("lba, value", [
    ("W", "0x00000000"),
    ("W", "0xFFFFFFFF"),
    ("W", "0xAA")
])
def test_value_valid_when_write(lba, value, mocker: MockerFixture):
    # arrange
    # ssd = SSD()
    ssd = mocker.Mock(spec=SSD)
    ssd._check_paramter_validation.return_value = False

    # act
    ret = ssd._check_paramter_validation(lba, value)

    # assert
    assert ret is True

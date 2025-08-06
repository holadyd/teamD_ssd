import json
import os
from pathlib import Path
import pytest
from ssd import SSD
from pytest_mock import MockFixture, MockerFixture

# 이 fixture는 각 테스트 함수 실행 후 항상 자동 실행됨
@pytest.fixture(autouse=True)
def cleanup_files():
    # Test Setup

    yield  # 테스트 실행

    # Test Teardown
    for file in ["ssd_nand.txt", "ssd_output.txt"]:
        if os.path.exists(file):
            os.remove(file)

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
    ssd.read(0)

    with open("ssd_output.txt", "r") as f:
        data1 = json.load(f)

    ssd.read(99)

    with open("ssd_output.txt", "r") as f:
        data2 = json.load(f)

    ## assert: 각각의 결과는 {"0": value} 형식으로, 1개의 데이터만 있어야 함
    assert len(data1) == 1
    assert len(data2) == 1


# ssd_u8
# W 명령어시 매개변수를 3개 받아야한다.
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
def test_write_3_args(mocker: MockFixture, args):
    '''
    :param mocker: ssd mocker
    :param args: test cases(w lba value)
    :return: lba,value 2개의 arguments 롤 write 실행하는지 검증
    '''
    op, lba, value = args
    mocker.patch.object(SSD, 'write')
    ssd = SSD()
    ssd.write(lba, value)
    assert len(ssd.write.call_args.args) == 2





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
    import json
    initial_nand_data = {str(i): 0 for i in range(100)}
    mock_file_content = json.dumps(initial_nand_data)
    # mocker.mock_open을 사용하여 open 함수를 모킹하고, 읽을 데이터를 설정합니다.
    mock_open = mocker.mock_open(read_data=mock_file_content)
    mocker.patch('builtins.open', mock_open)
    check_para_validataion_method = mocker.patch('ssd.SSD._check_parameter_validation')
    check_para_validataion_method.return_value = True
    ssd = SSD()
    ssd.write(99, '0xFFFFFFFF')
    mock_file_handle = mock_open()
    mock_file_handle.read.assert_called_once()


# ssd_u14
def test_write_create_ssd_nand_file(mocker: MockFixture):
    '''
    ssd_nand 파일 읽는(쓰는모드) 함수를 호출한다.
    :param mocker: Mocker
    :return: builtin open(write모드) 했는지?
    '''
    import json
    initial_nand_data = {str(i): '0' for i in range(100)}
    mock_file_content = json.dumps(initial_nand_data)
    # mocker.mock_open을 사용하여 open 함수를 모킹하고, 읽을 데이터를 설정합니다.
    mock_open = mocker.mock_open(read_data=mock_file_content)
    mocker.patch('builtins.open', mock_open)
    check_para_validataion_method = mocker.patch('ssd.SSD._check_parameter_validation')
    check_para_validataion_method.return_value = True
    ssd = SSD()
    lba, value = 99, '0xFFFFFFFF'
    ssd.write(lba, value)
    mock_open.assert_any_call('ssd_nand.txt', 'w')


# ssd_u20
def test_init_ssd_nand_file():
    # arrange
    nand_path = Path("ssd_nand.txt")
    if nand_path.exists():
        nand_path.unlink()

    # act
    ssd = SSD()

    # assert: 파일이 생성되었는지 확인
    assert nand_path.exists(), "ssd_nand.txt 파일이 생성되지 않았습니다."

    # assert: JSON 내용 확인
    with open(nand_path, "r") as f:
        data = json.load(f)

    # assert: 100개의 LBA가 있는지 확인
    assert len(data) == 100, "LBA 수가 100개가 아닙니다."

    # assert: 각 LBA 값이 "0x00000000"으로 초기화되었는지 확인
    for i in range(100):
        key = str(i)
        assert data[key] == "0x00000000", f"LBA {key}의 초기값이 올바르지 않습니다."

    # 테스트 후 정리
    nand_path.unlink()

# ssd_u21
def test_init_ssd_output_file():
    # arrange
    nand_path = Path("ssd_output.txt")
    if nand_path.exists():
        nand_path.unlink()

    # act
    ssd = SSD()

    # assert: 파일이 생성되었는지 확인
    assert nand_path.exists(), "ssd_output.txt 파일이 생성되지 않았습니다."

    # assert: JSON 내용 확인
    with open(nand_path, "r") as f:
        data = json.load(f)

    # assert: 1개의 LBA가 있는지 확인
    assert len(data) == 1, "Output file의 data 수가 1개가 아닙니다."

    # assert: 값이 "0x00000000"으로 초기화되었는지 확인
    assert data["0"] == "0x00000000", f"Output file의 초기값이 올바르지 않습니다."

    # 테스트 후 정리
    nand_path.unlink()

# ssd_u24
def test_read_store_ERROR_when_invalid_LBA():
    ## arrange
    ssd = SSD()

    ## act
    ssd.read(101)

    with open("ssd_output.txt", "r") as f:
        data2 = json.load(f)

    # assert
    assert data2["0"] == "ERROR"

# ssd_u18
@pytest.mark.parametrize("lba", [-1, -100, -9999, 9999, 100])
def test_lba_invalid(lba):
    # arrange
    ssd = SSD()

    # act
    ret = ssd._check_parameter_validation(lba)

    # assert
    assert ret is False


# ssd_u19
@pytest.mark.parametrize("lba, value", [
    ("10", "0x0000000H"),
    ("11", "0xFFFFFZZZ"),
    ("55", "ABCD"),
    ("99", "000000000")
])
def test_value_invalid_when_write(lba, value, mocker: MockerFixture):
    # arrange
    ssd = SSD()
    #ssd = mocker.Mock(spec=SSD)
    #ssd._check_parameter_validation.return_value = True

    # act
    ret = ssd._check_parameter_validation(lba, value)

    # assert
    assert ret is False


# ssd_u22
@pytest.mark.parametrize("lba", [i for i in range(100)])
def test_lba_valid(lba, mocker: MockerFixture):
    # arrange
    ssd = SSD()
    #ssd = mocker.Mock(spec=SSD)
    #ssd._check_parameter_validation.return_value = False

    # act
    ret = ssd._check_parameter_validation(lba)

    # assert
    assert ret is True


# ssd_23
@pytest.mark.parametrize("lba, value", [
    ("0", "0x00000000"),
    ("99", "0xFFFFFFFF"),
    ("6", "0xAA"),
    ("18", "0xFF")
])
def test_value_valid_when_write(lba, value, mocker: MockerFixture):
    # arrange
    ssd = SSD()
    #ssd = mocker.Mock(spec=SSD)
    #ssd._check_parameter_validation.return_value = False

    # act
    ret = ssd._check_parameter_validation(lba, value)

    # assert
    assert ret is True

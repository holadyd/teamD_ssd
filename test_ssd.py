import os
import pytest
from ssd import SSD


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

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
def test_read_2_args():
    ssd = SSD()
    result = ssd.read(42)

    assert result.startswith("0x") and len(result) == 10

# ssd_u3
@pytest.mark.parametrize("args", [
    (), # 인자 1개
    (1,),   # 인자 2개
    (1, 2, 3),  # 인자 3개
])
def test_read_not_2_args(args):
    ssd = SSD()
    with pytest.raises(ValueError):
        ssd.read(*args)

# ssd_u4
def test_output_file_exist():
    ssd = SSD()

    assert os.path.exists('ssd_output.txt'), 'ssd_output.txt 파일이 존재하지 않습니다.'

# ssd_u5
def test_nand_file_exit():
    ssd = SSD()

    assert os.path.exists('ssd_nand.txt'), 'ssd_nand.txt 파일이 존재하지 않습니다.'

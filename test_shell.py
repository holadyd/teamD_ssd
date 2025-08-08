import os
from unittest.mock import patch

import pytest

from logger import Logger
from shell import Shell
import sys
from io import StringIO
import re
import time
from buffer import Buffer


def input_command(shell, command):
    shell.read_command(command)
    if shell.valid_check():
        shell.run_command()


def test_shell_exit(capsys):
    buf = Buffer()
    buf._reset_buffer()
    sys.stdin = StringIO("exit\n")

    shell = Shell()
    shell.run_shell()

    captured = capsys.readouterr()

    assert captured.out == "Shell>Shell Exited Successfully.\n"


def test_run_command_write():
    buf = Buffer()
    buf._reset_buffer()
    with patch.object(Shell, 'run_command', return_value="[Write] Done") as mock_method:
        shell = Shell()
        result = shell.run_command("write 3 0x1289CDEF")

        assert result == "[Write] Done"

        mock_method.assert_called_once_with("write 3 0x1289CDEF")


def test_run_command_read():
    buf = Buffer()
    buf._reset_buffer()
    with patch.object(Shell, 'run_command', return_value="[Read] LBA : 0x00000000") as mock_method:
        shell = Shell()
        result = shell.run_command("read 30")

        assert result == "[Read] LBA : 0x00000000"

        mock_method.assert_called_once_with("read 30")


def test_shell_help(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("help")
    shell.run_command()

    captured = capsys.readouterr()
    expected = ('***SSD Test Shell Help***\n'
                '      write         지정한 LBA에 Data를 기록한다.\n'
                '        Usage) write [LBA] [Data]\n'
                '      fullwrite     모든 LBA에 Data를 기록한다.\n'
                '        Usage) fullwrite [Data]\n'
                '      read          지정한 LBA의 Data를 출력한다.\n'
                '        Usage) read [LBA]\n'
                '      fullread      모든 LBA에 대해 Data를 출력한다.\n'
                '        Usage) fullread\n'
                '      exit          Test Shell을 종료한다.\n'
                '      help          도움말을 출력한다.\n'
                '\n'
                '    Made by Digital Ninjas\n'
                '    김현용, 김준휘, 모유찬, 민재원, 이성규, 이재윤\n')

    assert captured.out == expected


@pytest.mark.skip
def test_shell_fullwrite(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("fullwrite 0xAAAABBBB")
    shell.run_command()
    out, err = capsys.readouterr()
    write_count = out.count("[Write] Done\n")
    assert write_count == 100


@pytest.mark.skip
def test_shell_fullread(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("fullread")
    shell.run_command()
    out, err = capsys.readouterr()

    # 정규표현식: [Read] LBA XX : 0xAAAAAAAA
    pattern = r"\[Read\] LBA \d{1,2} : 0x[0-9A-Fa-f]{8}"
    matches = re.findall(pattern, out)
    assert len(matches) == 100


def test_shell_input_validation_format_write_fail(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("write abc abc\n")
    if shell.valid_check():
        shell.run_command()
    out, err = capsys.readouterr()
    assert "Error" in out


def test_shell_input_validation_format_read_fail(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("read gbc\n")
    if shell.valid_check():
        shell.run_command()
    out, err = capsys.readouterr()

    assert "Error" in out


def test_shell_input_validation_format_fullwrite_fail(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("fullwrite abc\n")
    if shell.valid_check():
        shell.run_command()
    out, err = capsys.readouterr()

    assert "Error" in out


def test_shell_input_validation_lba_range_fail(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("read 300")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert captured.out == "[Error] INVALID_DATA\n"


def test_shell_input_validation_data_range_fail(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("write 99 0x123456789")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert "Error" in captured.out


def test_shell_input_validation_invalid_command(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("reee 30")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert "Error" in captured.out


@pytest.mark.skip
def test_script_2_write_read_aging(capsys, mocker):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_compare = mocker.Mock()
    shell.read_compare.side_effect = func
    shell.read_command("2_")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert captured.out == "PASS\n" * 30


def func(list):
    print("PASS")


def test_read_compare_pass(mocker, capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()

    mocker.patch.object(shell, 'ssd_read', side_effect=[100, 200])

    compare_list = [(1, 100), (2, 200)]
    shell.read_compare(compare_list)

    captured = capsys.readouterr()
    assert "PASS" in captured.out


def test_read_compare_fail(mocker, capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()

    mocker.patch.object(shell, 'ssd_read', side_effect=[101, 201])

    compare_list = [(1, 100), (2, 200)]
    shell.read_compare(compare_list)

    captured = capsys.readouterr()
    assert "FAIL" in captured.out


@pytest.mark.skip
def test_script_1_fullwrite_read_compare(capsys, mocker):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_compare = mocker.Mock()
    shell.read_compare.side_effect = func
    shell.read_command("1_")
    if shell.valid_check():
        shell.run_command()
    captured = capsys.readouterr()
    assert captured.out == "PASS\n" * 10

    shell.read_compare.side_effect = func
    shell.read_command("1_FullWriteAndReadCompare")
    if shell.valid_check():
        shell.run_command()
    captured = capsys.readouterr()
    assert captured.out == "PASS\n" * 10


@pytest.mark.skip
def test_script_3_write_read_aging(capsys, mocker):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_compare = mocker.Mock()
    shell.read_compare.side_effect = func
    shell.read_command("3_")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert captured.out == "PASS\n" * 200


def test_write_decimal_test(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("write 3 3")
    if shell.valid_check():
        shell.run_command()
    shell.read_command("read 3")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert captured.out == "[Write] Done\n[Read] LBA 3 : 0x00000003\n"


def test_write_hex_test(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("write 3 0x3")
    if shell.valid_check():
        shell.run_command()
    shell.read_command("read 3")
    if shell.valid_check():
        shell.run_command()

    captured = capsys.readouterr()

    assert captured.out == "[Write] Done\n[Read] LBA 3 : 0x00000003\n"


def test_ssd_read_write_in_shell_1():
    buf = Buffer()
    buf._reset_buffer()
    sh = Shell()
    sh.ssd_write("30", "0xAAAAAAAA")
    ret = sh.ssd_read("30", for_script=True)

    assert ret == "0xAAAAAAAA"


def test_ssd_read_write_in_shell_2():
    buf = Buffer()
    buf._reset_buffer()
    sh = Shell()
    value = "0x12345678"
    sh.ssd_write("30", value)
    ret = sh.ssd_read("30", for_script=True)

    assert ret == value


def test_runner_mode(capsys):
    buf = Buffer()
    buf._reset_buffer()
    # os.system(f"shell shell_scripts.txt")
    sh = Shell()
    sh._is_runner_mode = True

    sh.script_parser("shell_scripts.txt")

    expected = ('1_FullWriteAndReadCompare\t___\tRun...Pass\n'
                '1_FullWriteAndReadCompare\t___\tRun...Pass\n')
    captured = capsys.readouterr()
    assert captured.out == expected

def test_erase(capsys):
    buf = Buffer()
    buf._reset_buffer()
    shell = Shell()
    shell.read_command("write 3 0x3")
    if shell.valid_check():
        shell.run_command()
    shell.read_command("erase 3 1")
    if shell.valid_check():
        shell.run_command()
    shell.read_command("read 3")
    if shell.valid_check():
        shell.run_command()


    captured = capsys.readouterr()

    assert captured.out == "[Write] Done\n[Erase] Done\n[Read] LBA 3 : 0x00000000\n"

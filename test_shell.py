from unittest.mock import patch

from shell import Shell
import sys
from io import StringIO
import re

def test_shell_basic(capsys):
    sys.stdin = StringIO("exit\n")

    shell = Shell()
    shell.run_shell()

    captured = capsys.readouterr()


    assert captured.out == "Shell>Shell Exited Successfully.\n"


def test_run_command_write():
    with patch.object(Shell, 'run_command', return_value="[Write] Done") as mock_method:
        shell = Shell()
        result = shell.run_command("write 3 0x1289CDEF")

        assert result == "[Write] Done"

        mock_method.assert_called_once_with("write 3 0x1289CDEF")

def test_run_command_read():
    with patch.object(Shell, 'run_command', return_value="[Read] LBA : 0x00000000") as mock_method:
        shell = Shell()
        result = shell.run_command("read 30")

        assert result == "[Read] LBA : 0x00000000"

        mock_method.assert_called_once_with("read 30")
#
#
# def test_shell_write(capsys):
#     sys.stdin = StringIO("W 20 0x1289CDEF\nexit\n")
#
#     shell = Shell()
#     shell.run_shell()
#
#     captured = capsys.readouterr()
#
#     # captured = capsys.readouterr()
#
#     assert captured.out == "Shell> [Write] Done Shell Exited Successfully.\n"
#
#
# def test_shell_read(capsys):
#     sys.stdin = StringIO("R 20\nexit\n")
#
#     shell = Shell()
#     shell.run_shell()
#
#     captured = capsys.readouterr()
#
#     # captured = capsys.readouterr()
#
#     assert captured.out == "Shell> [Write] Done Shell Exited Successfully.\n"


def test_shell_fullwrite(capsys):
    shell = Shell()
    shell.run_command("fullwrite 0xAAAABBBB\n")()
    out, err = capsys.readouterr()
    write_count = out.count("[Write] Done\n")
    assert write_count == 100


def test_shell_fullread(capsys):
    shell = Shell()
    shell.run_command("fullread\n")
    out, err = capsys.readouterr()

    # 정규표현식: [Read] LBA XX : 0xAAAAAAAA
    pattern = r"\[Read\] LBA \d{1,2} : 0x[0-9A-Fa-f]{8}"
    matches = re.findall(pattern, out)
    assert len(matches) == 100

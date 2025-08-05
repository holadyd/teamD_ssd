from unittest.mock import patch

from shell import Shell
import sys
from io import StringIO
import re


def test_shell_exit(capsys):
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


def test_shell_help(capsys):
    shell = Shell()
    shell.run_command("help")

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

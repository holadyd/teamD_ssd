from shell import Shell
import sys
from io import StringIO
import re

def test_shell_exit(capsys):
    sys.stdin = StringIO("exit\n")

    shell = Shell()
    shell.run_shell()

    captured = capsys.readouterr()


    # captured = capsys.readouterr()

    assert captured.out == "Shell>Shell Exited Successfully.\n"


def test_shell_fullwrite(capsys):
    shell = Shell()
    shell.run_command("fullwrite 0xAAAABBBB\n")
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

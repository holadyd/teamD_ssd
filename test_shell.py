from shell import Shell
import sys
from io import StringIO


def test_shell_exit(capsys):
    sys.stdin = StringIO("exit\n")

    shell = Shell()
    shell.run_shell()

    captured = capsys.readouterr()

    assert captured.out == "Shell>Shell Exited Successfully.\n"

def test_shell_help(capsys):
    shell = Shell()
    shell.run_command("help")

    captured = capsys.readouterr()

    assert captured.out == "Shell>Shell Exited Successfully.\n"
from shell import Shell
import sys
from io import StringIO

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
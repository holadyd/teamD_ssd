import os
import pytest
from ssd import SSD

def test_console_not_print(capsys):
    ssd = SSD()

    ssd.read(50)
    ssd.write(50, '0x12345678')

    captured = capsys.readouterr()
    assert captured.out == ""


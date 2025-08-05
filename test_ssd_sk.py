import pytest
from pytest_mock import MockerFixture

from ssd import SSD


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

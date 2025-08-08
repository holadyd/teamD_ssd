import os
import pytest
from ssd_buffer.buffer import Buffer

from settings import ROOT_DIR

@pytest.fixture
def buf():
    buf = Buffer()
    buf.flush_buffer()

    return buf

def test_update_buffer_1(buf):
    # Scenario1
    buf.write_buffer("W 20 0xABCDEFFF")
    buf.write_buffer("E 10 4")
    buf.write_buffer("E 12 3")  # 위의 3개를 합치면 W 20 ~ + E 10 5가 되어야 함

    buf.update_buffer()
    buf.read_buffer()
    assert buf._buffer == ['1_E_10_5', '2_W_20_0xABCDEFFF', '3_empty', '4_empty', '5_empty']


def test_update_buffer_2(buf):
    buf._reset_buffer()
    buf.write_buffer("E 30 10")
    buf.write_buffer("W 40 0xAAAAAAAA")
    buf.write_buffer("E 41 4")
    buf.write_buffer("W 45 0xBBBBBBBB")
    buf.write_buffer("E 46 5")

    buf.update_buffer()
    buf.read_buffer()

    assert buf._buffer == ['1_E_30_10', '2_E_41_10', '3_W_40_0xAAAAAAAA', '4_W_45_0xBBBBBBBB', '5_empty']


def test_update_buffer_3(buf):
    buf._reset_buffer()
    buf.write_buffer("E 31 6")
    buf.write_buffer("W 37 0xAAAAAAAA")
    buf.write_buffer("E 38 3")
    buf.write_buffer("E 41 10")
    buf.write_buffer("W 51 0xBBBBBBBB")

    buf.update_buffer()
    buf.read_buffer()

    assert buf._buffer == ['1_E_31_10', '2_E_41_10', '3_W_37_0xAAAAAAAA', '4_W_51_0xBBBBBBBB', '5_empty']


def test_update_buffer_4(buf):
    buf._reset_buffer()
    buf.write_buffer("E 31 6")
    buf.write_buffer("W 37 0xAAAAAAAA")
    buf.write_buffer("E 38 3")
    buf.write_buffer("W 41 0xBBBBBBBB")
    buf.write_buffer("E 42 10")

    buf.update_buffer()
    buf.read_buffer()

    assert buf._buffer == ['1_E_31_10', '2_E_42_10', '3_W_37_0xAAAAAAAA', '4_W_41_0xBBBBBBBB', '5_empty']


def test_update_buffer_5(buf):
    buf._reset_buffer()
    buf.write_buffer("W 31 0xAAAAAAAA")
    buf.write_buffer("W 32 0xBBBBBBBB")
    buf.write_buffer("W 33 0xCCCCCCCC")
    buf.write_buffer("W 34 0xDDDDDDDD")
    buf.write_buffer("W 36 0xEEEEEEEE")

    buf.write_buffer("E 34 2")

    buf.update_buffer()
    buf.read_buffer()

    assert buf._buffer == ['1_E_34_2', '2_empty', '3_empty', '4_empty', '5_empty']


def test_update_buffer_6(buf):
    # Scenario1
    buf.write_buffer("E 10 4")
    buf.write_buffer("W 13 0xABCDEFFF")
    buf.write_buffer("E 12 3")  # 위의 3개를 합치면 W 20 ~ + E 10 5가 되어야 함

    buf.update_buffer()
    buf.read_buffer()
    assert buf._buffer == ['1_E_10_5', '2_empty', '3_empty', '4_empty', '5_empty']


# buffer 생성시  buffer 폴더가 없다면 buffer 폴더 생성 + 파일 초기화 ( {index}_empty )
def test_init_buffer_dir_and_files(buf):
    buf_dir = f"{ROOT_DIR}\\buffer"

    assert os.path.exists(buf_dir) and os.path.isdir(buf_dir)

    for i in range(1, 6):
        file_path = os.path.join(buf_dir, f"{i}_empty")
        assert os.path.exists(file_path) and os.path.isfile(file_path)


# buffer file의 내용은 아무 것도 없어야 함
def test_buffer_file_should_be_empty(buf):
    buf_dir = f"{ROOT_DIR}\\buffer"

    for i in range(1, 6):
        file_path = os.path.join(buf_dir, f"{i}_empty")
        # 파일이 비어 있어야 함 (크기 0)
        assert os.path.getsize(file_path) == 0


# buffer write 후에도 buffer file의 내용은 아무 것도 없어야 함
def test_buffer_file_should_be_empty_after_buffer_write(buf):
    buf._reset_buffer()
    buf_dir = f"{ROOT_DIR}\\buffer"

    buf.write_buffer("W 31 0xAAAAAAAA")
    buf.write_buffer("W 32 0xBBBBBBBB")
    buf.write_buffer("W 33 0xCCCCCCCC")
    buf.read_buffer()

    # 모든 파일에 대해 내용이 비어 있는지 확인
    for fname in os.listdir(buf_dir):
        file_path = os.path.join(buf_dir, fname)
        # 파일 크기가 0이어야 함
        assert os.path.getsize(file_path) == 0


# buffer write + update 후에도 buffer file의 내용은 아무 것도 없어야 함
def test_buffer_file_should_be_empty_after_buffer_write2(buf):
    buf_dir = f"{ROOT_DIR}\\buffer"

    buf.write_buffer("W 31 0xAAAAAAAA")
    buf.write_buffer("W 32 0xBBBBBBBB")
    buf.write_buffer("W 33 0xCCCCCCCC")
    buf.write_buffer("E 33 2")
    buf.update_buffer()
    buf.read_buffer()

    assert buf._buffer == ['1_E_33_2', '2_W_31_0xAAAAAAAA', '3_W_32_0xBBBBBBBB', '4_empty', '5_empty']

    # 모든 파일에 대해 내용이 비어 있는지 확인
    for fname in os.listdir(buf_dir):
        file_path = os.path.join(buf_dir, fname)
        # 파일 크기가 0이어야 함
        assert os.path.getsize(file_path) == 0


# buffer flush 되어 있는 것 확인
def test_buffer_flush(buf):
    buf.write_buffer("W 31 0xAAAAAAAA")
    buf.write_buffer("W 32 0xBBBBBBBB")
    buf.write_buffer("W 33 0xCCCCCCCC")

    flushed_buf = buf.flush_buffer()

    assert flushed_buf == ['1_W_31_0xAAAAAAAA', '2_W_32_0xBBBBBBBB', '3_W_33_0xCCCCCCCC', '4_empty', '5_empty']
    assert buf._buffer == ['1_empty', '2_empty', '3_empty', '4_empty', '5_empty']


# buffer fast read 확인
def test_buffer_fast_read(buf):
    buf.write_buffer("W 31 0xAAAAAAAA")
    buf.write_buffer("W 32 0xBBBBBBBB")

    ret = buf.fast_read("31")

    assert ret == '0xAAAAAAAA'

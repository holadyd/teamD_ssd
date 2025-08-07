from Buffer import Buffer

def test_update_buffer_1():
    buf = Buffer()

    # Scenario1
    buf.write_buffer("W 20 0xABCDEFFF")
    buf.write_buffer("E 10 4")
    buf.write_buffer("E 12 3")  # 위의 3개를 합치면 W 20 ~ + E 10 5가 되어야 함

    buf.update_buffer()
    assert buf._buffer == ['1_W_20_0xABCDEFFF', '2_E_10_5', '3_empty', '4_empty', '5_empty']

def test_update_buffer_2():
    buf = Buffer()

    buf._reset_buffer()
    buf.write_buffer("E 30 10")
    buf.write_buffer("W 40 0xAAAAAAAA")
    buf.write_buffer("E 41 4")
    buf.write_buffer("W 45 0xBBBBBBBB")
    buf.write_buffer("E 46 5")

    buf.update_buffer()

    assert buf._buffer == ['1_E_30_10', '2_E_41_10', '3_W_40_0xAAAAAAAA', '4_W_45_0xBBBBBBBB', '5_empty']


def test_update_buffer_3():
    buf = Buffer()

    buf._reset_buffer()
    buf.write_buffer("E 31 6")
    buf.write_buffer("W 37 0xAAAAAAAA")
    buf.write_buffer("E 38 3")
    buf.write_buffer("E 41 10")
    buf.write_buffer("W 51 0xBBBBBBBB")

    buf.update_buffer()

    assert buf._buffer == ['1_E_31_10', '2_E_41_10', '3_W_37_0xAAAAAAAA', '4_W_51_0xBBBBBBBB', '5_empty']


def test_update_buffer_4():
    buf = Buffer()

    buf._reset_buffer()
    buf.write_buffer("E 31 6")
    buf.write_buffer("W 37 0xAAAAAAAA")
    buf.write_buffer("E 38 3")
    buf.write_buffer("W 41 0xBBBBBBBB")
    buf.write_buffer("E 42 10")

    buf.update_buffer()

    assert buf._buffer == ['1_E_31_10', '2_E_42_10', '3_W_37_0xAAAAAAAA', '4_W_41_0xBBBBBBBB', '5_empty']

def test_update_buffer_5():
    buf = Buffer()

    buf._reset_buffer()
    buf.write_buffer("W 31 0xAAAAAAAA")
    buf.write_buffer("W 32 0xBBBBBBBB")
    buf.write_buffer("W 33 0xCCCCCCCC")
    buf.write_buffer("W 34 0xDDDDDDDD")
    buf.write_buffer("W 36 0xEEEEEEEE")
    buf.write_buffer("E 34 2")

    buf.update_buffer()

    assert buf._buffer == ['1_W_31_0xAAAAAAAA', '2_W_32_0xBBBBBBBB', '3_W_33_0xCCCCCCCC', '4_W_36_0xEEEEEEEE', '5_E_34_2']



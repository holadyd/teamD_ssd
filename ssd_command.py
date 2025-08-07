from abc import ABC, abstractmethod


class SSDCommand(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def make_string(self):
        pass


class WriteCommand(SSDCommand):
    def __init__(self, lba, data):
        self.lba = lba
        self.data = data

    def validate(self):
        pass

    def make_string(self):
        pass


class ReadCommand(SSDCommand):
    def __init__(self, ssd, lba):
        self.ssd = ssd
        self.lba = lba

    def validate(self):
        pass

    def make_string(self):
        pass


class EraseCommand(SSDCommand):
    lba_upper_limit = 99
    lba_lower_limit = 0
    erase_size_range = 10

    def __init__(self, lba, data_size):
        self.lba = lba
        self.data_size = data_size

    def validate(self):
        try:
            lba: int = int(self.lba)  # lba 검증(숫자 여부)
            if 0 > lba or lba > 99:
                raise ValueError

            value: int = int(self.data_size)  # size value 검증(숫자 여부)
            if value < 0 or value > self.erase_size_range:
                raise ValueError
            if lba + value > self.lba_upper_limit:
                raise ValueError
            return True
        except (ValueError, TypeError):
            return False

    def make_string(self):
        pass

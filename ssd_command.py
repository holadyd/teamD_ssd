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
    def __init__(self, lba, data_size):
        self.lba = lba
        self.data_size = data_size

    def validate(self):
        pass

    def make_string(self):
        pass

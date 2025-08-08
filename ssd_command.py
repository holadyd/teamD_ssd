from abc import ABC, abstractmethod


class SSDCommand(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def make_string(self):
        pass


class InvalidCommand(SSDCommand):

    def validate(self):
        return False

    def make_string(self):
        return 'ERROR'


class WriteCommand(SSDCommand):
    def __init__(self, args):
        self.args = args
        self.lba, self.data = args

    def validate(self) -> bool:
        # value  invalid Check
        try:
            int(self.data, 0)  # 0이면 0x면 16진수, 0o면 8진수, 아니면 10진수

        except ValueError:
            return False

        if not (0x0 <= int(self.data, 0) <= 0xFFFFFFFF):
            return False
        # lba invalid Check
        # 1. int 인지 체크
        try:
            int(self.lba)
        except (ValueError, TypeError):
            return False

        # 2. 0~ 99 인지 체크
        if 0 <= int(self.lba) <= 99:
            return True
        return False

    def make_string(self):
        return f'W {self.lba} {self.data}'


class ReadCommand(SSDCommand):
    def __init__(self, args):
        self.args = args
        self.lba = args[0]

    def validate(self):
        # lba invalid Check
        # 1. int 인지 체크
        try:
            int(self.lba)
        except (ValueError, TypeError):
            return False

        # 2. 0~ 99 인지 체크
        if 0 <= int(self.lba) <= 99:
            return True
        return False

    def make_string(self):
        return f'R {self.lba}'


class EraseCommand(SSDCommand):
    lba_upper_limit = 99
    lba_lower_limit = 0
    erase_size_range = 10

    def __init__(self, args):
        self.args = args
        self.lba, self.data_size = args

    def validate(self):
        try:
            lba: int = int(self.lba)  # lba 검증(숫자 여부)
            if 0 > lba or lba > 99:
                raise ValueError

            value: int = int(self.data_size)  # size value 검증(숫자 여부)
            if value < 0 or value > self.erase_size_range:
                raise ValueError
            if lba + value > self.lba_upper_limit + 1:
                raise ValueError
            return True
        except (ValueError, TypeError):
            return False

    def make_string(self):
        return f'E {self.lba} {self.data_size}'


class FlushCommand(SSDCommand):

    def __init__(self, args):
        self.args = args

    def validate(self):
        return True

    def make_string(self):
        return 'flush'


class CommandFactory:
    @staticmethod
    def create(args) -> SSDCommand:
        if len(args) == 0 or str(args[0]).upper() not in ['R', 'W', 'E', 'F']:
            return InvalidCommand()
        command, *rest_args = args
        if command == "R":
            return ReadCommand(rest_args)
        if command == "W":
            return WriteCommand(rest_args)
        if command == 'E':
            return EraseCommand(rest_args)
        if command == 'F':
            return FlushCommand(rest_args)
        else:
            return InvalidCommand()

from abc import ABC, abstractmethod


class SSDCommand(ABC):
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def make_string(self):
        pass

    @staticmethod
    def convert_number_to_decimal(number_str: str) -> str:
        return str(int(number_str, 0))

    @staticmethod
    def convert_number_to_hex(number_str: str) -> str:
        number_str = str(number_str)
        if not number_str.startswith('0x'):
            str_value = hex(int(number_str, 0))
        return number_str[:2] + f'0000000{number_str[2:]}'[-8:].upper()


class InvalidCommand(SSDCommand):

    def validate(self):
        return False

    def make_string(self):
        return 'ERROR'


class WriteCommand(SSDCommand):
    def __init__(self, args):
        self.args = args
        self.lba, self.value = None, None

    def validate(self) -> bool:
        # value  invalid Check
        if len(self.args) != 2:
            return False
        self.lba, self.value = self.args

        try:
            int(self.value, 0)  # 0이면 0x면 16진수, 0o면 8진수, 아니면 10진수

        except (ValueError, TypeError):
            return False

        if not (0x0 <= int(self.value, 0) <= 0xFFFFFFFF):
            return False
        # lba invalid Check
        # 1. int 인지 체크
        try:
            int(self.lba, 0)
        except (ValueError, TypeError):
            return False

        # 2. 0~ 99 인지 체크
        if 0 <= int(self.lba, 0) <= 99:
            return True
        return False

    def make_string(self):
        return f'W {self.lba} {self.value}'

    def convert_value_to_hex(self):
        str_value = str(self.value)
        if not str_value.startswith('0x'):
            str_value = hex(int(str_value, 0))
        self.value = str_value[:2] + f'0000000{str_value[2:]}'[-8:].upper()


class ReadCommand(SSDCommand):
    def __init__(self, args):
        self.args = args
        self.lba = None

    def validate(self):
        if len(self.args) != 1:
            return False
        self.lba = self.args[0]

        # lba invalid Check
        # 1. int 인지 체크
        try:
            int(self.lba, 0)
        except (ValueError, TypeError):
            return False

        # 2. 0~ 99 인지 체크
        if 0 <= int(self.lba, 0) <= 99:
            return True
        return False

    def make_string(self):
        return f'R {self.lba}'

    def convert_lba_to_decimal(self):
        self.lba = str(int(self.lba, 0))


class EraseCommand(SSDCommand):
    lba_upper_limit = 99
    lba_lower_limit = 0
    erase_size_range = 10

    def __init__(self, args):
        self.args = args
        self.lba, self.data_size = None, None

    def validate(self):
        if len(self.args) != 2:
            return False
        self.lba, self.data_size = self.args

        try:
            lba: int = int(self.lba, 0)  # lba 검증(숫자 여부)
            if 0 > lba or lba > 99:
                raise ValueError

            value: int = int(self.data_size, 0)  # size value 검증(숫자 여부)
            if value < 0 or value > self.erase_size_range:
                raise ValueError
            if lba + value > self.lba_upper_limit + 1:
                raise ValueError
            return True
        except (ValueError, TypeError):
            return False

    def make_string(self):
        return f'E {self.lba} {self.data_size}'

    def convert_lba_to_decimal(self):
        self.lba = str(int(self.lba, 0))


class FlushCommand(SSDCommand):

    def __init__(self, args):
        self.args = args

    def validate(self):
        if len(self.args) != 0:
            return False
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

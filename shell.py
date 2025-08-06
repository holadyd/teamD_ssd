import json
from enum import Enum
import os
from hmac import compare_digest
import random
from random import randrange


class Shell:

    def __init__(self):
        self.command = None
        self.ret = True
        self.one_arg_lst = ["help", "exit", "fullread", '1_', '1_FullWriteAndReadCompare',
                            '2_', '2_PartialLBAWrite', '3_', '3_WriteReadAging']
        self.two_arg_lst = ["read", "fullwrite"]
        self.three_arg_lst = ["write"]
        self.prev_written_values = []

    def read_output(self):
        with open("ssd_output.txt", "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def run_shell(self):
        while self.ret:

            self.read_command()

            if self.valid_check():
                self.ret = self.run_command()

    def run_command(self):
        commands = self.command.strip().split(" ")

        if commands[0] == "write":
            address = commands[1]
            content = commands[2]
            self.ssd_write(address, content)
        elif commands[0] == "read":
            address = commands[1]
            self.ssd_read(address)
        elif commands[0] == "fullwrite":
            for address in range(100):
                content = commands[1]
                self.ssd_write(address, content)
        elif commands[0] == "fullread":
            for address in range(100):
                self.ssd_read(address)
        elif commands[0] == "help":
            self.print_help()
        elif commands[0] == "exit":
            print("Shell Exited Successfully.")
            return False
        elif commands[0] in ['1_', '1_FullWriteAndReadCompare']:
            self.run_script_1()
        elif commands[0] in ['2_', '2_PartialLBAWrite']:
            self.run_script_2()
        elif commands[0] in ['3_', '3_WriteReadAging']:
            self.run_script_3()

        return True

    def ssd_read(self, address, for_script=False):
        os.system(f"python ssd.py R {address}")
        result = self.read_output()["0"]
        if for_script:
            return result
        else:
            print(f"[Read] LBA {address} : {result}")

    def ssd_write(self, address, content, for_script=False):
        os.system(f"python ssd.py W {address} {content}")
        if for_script:
            return

        print("[Write] Done")

    def read_command(self, command=None):
        if command == None:
            self.command = input("Shell>")
        else:
            self.command = command

    def print_help(self):
        with open("help_docs.txt", "r", encoding="utf-8") as f:
            docs = f.readlines()
        print("".join(docs))

    def is_invalid_command(self, command_args):
        if command_args[0] not in self.one_arg_lst and \
                command_args[0] not in self.two_arg_lst and \
                command_args[0] not in self.three_arg_lst:
            return True
        return False

    def is_invalid_para_length(self, command_args):
        if command_args[0] in self.one_arg_lst:
            if len(command_args) != 1:
                return True
        if command_args[0] in self.two_arg_lst:
            if len(command_args) != 2:
                return True
        if command_args[0] in self.three_arg_lst:
            if len(command_args) != 3:
                return True
        return False

    def is_valid_format(self, command_args):
        if self.is_invalid_command(command_args):
            self.print_valid_error(self.ErrorPrintEnum.INVALID_COMMAND)
            return False
        if self.is_invalid_para_length(command_args):
            self.print_valid_error(self.ErrorPrintEnum.INVALID_PARAMETER_LENGTH)
            return False
        if command_args[0] in self.two_arg_lst:
            if not self.is_valid_number(command_args[1]):
                self.print_valid_error(self.ErrorPrintEnum.INVALID_DATA)
                return False
            if not self.is_data_in_range(command_args[1]):
                self.print_valid_error(self.ErrorPrintEnum.INVALID_LBA_RANGE)
                return False
            if not self.is_valid_address(command_args):
                return False

        if command_args[0] in self.three_arg_lst:
            if not self.is_valid_number(command_args[1]):
                self.print_valid_error(self.ErrorPrintEnum.INVALID_DATA)
                return False
            if not self.is_valid_number(command_args[2]):
                self.print_valid_error(self.ErrorPrintEnum.INVALID_DATA)
                return False
            if not self.is_data_in_range(command_args[2]):
                self.print_valid_error(self.ErrorPrintEnum.INVALID_LBA_RANGE)
                return False
            if not self.is_valid_address(command_args):
                return False
        return True

    def is_data_in_range(self, num):
        return 0x0 <= int(num, 0) <= 0xFFFFFFFF

    def is_valid_number(self, num):
        try:
            int(num, 0)  # 0이면 0x면 16진수, 0o면 8진수, 아니면 10진수
            return True
        except ValueError:
            return False

    def is_valid_address(self, command_args):
        if command_args[0] in ["exit", "help", "fullread", "fullwrite"]:
            return True
        if command_args[0] not in ["write", "read"]:
            return False
        address = command_args[1]

        if not 0 <= int(address) <= 99:
            self.print_valid_error(self.ErrorPrintEnum.INVALID_LBA_RANGE)
            return False

        return True

    def valid_check(self):

        command_args = self.command.strip().split(" ")

        if not self.is_valid_format(command_args):
            return False

        return True

    class ErrorPrintEnum(Enum):
        INVALID_COMMAND = 0
        INVALID_PARAMETER_LENGTH = 1
        INVALID_DATA = 2
        INVALID_LBA_RANGE = 3

    def print_valid_error(self, error_type):
        if error_type == self.ErrorPrintEnum.INVALID_COMMAND:
            print("[Error] INVALID COMMAND")
        elif error_type == self.ErrorPrintEnum.INVALID_PARAMETER_LENGTH:
            print("[Error] INVALID PARAMETER LENGTH")
        elif error_type == self.ErrorPrintEnum.INVALID_DATA:
            print("[Error] INVALID_DATA")
        elif error_type == self.ErrorPrintEnum.INVALID_LBA_RANGE:
            print("[Error] INVALID_DATA")

    def read_compare(self, compare_list):
        for (address, value) in compare_list:
            ret = self.ssd_read(address, for_script=True)
            if ret != value:
                print("FAIL")
                return
        print("PASS")

    def run_script_1(self):
        unique_values = self.generate_unique_random(100)
        for addr_shift in range(10):
            compare_list = []
            for start_addr in range(5) :
                unique_value = unique_values[addr_shift * 10 + start_addr]
                self.ssd_write(f'{start_addr + addr_shift}', f'0x{unique_value:08x}', for_script=True)
                compare_list.append((f'{start_addr+ addr_shift}', f'0x{unique_value:08x}'))
            self.read_compare(compare_list)

    def run_script_2(self):

        compare_list = [
            ("0", "0x0000FFFF"),
            ("1", "0x0000FFFF"),
            ("2", "0x0000FFFF"),
            ("3", "0x0000FFFF"),
            ("4", "0x0000FFFF")
        ]
        for _ in range(30):
            self.ssd_write("4", "0x0000FFFF", for_script=True)
            self.ssd_write("0", "0x0000FFFF", for_script=True)
            self.ssd_write("3", "0x0000FFFF", for_script=True)
            self.ssd_write("1", "0x0000FFFF", for_script=True)
            self.ssd_write("2", "0x0000FFFF", for_script=True)
            self.read_compare(compare_list)

    def run_script_3(self):
        for _ in range(200):
            value1 = f'0x{randrange(0xFFFFFFFF + 1):08x}'
            value2 = f'0x{randrange(0xFFFFFFFF + 1):08x}'
            compare_list = [
                ("0", value1),
                ("99", value2)
            ]
            self.ssd_write("0", value1, for_script=True)
            self.ssd_write("99", value2, for_script=True)
            self.read_compare(compare_list)

    def generate_unique_random(self, count):
        min_val, max_val = (0, 0xFFFFFFFF)
        unique_values = set()

        while len(unique_values) < count:
            val = random.randint(min_val, max_val)
            if val not in self.prev_written_values and val not in unique_values:
                unique_values.add(val)

        return list(unique_values)


if __name__ == "__main__":
    shell = Shell()
    shell.run_shell()

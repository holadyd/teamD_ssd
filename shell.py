import json
from enum import Enum
import os
from hmac import compare_digest
import random
from logger import Logger
import sys
from script import Script


class Shell:

    def __init__(self):
        self.command = None
        self.ret = True
        self.one_arg_lst = ["help", "exit", "fullread", '1_', '1_FullWriteAndReadCompare',
                            '2_', '2_PartialLBAWrite', '3_', '3_WriteReadAging']
        self.two_arg_lst = ["read", "fullwrite"]
        self.three_arg_lst = ["write"]
        self.arguments = self.one_arg_lst + self.two_arg_lst + self.three_arg_lst
        self.prev_written_values = []
        self._is_runner_mode = False
        self.logger = Logger()
        self.script = Script(self)

    def read_output(self):
        self.logger_print(f"function executed")
        with open("ssd_output.txt", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.logger_print(data)
        return data

    def logger_print(self, message):
        method_name = f'{self.__class__.__name__}.{sys._getframe(1).f_code.co_name}()'
        self.logger.print(method_name, message)

    def console_print(self, message):
        if not self._is_runner_mode:
            print(message)

    def run_shell(self):
        self.logger_print("Shell Application Run")
        while self.ret:

            self.read_command()

            if self.valid_check():
                self.ret = self.run_command()

    def run_command(self):
        self.logger_print(f'run command with {self.command}')
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
            self.console_print("Shell Exited Successfully.")
            self.logger_print(f'shell exited with exit command')
            return False
        elif commands[0] in ['1_', '1_FullWriteAndReadCompare']:
            self.run_script_1()
        elif commands[0] in ['2_', '2_PartialLBAWrite']:
            self.run_script_2()
        elif commands[0] in ['3_', '3_WriteReadAging']:
            self.run_script_3()

        return True

    def ssd_read(self, address, for_script=False):
        self.logger_print(f'read {address}, for_script is {for_script}')
        os.system(f"python ssd.py R {address}")
        result = self.read_output()["0"]
        self.logger_print(f"[Read] LBA {address} : {result}")

        if for_script:
            return result

        self.console_print(f"[Read] LBA {address} : {result}")

    def ssd_write(self, address, content, for_script=False):
        self.logger_print(f'read {address}, content {content}, for_script is {for_script}')
        os.system(f"python ssd.py W {address} {str(hex(int(content, 0)))}")
        self.logger_print(f'[Write] Done - {address}, {content}')
        if for_script:
            return

        self.console_print("[Write] Done")

    def read_command(self, command=None):
        self.logger_print(f'wait command, preset command: {command}')
        if command == None:
            self.command = input("Shell>")
        else:
            self.command = command
        self.logger_print(f'input command: {self.command}')

    def print_help(self):
        self.logger_print(f'print help docs')
        with open("help_docs.txt", "r", encoding="utf-8") as f:
            docs = f.readlines()
        self.console_print("".join(docs))

    def is_invalid_command(self, command_args):
        self.logger_print(f'command_args: {command_args}')
        if command_args[0] not in self.arguments:
            self.logger_print(f'return True')
            return True
        self.logger_print(f'return False')
        return False

    def is_invalid_para_length(self, command_args):
        self.logger_print(f'command_args: {command_args}')
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
        self.logger_print(f'command_args: {command_args}')
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

        address_numb = int(address, 0)

        if not 0 <= address_numb <= 99:
            self.print_valid_error(self.ErrorPrintEnum.INVALID_LBA_RANGE)
            return False

        return True

    def valid_check(self):
        command_args = self.command.strip().split(" ")
        self.logger_print(f'command_args: {command_args}')

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
            self.console_print("[Error] INVALID COMMAND")
        elif error_type == self.ErrorPrintEnum.INVALID_PARAMETER_LENGTH:
            self.console_print("[Error] INVALID PARAMETER LENGTH")
        elif error_type == self.ErrorPrintEnum.INVALID_DATA:
            self.console_print("[Error] INVALID_DATA")
        elif error_type == self.ErrorPrintEnum.INVALID_LBA_RANGE:
            self.console_print("[Error] INVALID_DATA")

    def read_compare(self, compare_list):
        for (address, value) in compare_list:
            ret = self.ssd_read(address, for_script=True)
            if ret != value:
                self.console_print("FAIL")
                return
        self.console_print("PASS")

    def run_script_1(self):
        self.script.script_1()

    def run_script_2(self):
        self.script.script_2()

    def run_script_3(self):
        self.script.script_3()

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

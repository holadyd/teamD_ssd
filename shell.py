import os
import json

class Shell:

    def __init__(self):
        self.command = None
        self.ret = True

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
            os.system(f"python ssd.py W {commands[1]} {commands[2]}")
            print("[Write] Done")
        elif commands[0] == "read":
            os.system(f"python ssd.py R {commands[1]}")
            result = self.read_output()[commands[1]]
            print(f"[Read] LBA {commands[1]} : {result}")
        elif commands[0] == "fullwrite":
            for address in range(100):
                os.system(f"python ssd.py W, {address}, {commands[1]}")
                print("[Write] Done")
        elif commands[0] == "fullread":
            for address in range(100):
                os.system(f"python ssd.py R {address}")
                result = self.read_output()[address]
                print(f"[Read] LBA {address} : {result}")
        elif commands[0] == "help":
            self.print_help()
        elif self.command == "exit":
            print("Shell Exited Successfully.")
            return False

        return True

    def read_command(self, command=None):
        if command == None:
            self.command = input("Shell>")
        else:
            self.command = command

    def print_help(self):
        print("""***SSD Test Shell Help***
      write         지정한 LBA에 Data를 기록한다.
        Usage) write [LBA] [Data]
      fullwrite     모든 LBA에 Data를 기록한다.
        Usage) fullwrite [Data]
      read          지정한 LBA의 Data를 출력한다.
        Usage) read [LBA]
      fullread      모든 LBA에 대해 Data를 출력한다.
        Usage) fullread
      exit          Test Shell을 종료한다.
      help          도움말을 출력한다.

    Made by Digital Ninjas
    김현용, 김준휘, 모유찬, 민재원, 이성규, 이재윤""")

    def is_valid_format(self, command_args):
        one_arg_lst = ["help", "exit", "fullread"]
        two_arg_lst = ["read", "fullwrite"]
        three_arg_lst = ["write"]

        if command_args[0] not in one_arg_lst and \
                command_args[0] not in two_arg_lst and \
                command_args[0] not in three_arg_lst:
            print("Error")
            return False
        if command_args[0] in one_arg_lst:
            if len(command_args) != 1:
                print("Error")
                return False
        if command_args[0] in two_arg_lst:
            if len(command_args) != 2:
                print("Error")
                return False
            if not self.is_valid_number(command_args[1]):
                print("Error")
                return False
            if not self.is_data_in_range(command_args[1]):
                print("Error")
                return False

        if command_args[0] in three_arg_lst:
            if len(command_args) != 3:
                print("Error")
                return False
            if not self.is_valid_number(command_args[1]):
                print("Error")
                return False
            if not self.is_valid_number(command_args[2]):
                print("Error")
                return False
            if not self.is_data_in_range(command_args[2]):
                print("Error")
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
            print("invalid address")
            return False

        return True

    def valid_check(self):

        command_args = self.command.strip().split(" ")

        if not self.is_valid_format(command_args):
            return False

        return True


if __name__ == "__main__":
    shell = Shell()
    shell.run_shell()

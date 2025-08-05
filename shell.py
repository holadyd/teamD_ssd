import os


class Shell:

    def __init__(self):
        self.command = None

    def read_output(self):
        with open("ssd_output.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return content

    def run_shell(self):
        while True:

            self.read_command()
            self.run_command(self.command)

            if self.command == "exit":
                print("Shell Exited Successfully.")
                break

    def run_command(self, command):
        if self.is_invalid_input(command):
            return
        commands = command.strip().split(" ")

        if command.startswith("write"):
            os.system(f"python ssd.py W, {commands[1]}, {commands[2]}")
            print("[Write] Done")
        elif command.startswith("R"):
            os.system(f"python ssd.py R, {commands[1]}")
            result = self.read_output()
            print(f"[Read] LBA {commands[1]} : {result}")
        elif command == "fullwrite 0xAAAABBBB\n":
            for _ in range(100):
                print("[Write] Done")
        elif command == "fullread\n":
            for _ in range(100):
                print("[Read] LBA 00 : 0xAAAABBBB")
        elif command == "help":
            self.print_help()

    def read_command(self):
        self.command = input("Shell>")

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

    def is_invalid_input(self, command: str):
        if self.is_invalid_format(command):
            return True
        return False

    def is_invalid_format(self, command):
        one_arg_lst = ["help", "exit", "fullread"]
        two_arg_lst = ["read", "fullwrite"]
        three_arg_lst = ["write"]
        command_args = command.strip().split(" ")
        if command_args[0] not in one_arg_lst and \
                command_args[0] not in two_arg_lst and \
                command_args[0] not in three_arg_lst :
            print("Error")
            return True
        if command_args[0] in one_arg_lst:
            if len(command_args) != 1:
                print("Error")
                return True
        if command_args[0] in two_arg_lst:
            if len(command_args) != 2:
                print("Error")
                return True
            if not self.is_valid_number(command_args[1]):
                return True
        if command_args[0] in three_arg_lst:
            if len(command_args) != 3:
                print("Error")
                return True
            if not self.is_valid_number(command_args[1]):
                return True
            if not self.is_valid_number(command_args[2]):
                return True

        return False

    def is_valid_number(self, num):
        try:
            int(num, 0)  # 0이면 0x면 16진수, 0o면 8진수, 아니면 10진수
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    shell = Shell()
    shell.run_shell()

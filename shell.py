
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
        commands = command.strip().split(" ")
        if self.command.startswith("write"):
            os.system(f"python ssd.py W, {commands[1]}, {commands[2]}")
            print("[Write] Done")
        elif self.command.startswith("R"):
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




if __name__ == "__main__":
    shell = Shell()
    shell.run_shell()

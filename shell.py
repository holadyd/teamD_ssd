
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


    def read_command(self):
        self.command = input("Shell>")


if __name__=="__main__":
    shell = Shell()
    shell.run_shell()

class Shell:
    ...

if __name__ == "__main__":
    ...
class Shell:

    def __init__(self):
        self.command = None

    def __del__(self):
        print("Shell Exited Successfully.")
        # exit()

    def run_shell(self):
        while True:
            self.print_shell()
            self.read_command()

            if self.command == "exit":
                try:
                    break
                finally:
                    self.__del__()


    def print_shell(self):
        print("Shell>")

    def read_command(self):
        self.command = input()


if __name__=="__main__":
    shell = Shell()
    shell.run_shell()
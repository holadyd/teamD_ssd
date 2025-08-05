class Shell:

    def __init__(self):
        self.command = None

    def run_shell(self):
        while True:
            self.print_shell()
            self.read_command()

            if self.command == "exit":
                pass

    def print_shell(self):
        print("Shell>")

    def read_command(self):
        self.command = input()


if __name__=="__main__":
    shell = Shell()
    shell.run_shell()
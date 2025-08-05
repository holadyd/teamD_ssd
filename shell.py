
class Shell:
    ...

if __name__ == "__main__":
    ...
class Shell:

    def __init__(self):
        self.command = None

    def run_shell(self):
        while True:


            self.read_command()
            self.run_command()

            if self.command == "exit":
                print("Shell Exited Successfully.")
                break



    def run_command(self):
        ...

    def read_command(self):
        self.command = input("Shell>")


if __name__=="__main__":
    shell = Shell()
    shell.run_shell()
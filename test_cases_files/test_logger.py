from logger.logger import Logger
from shell import Shell
import time

def input_command(shell, command):
    shell.read_command(command)
    if shell.valid_check():
        shell.run_command()

def test_log_print(mocker):
    shell = Shell()
    test_log = f'{time.time()}.log'
    shell.logger = Logger(log_dir='../test_logs', log_file=f'{test_log}', max_bytes=100 * 1024)
    shell.logger._get_timestamp = mocker.Mock()
    shell.logger._get_timestamp.return_value = '2025-08-07 11:53:47'

    input_command(shell, "write 3 3")
    input_command(shell, "read 3")
    input_command(shell, "help")
    input_command(shell, "exit")

    with open(f'../test_logs/expected.log', 'r') as file:
        expected = file.readlines()
    with open(f'./test_logs/{test_log}', 'r') as file:
        test_result = file.readlines()

    assert test_result == expected



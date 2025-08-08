from random import randrange


class Script:
    def __init__(self, shell):
        self.shell = shell

    def input_dummy_command(self):
        for i in range(5):
            self.shell.erase(f'{i*10}', '10')

    def script_1(self):
        self.input_dummy_command()
        self.shell._is_test_pass = True
        self.shell.logger_print(f'script1 executed')
        unique_values = self.shell.generate_unique_random(100)
        for addr_shift in range(10):
            compare_list = []
            for start_addr in range(5):
                unique_value = unique_values[addr_shift * 10 + start_addr]
                self.shell.ssd_write(f'{start_addr + addr_shift}', f'0x{unique_value:08X}', for_script=True)
                compare_list.append((f'{start_addr + addr_shift}', f'0x{unique_value:08X}'))

            self.shell.read_compare(compare_list)

    def script_2(self):
        self.input_dummy_command()
        self.shell._is_test_pass = True
        self.shell.logger_print(f'script2 executed')
        compare_list = [
            ("0", "0x0000FFFF"),
            ("1", "0x0000FFFF"),
            ("2", "0x0000FFFF"),
            ("3", "0x0000FFFF"),
            ("4", "0x0000FFFF")
        ]
        for _ in range(30):
            self.shell.ssd_write("4", "0x0000FFFF", for_script=True)
            self.shell.ssd_write("0", "0x0000FFFF", for_script=True)
            self.shell.ssd_write("3", "0x0000FFFF", for_script=True)
            self.shell.ssd_write("1", "0x0000FFFF", for_script=True)
            self.shell.ssd_write("2", "0x0000FFFF", for_script=True)
            self.shell.read_compare(compare_list)

    def script_3(self):
        self.input_dummy_command()
        self.shell._is_test_pass = True
        self.shell.logger_print(f'script3 executed')
        for _ in range(200):
            value1 = f'0x{randrange(0xFFFFFFFF + 1):08X}'
            value2 = f'0x{randrange(0xFFFFFFFF + 1):08X}'
            compare_list = [
                ("0", value1),
                ("99", value2)
            ]
            self.shell.ssd_write("0", value1, for_script=True)
            self.shell.ssd_write("99", value2, for_script=True)
            self.shell.read_compare(compare_list)

    def script_4(self):
        self.input_dummy_command()
        self.shell._is_test_pass = True
        self.shell.logger_print(f'script4 executed')
        self.shell.ssd_erase("0", "1", for_script=True)
        self.shell.ssd_erase("1", "1", for_script=True)
        self.shell.ssd_erase("2", "1", for_script=True)

        for _ in range(30):
            for i in range(48):
                value1 = f'0x{randrange(0xFFFFFFFF + 1):08X}'
                value2 = f'0x{randrange(0xFFFFFFFF + 1):08X}'
                compare_list = [
                    (f'{2*i+2}', '0x00000000'),
                    (f'{2*i+3}', '0x00000000'),
                    (f'{2*i+4}', '0x00000000'),
                ]
                self.shell.ssd_write(f'{2*i+2}', value1, for_script=True)
                self.shell.ssd_write(f'{2*i+2}', value2, for_script=True)

                self.shell.ssd_erase(f'{2*i+2}', "1", for_script=True)
                self.shell.ssd_erase(f'{2*i+3}', "1", for_script=True)
                self.shell.ssd_erase(f'{2*i+4}', "1", for_script=True)

                self.shell.read_compare(compare_list)
            break

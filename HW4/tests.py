import unittest
from io import StringIO
from unittest.mock import patch
from nomer4 import Assembler


class TestAssemblerCommands(unittest.TestCase):
    def setUp(self):
        self.assembler = Assembler("input1.txt", "output.bin", "log.json")

    @patch("builtins.open")
    def test_all_commands(self, mock_open):
        # Мокируем вывод в файл
        mock_output = StringIO()
        mock_open.return_value.__enter__.return_value = mock_output

        # Тестовые команды
        commands = [
            "LOAD_CONST 63 366",  # LOAD_CONST
            "READ_MEMORY 32 524",  # READ_MEMORY
            "WRITE_MEMORY 97 79",  # WRITE_MEMORY
            "MAX 144 895"  # MAX
        ]

        # Обрабатываем каждую команду
        for command in commands:
            self.assembler.process_line(command)

        # Ожидаемые инструкции после обработки команд
        expected_instructions = [
            (63, 366),  # LOAD_CONST
            (32, 524),  # READ_MEMORY
            (97, 79),  # WRITE_MEMORY
            (144, 895)  # MAX
        ]
        self.assertEqual(self.assembler.instructions, expected_instructions)

        # Генерация бинарного файла
        self.assembler.write_binary()

        # Проверка бинарного вывода
        binary_output = mock_output.getvalue().strip()
        expected_binary = (
            "0x3F, 0x6E, 0x01, 0x00, 0x00\n"  # LOAD_CONST
            "0x20, 0x0C, 0x02, 0x00, 0x00\n"  # READ_MEMORY
            "0x61, 0x4F, 0x00, 0x00, 0x00\n"  # WRITE_MEMORY
            "0x90, 0x7F, 0x03, 0x00, 0x00"  # MAX
        )
        self.assertEqual(binary_output, expected_binary)


if __name__ == '__main__':
    unittest.main()

import unittest
from io import StringIO
from contextlib import redirect_stdout

# Импортируем функции и переменные из основного файла
from ta3 import parse_config, convert_to_toml_format, constants

class TestConfigParser(unittest.TestCase):

    def run_parser(self, input_lines):
        """Утилита для тестирования всего процесса парсинга."""
        constants.clear()  # Очищаем константы перед каждым тестом
        config_data = parse_config(input_lines)
        return convert_to_toml_format(config_data)

    def test_simple_block(self):
        input_lines = [
            "set max_users = 100",
            "begin",
            "  current_users := 10;",
            "  max := ?{max_users};",
            "end"
        ]
        expected_output = """begin
  current_users := 10;
  max := 100;
end"""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_multiple_blocks(self):
        input_lines = [
            "set greeting = @\"Hello!\"",
            "begin",
            "  message := ?{greeting};",
            "end",
            "begin",
            "  count := 42;",
            "end"
        ]
        expected_output = """begin
  message := @"Hello!";
end
begin
  count := 42;
end"""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_string_handling(self):
        input_lines = [
            "begin",
            "  text := @\"This is a test string\";",
            "end"
        ]
        expected_output = """begin
  text := @"This is a test string";
end"""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_set_and_use_constants(self):
        input_lines = [
            "set number = 123",
            "set text = @\"Sample text\"",
            "begin",
            "  num := ?{number};",
            "  str := ?{text};",
            "end"
        ]
        expected_output = """begin
  num := 123;
  str := @"Sample text";
end"""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_missing_begin(self):
        input_lines = [
            "  some_key := 1;",
            "end"
        ]
        with self.assertRaises(SyntaxError) as context:
            self.run_parser(input_lines)
        self.assertEqual(str(context.exception), "Присваивание значения возможно только внутри 'begin ... end'.")

    def test_unknown_constant(self):
        input_lines = [
            "begin",
            "  some_key := ?{unknown};",
            "end"
        ]
        with self.assertRaises(ValueError) as context:
            self.run_parser(input_lines)
        self.assertEqual(str(context.exception), "Неизвестная константа: unknown")

    def test_invalid_syntax(self):
        input_lines = [
            "invalid syntax"
        ]
        with self.assertRaises(SyntaxError) as context:
            self.run_parser(input_lines)
        self.assertEqual(str(context.exception), "Неверная строка: invalid syntax")

    def test_nested_begin(self):
        input_lines = [
            "begin",
            "  inner_key := 1;",
            "  begin",
            "    nested_key := 2;",
            "  end",
            "end"
        ]
        with self.assertRaises(SyntaxError) as context:
            self.run_parser(input_lines)
        self.assertEqual(str(context.exception), "Невозможно вложить 'begin' в 'begin'.")

    def test_empty_input(self):
        input_lines = []
        expected_output = ""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_just_constants(self):
        input_lines = [
            "set pi = 3.14",
            "set message = @\"Hello, World!\""
        ]
        expected_output = ""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_single_value_assignment(self):
        input_lines = [
            "begin",
            "  value := 42;",
            "end"
        ]
        expected_output = """begin
  value := 42;
end"""
        self.assertEqual(self.run_parser(input_lines), expected_output)

    def test_string_constant(self):
        input_lines = [
            "set greeting = @\"Hi, there!\"",
            "begin",
            "  message := ?{greeting};",
            "end"
        ]
        expected_output = """begin
  message := @"Hi, there!";
end"""
        self.assertEqual(self.run_parser(input_lines), expected_output)


if __name__ == "__main__":
    unittest.main()


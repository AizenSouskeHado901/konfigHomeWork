import unittest
from io import StringIO
import sys
import toml
from ta3 import parse_config, parse_value, constants

class TestConfigToTOML(unittest.TestCase):

    def setUp(self):
        """Сбрасываем константы перед каждым тестом"""
        constants.clear()

    def test_basic_config(self):
        """Тест на корректное преобразование простой конфигурации"""
        input_data = """
        set db_name = @"example_db"
        set db_port = 5432

        begin
         username := @"admin";
         password := @"pass123";
         host := @"localhost";
         port := ?{db_port};
         database := ?{db_name};
        end
        """
        expected_output = {
            "username": "admin",
            "password": "pass123",
            "host": "localhost",
            "port": 5432,
            "database": "example_db"
        }
        config_data = parse_config(input_data.strip().splitlines())
        self.assertEqual(config_data, expected_output)

    def test_server_config(self):
        """Тест на корректное преобразование конфигурации сервера"""
        input_data = """
        set server_name = @"my_server"
        set server_port = 8080

        begin
         host := @"127.0.0.1";
         port := ?{server_port};
         server_name := ?{server_name};
         root_directory := @"/var/www/html";
        end
        """
        expected_output = {
            "host": "127.0.0.1",
            "port": 8080,
            "server_name": "my_server",
            "root_directory": "/var/www/html"
        }
        config_data = parse_config(input_data.strip().splitlines())
        self.assertEqual(config_data, expected_output)

    def test_invalid_syntax(self):
        """Тест на обработку ошибки при некорректном синтаксисе"""
        input_data = """
        set db_name = @"example_db"
        
        begin
         username := "admin";  # Неправильный синтаксис, отсутствует @ в строке
         password := @"pass123";
        end
        """
        with self.assertRaises(SyntaxError):
            parse_config(input_data.strip().splitlines())

    def test_unknown_constant(self):
        """Тест на ошибку при использовании неизвестной константы"""
        input_data = """
        begin
         username := ?{undefined_constant};
        end
        """
        with self.assertRaises(ValueError) as context:
            parse_config(input_data.strip().splitlines())
        self.assertIn("Неизвестная константа", str(context.exception))

    def test_value_parsing(self):
        """Тест на корректное парсинг значений: числа, строки и ссылки на константы"""
        constants["existing_constant"] = "constant_value"
        self.assertEqual(parse_value("123"), 123)  # Число
        self.assertEqual(parse_value('@"string_value"'), "string_value")  # Строка с правильным синтаксисом
        self.assertEqual(parse_value("?{existing_constant}"), "constant_value")  # Константа


    def test_output_to_toml(self):
        """Тест на проверку финального вывода в формате TOML"""
        input_data = """
        set example_key = @"example_value"

        begin
         key1 := @"value1";
         key2 := ?{example_key};
         key3 := 42;
        end
        """
        expected_output = {
            "key1": "value1",
            "key2": "example_value",
            "key3": 42
        }
        config_data = parse_config(input_data.strip().splitlines())
        toml_output = toml.dumps(config_data)
        self.assertEqual(toml.loads(toml_output), expected_output)

if __name__ == "__main__":
    unittest.main()

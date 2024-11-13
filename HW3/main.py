import re
import sys
import toml
from typing import Union, Dict

# Словарь для хранения констант
constants = {}

# Регулярные выражения для элементов конфигурационного языка
patterns = {
    "begin": r"^begin\s*$",
    "end": r"^end\s*$",
    "set": r"^set\s+([a-zA-Z][_a-zA-Z0-9]*)\s*=\s*(.+)\s*$",
    "assign": r"^([a-zA-Z][_a-zA-Z0-9]*)\s*:=\s*(.+)\s*;$",
    "string": r'^@"(.*)"$',
    "constant_ref": r"^\?\{([a-zA-Z][_a-zA-Z0-9]*)\}$",
}

def parse_value(value: str) -> Union[int, str, None]:
    """Парсит значение: число, строка или ссылка на константу."""
    if re.match(r"^\d+$", value):
        return int(value)
    if re.match(patterns["string"], value):
        return re.match(patterns["string"], value).group(1)
    if re.match(patterns["constant_ref"], value):
        name = re.match(patterns["constant_ref"], value).group(1)
        if name in constants:
            return constants[name]
        else:
            raise ValueError(f"Неизвестная константа: {name}")
    return None

def parse_config(input_lines):
    """Парсит конфигурацию и возвращает структуру данных в виде словаря."""
    result = {}
    current_dict = None

    for line in input_lines:
        line = line.strip()
        if re.match(patterns["begin"], line):
            if current_dict is not None:
                raise SyntaxError("Невозможно вложить 'begin' в 'begin'.")
            current_dict = {}
        elif re.match(patterns["end"], line):
            if current_dict is None:
                raise SyntaxError("Найден 'end' без соответствующего 'begin'.")
            result.update(current_dict)
            current_dict = None
        elif re.match(patterns["set"], line):
            name, value = re.match(patterns["set"], line).groups()
            constants[name] = parse_value(value)
        elif re.match(patterns["assign"], line):
            if current_dict is None:
                raise SyntaxError("Присваивание значения возможно только внутри 'begin ... end'.")
            name, value = re.match(patterns["assign"], line).groups()
            current_dict[name] = parse_value(value)
        elif line:
            raise SyntaxError(f"Неверная строка: {line}")
    return result

def main():
    # Считываем входные данные из stdin
    input_lines = sys.stdin.readlines()
    try:
        config_data = parse_config(input_lines)
        toml_output = toml.dumps(config_data)
        print(toml_output)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()

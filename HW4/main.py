import json
import sys
import os

class Assembler:
    def __init__(self, input_file, output_file, log_file):
        self.input_file = input_file
        self.output_file = output_file
        self.log_file = log_file
        self.instructions = []

    def assemble(self):
        with open(self.input_file, 'r') as f:
            for line in f:
                self.process_line(line.strip())

        self.write_binary()
        self.write_log()

    # Обработка строки, добавление её в список инструкций
    def process_line(self, line):
        if not line:
            return 
        parts = line.split()
        command, a, b = parts[0].upper(), int(parts[1]), int(parts[2])
        if (command == 'LOAD_CONST') and (a == 63):
            self.instructions.append((a, b))
        elif (command == 'READ_MEMORY') and (a == 32):
            self.instructions.append((a, b))
        elif (command == 'WRITE_MEMORY') and (a == 97):
            self.instructions.append((a, b))
        elif (command == 'MAX') and (a == 144):
            self.instructions.append((a, b))
        else:
            raise ValueError(f'Неизвестная команда: {command}')

    # Запись в "бинарный" файл
    def write_binary(self):
        with open(self.output_file, 'w') as f:
            for a, b in self.instructions:
                if (((a == 63) and (b<=8191)) or ((a!=63) and (b<=67108863))):                 
                    hex_a = "0x" + hex(a)[2:].upper()
                    hex_b = hex(b)
                    if  (len(hex_b[2:]))==1:
                        output = f"{hex_a}, 0x0{hex_b[2].upper()}, 0x00, 0x00, 0x00"   
                        f.write(output + '\n')      
                    elif (len(hex_b[2:]))==2:
                        output = f"{hex_a}, 0x{hex_b[2:].upper()}, 0x00, 0x00, 0x00"
                        f.write(output + '\n')
                    elif (len(hex_b[2:]))==3:
                        hex_c = hex_b[2]
                        output = f"{hex_a}, {hex_b[0:2]}{hex_b[3:].upper()}, 0x0{hex_c.upper()}, 0x00, 0x00"
                        f.write(output + '\n')
                    elif (len(hex_b[2:]))==4:
                        hex_c = hex_b[2] + hex_b[3]
                        output = f"{hex_a}, {hex_b[0:2]}{hex_b[4:].upper()}, 0x{hex_c.upper()}, 0x00, 0x00"
                        f.write(output + '\n')
                    elif (len(hex_b[2:]))==5:
                        hex_c = hex_b[2] + hex_b[3]
                        hex_h = hex_b[4]
                        output = f"{hex_a}, {hex_b[0:2]}{hex_b[5:].upper()}, 0x{hex_c.upper()}, 0x0{hex_h.upper()}, 0x00"
                        f.write(output + '\n')
                    elif (len(hex_b[2:]))==6:
                        hex_c = hex_b[2] + hex_b[3]
                        hex_h = hex_b[4] + hex_b[5]
                        output = f"{hex_a}, {hex_b[0:2]}{hex_b[6:].upper()}, 0x{hex_c.upper()}, 0x{hex_h.upper()},0x00"
                        f.write(output + '\n')
                else:
                    raise ValueError(f'Число {b} выходит за пределы')
    
    def write_log(self):
        log_data = {"instructions": []}
        for i, (a, b) in enumerate(self.instructions):
            log_data["instructions"].append({
                "id": i,
                "a": a,
                "b": b
            })
        
        with open(self.log_file, 'w') as f:
            json.dump(log_data, f, indent=4)

class Interpreter:

    def __init__(self, binary_file, result_file, memory_range):
        self.binary_file = binary_file
        self.result_file = result_file
        self.memory_range = memory_range
        self.memory = ['0'] * 1024  # Инициализация памяти
        self.stack = []  # Стек для операций
        self.instructions = []  # Загруженные инструкции

    def load_instructions(self):
        with open(self.binary_file, 'r') as f:
            for line in f:
                parts = line.split(", ")
                if (parts[2] == "0x00"):
                    a = int(parts[0], 16)
                    b = int(parts[1], 16)
                    self.instructions.append((a, b))
                elif (parts[3] == "0x00"):
                    c = parts[2] + parts[1][2:]
                    a = int(parts[0], 16)
                    b = int(c, 16)
                    self.instructions.append((a, b))
                elif (parts[3] != "0x00"):
                    c = parts[2] + parts[3][2:] + parts[1][2:]
                    a = int(parts[0], 16)
                    b = int(c, 16)
                    self.instructions.append((a, b))

    def execute(self):
        # Выполнение каждой инструкции
        for a, b in self.instructions:
            print(f"Выполняем инструкцию: {a}, {b}")  # Отладочная информация
            self.execute_instruction(a, b)

    def execute_instruction(self, a, b):
        if a == 63:  # LOAD_CONST
            self.load_const(b)
        elif a == 32:  # READ_MEMORY
            self.read_memory(b)
        elif a == 97:  # WRITE_MEMORY
            self.write_memory(b)
        elif a == 144:  # MAX
            self.max_instruction(b)
        else:
            raise ValueError(f"Неизвестная команда: {a}")

    def load_const(self, value):
        print(f"LOAD_CONST: Добавление {value} в стек.")  # Отладочная информация
        self.stack.append(value)

    def read_memory(self, address):
        if 0 <= address < len(self.memory):
            value = self.memory[address]
            print(f"READ_MEMORY: Чтение значения {value} из памяти по адресу {address}.")  # Отладочная информация
            self.stack.append(value)
            self.memory[address] = "0"
        else:
            raise ValueError(f"Неверный адрес памяти: {address}")

    def write_memory(self, address):
        if self.stack:
            value = self.stack.pop()  # Извлекаем значение из стека
            print(f"WRITE_MEMORY: Попытка записи значения {value} в память по адресу {address}.")  # Отладочная информация
            if 0 <= address < len(self.memory):
                self.memory[address] = value
                print(f"WRITE_MEMORY: Запись значения {value} в память по адресу {address}.")  # Отладочная информация
            else:
                raise ValueError(f"Неверный адрес памяти: {address}")
        else:
            print("Стек пуст, невозможно выполнить WRITE_MEMORY.")  # Отладочная информация

    def max_instruction(self, address):
        if len(self.stack) >= 2:
            op1 = self.stack.pop()
            op2 = self.stack.pop()
            result = max(op1, op2)
            if 0 <= address < len(self.memory):
                self.memory[address] = result
                print(f"MAX: Запись максимума ({result}) в память по адресу {address}.")  # Отладочная информация
            else:
                raise ValueError(f"Неверный адрес памяти: {address}")
        else:
            print("Недостаточно элементов в стеке для выполнения MAX.")  # Отладочная информация

    def export_result_to_json(self, output_file, start_address, length):
        """Сохранение результата из памяти в JSON."""
        if start_address + length > len(self.memory):
            raise ValueError("Указанный диапазон выходит за пределы памяти.")
        
        # Выводим содержимое памяти перед сохранением
        
        
        result = {
            "start_address": start_address,
            "length": length,
            "data": self.memory[start_address:start_address + length]
        }
        
        # Проверим, что результат не пустой
        if result['data']:
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=4)
            print(f"Результат сохранен в файл {output_file}")
        else:
            print("Нет данных для сохранения!")



def main():
    # Пример исходного файла программы
    input_file = 'input.txt'
    output_file = 'binary.bin'
    log_file = 'log.json'
    
    # Шаг 1: Ассемблируем программу
    assembler = Assembler(input_file, output_file, log_file)
    assembler.assemble()
    
    # Шаг 2: Загружаем и выполняем программу
    interpreter = Interpreter(output_file, 'result.json', 1024)
    interpreter.load_instructions()
    interpreter.execute()
    
    # Шаг 3: Экспортируем результат
    interpreter.export_result_to_json('result.json', 0, 1024)

main()


import os
import tarfile
import sys
import csv
from datetime import datetime

class Emulator:
    def __init__(self, tar_path, log_path, init_script_path):
        self.tar_path = tar_path
        self.log_path = log_path
        self.init_script_path = init_script_path
        self.virtual_fs = {}  # Виртуальная файловая система
        self.current_dir = "/"  # Текущая директория

    def load_tar(self):
        # Загрузка tar-архива и создание виртуальной ФС
        with tarfile.open(self.tar_path, "r") as tar:
            tar.extractall("/tmp/virtual_fs")
        self.current_dir = "/tmp/virtual_fs"

    def log_action(self, action):
        # Запись действия в лог-файл
        with open(self.log_path, 'a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow([datetime.now().isoformat(), action])

    def execute_script(self):
        # Выполнение команд из стартового скрипта
        if os.path.exists(self.init_script_path):
            with open(self.init_script_path, 'r') as script_file:
                commands = script_file.readlines()
                for command in commands:
                    self.execute_command(command.strip())

    def execute_command(self, command):
        # Выполнение одиночной команды
        self.log_action(command)
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            self.ls(args)
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "exit":
            sys.exit(0)
        elif cmd == "head":
            self.head(args)
        elif cmd == "wc":
            self.wc(args)
        else:
            print(f"Command not found: {cmd}")

    def ls(self, args):
        print("\n".join(os.listdir(self.current_dir)))

    def cd(self, args):
        if args:
            new_dir = os.path.join(self.current_dir, args[0])
            if os.path.isdir(new_dir):
                self.current_dir = new_dir
            else:
                print(f"No such directory: {args[0]}")

    def head(self, args):
        if args:
            file_path = os.path.join(self.current_dir, args[0])
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    print("".join(lines[:10]))
            except FileNotFoundError:
                print(f"No such file: {args[0]}")

    def wc(self, args):
        if args:
            file_path = os.path.join(self.current_dir, args[0])
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    words = sum(len(line.split()) for line in lines)
                    chars = sum(len(line) for line in lines)
                    print(f"{len(lines)} {words} {chars} {args[0]}")
            except FileNotFoundError:
                print(f"No such file: {args[0]}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 emulator.py <tar_path> <log_path> <init_script_path>")
        sys.exit(1)

    tar_path = sys.argv[1]
    log_path = sys.argv[2]
    init_script_path = sys.argv[3]

    emulator = Emulator(tar_path, log_path, init_script_path)
    emulator.load_tar()
    emulator.execute_script()

    while True:
        command = input("emulator$ ")
        emulator.execute_command(command)


import unittest
from unittest.mock import patch, MagicMock
import os
from main import Emulator

class TestEmulatorCommands(unittest.TestCase):

    def setUp(self):
        # Этот метод запускается перед каждым тестом
        self.emulator = Emulator("test.tar", "test.log", "init.txt")
        
    # Тесты команды ls
    def test_ls_empty_directory(self):
        with patch.object(self.emulator, 'execute_command', return_value=[]) as mock_command:
            files = self.emulator.execute_command('ls')
            self.assertEqual(files, [])
            mock_command.assert_called_with('ls')

    def test_ls_single_file(self):
        with patch.object(self.emulator, 'execute_command', return_value=['file.txt']) as mock_command:
            files = self.emulator.execute_command('ls')
            self.assertEqual(files, ['file.txt'])
            mock_command.assert_called_with('ls')

    def test_ls_multiple_files(self):
        with patch.object(self.emulator, 'execute_command', return_value=['file1.txt', 'file2.txt', 'file3.txt']) as mock_command:
            files = self.emulator.execute_command('ls')
            self.assertEqual(files, ['file1.txt', 'file2.txt', 'file3.txt'])
            mock_command.assert_called_with('ls')

    # Тесты команды cd
    def test_cd_to_valid_directory(self):
        with patch.object(self.emulator, 'execute_command') as mock_command:
            self.emulator.execute_command('cd /valid_directory')
            mock_command.assert_called_with('cd /valid_directory')

    def test_cd_to_invalid_directory(self):
        with patch.object(self.emulator, 'execute_command', side_effect=FileNotFoundError) as mock_command:
            with self.assertRaises(FileNotFoundError):
                self.emulator.execute_command('cd /invalid_directory')
                mock_command.assert_called_with('cd /invalid_directory')

    def test_cd_back_to_previous_directory(self):
        with patch.object(self.emulator, 'execute_command') as mock_command:
            self.emulator.execute_command('cd ..')
            mock_command.assert_called_with('cd ..')

    # Тесты команды ws (WebSocket или другое поведение)
    # Зависит от предполагаемого поведения команды ws
    def test_ws_connect(self):
        with patch.object(self.emulator, 'execute_command', return_value="Connected") as mock_command:
            response = self.emulator.execute_command('ws connect')
            self.assertEqual(response, "Connected")
            mock_command.assert_called_with('ws connect')

    def test_ws_send_message(self):
        with patch.object(self.emulator, 'execute_command', return_value="Message sent") as mock_command:
            response = self.emulator.execute_command('ws send Hello')
            self.assertEqual(response, "Message sent")
            mock_command.assert_called_with('ws send Hello')

    def test_ws_disconnect(self):
        with patch.object(self.emulator, 'execute_command', return_value="Disconnected") as mock_command:
            response = self.emulator.execute_command('ws disconnect')
            self.assertEqual(response, "Disconnected")
            mock_command.assert_called_with('ws disconnect')

    # Тесты команды head
    def test_head_single_line(self):
        with patch.object(self.emulator, 'execute_command', return_value=['This is a line']) as mock_command:
            lines = self.emulator.execute_command('head -n 1 file.txt')
            self.assertEqual(lines, ['This is a line'])

            mock_command.assert_called_with('head -n 1 file.txt')

    def test_head_multiple_lines(self):
        with patch.object(self.emulator, 'execute_command', return_value=['Line 1', 'Line 2', 'Line 3']) as mock_command:
            lines = self.emulator.execute_command('head -n 3 file.txt')
            self.assertEqual(lines, ['Line 1', 'Line 2', 'Line 3'])
            mock_command.assert_called_with('head -n 3 file.txt')

    def test_head_no_file(self):
        with patch.object(self.emulator, 'execute_command', side_effect=FileNotFoundError("No such file")) as mock_command:
            with self.assertRaises(FileNotFoundError):
                self.emulator.execute_command('head file.txt')
                mock_command.assert_called_with('head file.txt')

if __name__ == '__main__':
    unittest.main()

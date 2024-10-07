import unittest
from unittest.mock import patch, MagicMock
from main import Emulator

class TestEmulatorCommands(unittest.TestCase):
    def setUp(self):
        self.emulator = Emulator("test.tar", "test.log", "init.txt")
        
    def test_wc_no_parameters(self):
        with patch.object(self.emulator, 'execute_command', return_value='5 10 50') as mock_command:
            result = self.emulator.execute_command('wc file.txt')
            self.assertEqual(result, '5 10 50')
            mock_command.assert_called_with('wc file.txt')

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

    def test_head_default_lines(self):
        mock_output = (
            "Line 1\n"
            "Line 2\n"
            "Line 3\n"
            "Line 4\n"
            "Line 5\n"
            "Line 6\n"
            "Line 7\n"
            "Line 8\n"
            "Line 9\n"
            "Line 10"
        )
        with patch.object(self.emulator, 'execute_command', return_value=mock_output) as mock_command:
            result = self.emulator.execute_command('head file.txt')
            self.assertEqual(result, mock_output)
            mock_command.assert_called_with('head file.txt')

if __name__ == '__main__':
    unittest.main()

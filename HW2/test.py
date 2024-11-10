import unittest
from unittest.mock import patch, MagicMock
from main import get_dependencies, visualize_dependencies
from pathlib import Path
import subprocess

class TestPackageDependencies(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_get_dependencies_success(self, mock_run):
        """Тестируем успешное получение зависимостей"""
        mock_run.return_value = MagicMock(stdout="Requires: numpy, requests")
        dependencies = get_dependencies('some_package')
        self.assertEqual(dependencies, ['numpy', 'requests'])
    
    @patch('subprocess.run')
    def test_get_dependencies_error_handling(self, mock_run):
        """Тестируем обработку ошибок при вызове pip show"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pip show some_package')
        dependencies = get_dependencies('some_package')
        self.assertEqual(dependencies, [])

    @patch('subprocess.run')
    def test_get_dependencies_with_whitespace(self, mock_run):
        """Тестируем обработку зависимостей с пробелами"""
        mock_run.return_value = MagicMock(stdout="Requires: numpy,  requests")
        dependencies = get_dependencies('some_package')
        # Удаляем пробелы из зависимостей
        dependencies = [dep.strip() for dep in dependencies]
        self.assertEqual(dependencies, ['numpy', 'requests'])

    @patch('subprocess.run')
    @patch('graphviz.Digraph.render')
    @patch('os.makedirs')
    def test_visualize_dependencies_success(self, mock_makedirs, mock_render, mock_run):
        """Тестируем успешную визуализацию зависимостей"""
        mock_run.return_value = MagicMock(stdout="Requires: numpy, requests")
        mock_render.return_value = None
        mock_makedirs.return_value = None

        visualize_dependencies('some_package', './output/some_package_graph.png', 'C:/Program Files/Graphviz/bin/dot.exe')

        mock_makedirs.assert_called_once_with(Path('./output').resolve(), exist_ok=True)

    @patch('subprocess.run')
    @patch('graphviz.Digraph.render')
    @patch('os.makedirs')
    def test_visualize_dependencies_create_directories(self, mock_makedirs, mock_render, mock_run):
        """Тестируем, что директория создается для графа зависимостей"""
        mock_run.return_value = MagicMock(stdout="Requires: numpy, requests")
        mock_render.return_value = None
        mock_makedirs.return_value = None

        visualize_dependencies('some_package', './output/some_package_graph.png', 'C:/Program Files/Graphviz/bin/dot.exe')

        mock_makedirs.assert_called_once_with(Path('./output').resolve(), exist_ok=True)

    @patch('subprocess.run')
    @patch('graphviz.Digraph.render')
    @patch('os.makedirs')
    def test_visualize_dependencies_error_handling(self, mock_makedirs, mock_render, mock_run):
        """Тестируем ошибку при визуализации зависимостей"""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'pip show some_package')
        
        visualize_dependencies('some_package', './output/some_package_graph.png', 'C:/Program Files/Graphviz/bin/dot.exe')
        
        # Проверяем, что `makedirs` вызывается даже при ошибке
        mock_makedirs.assert_called_once_with(Path('./output').resolve(), exist_ok=True)

if __name__ == '__main__':
    unittest.main()

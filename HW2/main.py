import subprocess
import sys
import os
from graphviz import Digraph

def get_dependencies(package_name):
    """Получаем список зависимостей пакета с помощью pip."""
    # Запускаем команду pip show для получения информации о пакете
    result = subprocess.run([sys.executable, '-m', 'pip', 'show', package_name], capture_output=True, text=True)

    # Считываем зависимости
    dependencies = []
    for line in result.stdout.splitlines():
        if line.startswith('Requires:'):
            deps = line.split(':')[1].strip()
            dependencies = deps.split(', ') if deps else []
    return dependencies

def visualize_dependencies(package_name, output_image_path, graphviz_path):
    """Визуализируем зависимости пакета и сохраняем граф."""
    # Получаем зависимости
    dependencies = get_dependencies(package_name)

    # Создаем объект Graphviz
    dot = Digraph(comment=package_name)

    # Устанавливаем параметры графа (по желанию можно настроить)
    dot.attr(size='20,20', dpi='300', nodesep='1.0', rankdir='LR')

    # Добавляем основной узел для пакета
    dot.node(package_name)

    # Добавляем зависимости как узлы и соединяем их с основным пакком
    for dep in dependencies:
        dot.node(dep)  # Добавляем зависимость как узел
        dot.edge(package_name, dep)  # Создаем ребро (связь) между пакетом и зависимостью

    # Проверка наличия директории и создание всех промежуточных папок
    output_dir = os.path.dirname(output_image_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)  # Создаем директорию, если её нет

    # Сохраняем граф в файл
    dot.render(output_image_path, format='png', cleanup=True)
    print(f"Граф зависимостей для {package_name} сохранён в {output_image_path}")

# Пример использования для пакета requests
visualize_dependencies('requests', './output/requests_dependency_graph.png', 'C:/Program Files/Graphviz/bin/dot.exe')

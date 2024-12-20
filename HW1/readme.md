# Конфигурационное управление.
## Задание 1
Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата 
**tar**. Эмулятор должен работать в режиме **CLI**.

Ключами командной строки задаются:
- Путь к архиву виртуальной файловой системы.
- Путь к лог-файлу.

- Путь к стартовому скрипту.

Лог-файл имеет формат **csv** и содержит все действия во время последнего сеанса работы с эмулятором. Для каждого действия указаны дата и время.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также следующие команды:
- head.
- wc.

Все функции эмулятора должны быть покрыты тестами, а для каждой из поддерживаемых команд необходимо написать 3 теста.

---
## Запуск программы
Для запуска программы используется **Git Bash**, но подойдут и другие командные строки. Далее будет представлена пошаговая инструкция.
1. Сначала скачиваем данный репозиторий себе на компьютер
2. Открываем **Git Bash**, видим перед нами окно

![1](https://github.com/user-attachments/assets/48cf10ef-c22a-4bf6-97d6-3469d2bb7cbb)


3. Теперь нужно перейти в директорию с программой. Для этого нужно прописать команду cd и указать ей относительный путь:

cd Desktop

![2](https://github.com/user-attachments/assets/7a44fcb8-14a0-43b5-8b73-822017fe5743)


4. Для запуска самой программы нужно указать следующую команду:


python3 <название_программы.py> <путь_к_архиву.tar> <путь_к_log-файлу.csv> <путь_к_начальному_скрипту.txt>

5. После этого программа запущена.

![3](https://github.com/user-attachments/assets/31ed8514-1195-4a57-8c34-d1e370a6e70e)


---

## Команда ls

Команда **ls** отображает файлы и каталоги, находящиеся внутри данного каталога.

![4](https://github.com/user-attachments/assets/27621214-62e4-4a17-9ff9-72c056dceace)


---

## Команда cd

Команда **cd** изменяет текущий каталог на указанный. Если не передан аргумент, то возвращает в домашний каталог.

![5](https://github.com/user-attachments/assets/1cf458db-4abe-41e6-b167-fc20cc8b9179)



## Команда head

Команда **head** выводит первые 10 строк файла.

![6](https://github.com/user-attachments/assets/ecdeccea-6691-4e10-a115-4017ab3f2995)


---

## Команда wc

Команда **wc** выводит количество переноса строки, количество слов и количество символов в файле.

![7](https://github.com/user-attachments/assets/a1de97c5-4f7b-4b12-823b-eb5fc444b40a)


## Команда exit

Команда **exit** используется для завершения работы эмулятора.



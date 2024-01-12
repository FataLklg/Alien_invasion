import os, sys


def resource_path(relative):
    """Помогает правильно определять пути к файлам при переводе в exe."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def save_record_to_file(score):
    """Сохраняет рекорд в файл."""
    filepath = resource_path('record.txt')
    with open(filepath, 'w') as f:
        f.write(str(score))

def read_record_from_file():
    """Считывает рекорд из файла или создаёт его, если файл отсутствует."""
    try:
        filepath = resource_path('record.txt')
        with open(filepath) as file:
            record = file.read()
        return int(record)
    except FileNotFoundError:
        with open(filepath, 'w') as file:
           record = file.write('0')
    return record

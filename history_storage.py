import json
import os

# Путь к файлу с историей (корень проекта)
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

def load_history():
    """Загружает историю из файла"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []
    except Exception as e:
        print(f"Ошибка загрузки истории: {e}")
        return []

def save_history(history):
    """Сохраняет историю в файл"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Ошибка сохранения истории: {e}")
        return False

def add_history_record(record):
    """Добавляет новую запись в историю"""
    history = load_history()
    # Добавляем запись в начало списка (сначала новые)
    history.insert(0, record)
    # Оставляем только последние 100 записей
    if len(history) > 100:
        history = history[:100]
    return save_history(history)

def clear_history():
    """Очищает всю историю"""
    return save_history([])

def delete_history_record(index):
    """Удаляет одну запись истории по индексу"""
    history = load_history()
    if 0 <= index < len(history):
        history.pop(index)
        return save_history(history)
    return False
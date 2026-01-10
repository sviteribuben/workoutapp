"""Модуль для работы с данными тренировок."""

import json
from pathlib import Path
from datetime import date

from models import Workout, WorkoutsData, Stats
from constants import WorkoutType


# Save JSON file in the same directory as this module (src_workout)
DATA_FILE = Path(__file__).parent / "workouts.json"


def load_data() -> WorkoutsData:
    """Загружает данные из JSON файла.
    
    Returns:
        WorkoutsData: Словарь с данными тренировок.
        
    Raises:
        OSError: Если произошла ошибка при чтении файла.
    """
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return {"workouts": []}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            # Валидация структуры данных
            if not isinstance(data, dict) or "workouts" not in data:
                return {"workouts": []}
            return data
    except (json.JSONDecodeError, OSError):
        return {"workouts": []}


def save_data(data: WorkoutsData) -> None:
    """Сохраняет данные в JSON файл.
    
    Args:
        data: Словарь с данными тренировок.
        
    Raises:
        OSError: Если произошла ошибка при записи файла.
    """
    try:
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise OSError(f"Не удалось сохранить данные: {e}") from e


def add_workout(was_done: bool, w_type: WorkoutType, comment: str) -> None:
    """Добавляет новую тренировку в хранилище.
    
    Args:
        was_done: Была ли выполнена тренировка.
        w_type: Тип тренировки.
        comment: Комментарий к тренировке.
        
    Raises:
        OSError: Если произошла ошибка при сохранении данных.
    """
    data = load_data()
    workouts = data.get("workouts", [])
    new_id = (workouts[-1]["id"] + 1) if workouts else 1
    
    workout: Workout = {
        "id": new_id,
        "date": date.today().isoformat(),
        "was_done": was_done,
        "type": w_type,
        "comment": comment,
    }
    
    workouts.append(workout)
    data["workouts"] = workouts
    save_data(data)


def get_all_workouts() -> list[Workout]:
    """Возвращает список всех тренировок.
    
    Returns:
        list[Workout]: Список всех тренировок.
    """
    data = load_data()
    return data.get("workouts", [])


def get_stats() -> Stats:
    """Вычисляет статистику по выполненным тренировкам.
    
    Returns:
        Stats: Словарь со статистикой.
    """
    data = load_data()
    workouts = [w for w in data.get("workouts", []) if w.get("was_done", False)]
    total = len(workouts)
    push_ups = sum(1 for w in workouts if w.get("type") == "push_ups")
    strength = sum(1 for w in workouts if w.get("type") == "strength_set")
    
    return {
        "total": total,
        "push_ups": push_ups,
        "strength_set": strength,
    }


def reset_data() -> None:
    """Полностью очищает прогресс тренировок.
    
    Raises:
        OSError: Если произошла ошибка при сохранении данных.
    """
    empty: WorkoutsData = {"workouts": []}
    save_data(empty)

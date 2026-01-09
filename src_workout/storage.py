import json
from pathlib import Path
from datetime import date
from typing import Any


# Save JSON file in the same directory as this module (src_workout)
DATA_FILE = Path(__file__).parent / "workouts.json"

def load_data() -> dict:
    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        return {"workouts": []}

    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {"workouts": []}

def add_workout(was_done: bool, w_type: Any, comment: str) -> None:
    data = load_data()
    workouts = data.get("workouts", [])
    new_id = (workouts[-1]["id"] + 1) if workouts else 1
    workouts.append(
        {
            "id": new_id,
            "date": date.today().isoformat(),
            "was_done": was_done,
            "type": w_type,
            "comment": comment,
        }
    )
    data["workouts"] = workouts
    save_data(data)

def save_data(data: dict) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_all_workouts() -> list[dict]:
    data = load_data()
    return data.get("workouts", [])

def get_stats() -> dict:
    data = load_data()
    workouts = [w for w in data.get("workouts", []) if w["was_done"]]
    total = len(workouts)
    push_ups = sum(1 for w in workouts if w["type"] == "push_ups")
    strength = sum(1 for w in workouts if w["type"] == "strength_set")
    return {
        "total": total,
        "push_ups": push_ups,
        "strength_set": strength,
    }

def reset_data() -> None:
    """Полностью очищает прогресс тренировок."""
    empty = {"workouts": []}
    save_data(empty)

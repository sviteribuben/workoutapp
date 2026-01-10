"""Константы для типов тренировок и других значений."""

from typing import Literal

# Типы тренировок
WorkoutType = Literal["push_ups", "strength_set"]

# Значения для статуса тренировки
WORKOUT_DONE_YES = "yes"
WORKOUT_DONE_NO = "no"

# Маппинг типов тренировок на отображаемые названия
WORKOUT_TYPE_DISPLAY_NAMES: dict[str, str] = {
    "push_ups": "Push ups",
    "strength_set": "Strength set",
}

# Маппинг статусов на отображаемые названия
WORKOUT_STATUS_DISPLAY_NAMES: dict[bool, str] = {
    True: "Была",
    False: "Не была",
}

"""Типы данных для проекта."""

from typing import TypedDict

from constants import WorkoutType


class Workout(TypedDict):
    """Структура данных тренировки."""
    id: int
    date: str  # ISO format: YYYY-MM-DD
    was_done: bool
    type: WorkoutType
    comment: str


class WorkoutsData(TypedDict):
    """Структура данных файла workouts.json."""
    workouts: list[Workout]


class Stats(TypedDict):
    """Статистика по тренировкам."""
    total: int
    push_ups: int
    strength_set: int

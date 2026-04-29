# Feature Order and Mappings - Shared between Training and Inference
FEATURE_ORDER = [
    'study_hours', 'break_time', 'sleep_hours', 'focus_score', 'previous_score',
    'course_encoded', 'difficulty_encoded', 'goal_encoded', 'energy_encoded', 
    'time_encoded', 'distraction_encoded', 'day_encoded'
]

COURSE_MAP = {
    "general": 0, "data structures": 1, "algorithms": 2, "dbms": 3,
    "machine learning": 4, "mathematics": 5
}

DIFFICULTY_MAP = {"low": 0, "medium": 1, "high": 2}
GOAL_MAP = {"concept": 0, "revision": 1, "exam": 2}
ENERGY_MAP = {"low": 0, "medium": 1, "high": 2}
TIME_MAP = {"morning": 0, "afternoon": 1, "night": 2}
DISTRACTION_MAP = {"low": 0, "medium": 1, "high": 2}
DAY_MAP = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, 
    "friday": 4, "saturday": 5, "sunday": 6
}

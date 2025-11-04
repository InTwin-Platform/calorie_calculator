from enum import Enum


class WeightGoal(Enum):
    MAINTAIN = "maintain"
    LOSE = "lose"
    GAIN = "gain"


class ActivityLevel(Enum):
    SEDENTARY = "S"
    LIGHTLY_ACTIVE = "LA"
    MODERATELY_ACTIVE = "MA"
    VERY_ACTIVE = "VA"
    SUPER_ACTIVE = "SA"

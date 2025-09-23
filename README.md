# Caloric Calculator

Internal package for calculating daily caloric needs.

## Functions

- **`calculate_bmi()`** - Body Mass Index from weight and height
- **`calculate_adjusted_weight()`** - Ideal weight adjusted for actual weight  
- **`calculate_bmr()`** - Basal Metabolic Rate (calories burned at rest)
- **`get_activity_factor()`** - Activity level multiplier (S=1.2, LA=1.375, MA=1.55, VA=1.725, SA=1.9)
- **`calculate_caloric_requirements()`** - Total daily calories to maintain weight
- **`calculate_daily_caloric_needs()`** - Target calories for weight goal (lose/gain/maintain)

## Installation
```bash
pip install git+https://github.com/InTwin-Platform/calorie_calculator.git
```

## Usage

```python
from caloric_calculator import CaloricCalculator, WeightGoal

calculator = CaloricCalculator(
    weight=70,           # kg
    height=175,          # cm
    age=30,
    sex='M',             # 'M' or 'F'
    activity_level='MA', # 'S', 'LA', 'MA', 'VA', 'SA'
    weight_goal=WeightGoal.LOSE,
    weight_amount="0.5"  # kg per week
)

daily_calories = calculator.calculate_daily_caloric_needs()
print(f"Daily calories: {daily_calories}")
```
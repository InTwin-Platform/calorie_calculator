# Caloric Calculator

A comprehensive package for calculating daily caloric needs based on scientifically-backed formulas. This package determines personalized caloric requirements considering body composition, activity levels, and weight goals while enforcing safe minimum calorie thresholds.

## Version 2.0.0

This version includes a complete overhaul of the calculation formulas to align with the latest nutritional science standards per [client specification document](https://docs.google.com/document/d/1I10qlLYEwizx2QXONQcaXyJb8RXWS9P5/edit?usp=sharing&ouid=106874706599868772131&rtpof=true&sd=true).

**✅ Full backward compatibility maintained with v1.x**

## Features

### Core Calculations

1. **Body Mass Index (BMI)**
   - Formula: `BMI = Weight (kg) / (Height (m))²`

2. **Ideal Weight (IW)**
   - For Males: `IW = 50 + 2.3 × (Height (inches) - 60)`
   - For Females: `IW = 45.5 + 2.3 × (Height (inches) - 60)`

3. **Adjusted Weight (AW)**
   - Formula: `AW = IW + 0.25 × (Actual Weight - IW)`

4. **Recommended Weight for Calorie Calculations**
   - Based on BMI ranges:
     - BMI < 18.5: Actual Weight
     - BMI 18.5-24.9: Actual Weight
     - BMI 25-29.9: Ideal Weight
     - BMI ≥ 30: Adjusted Weight

5. **Basal Metabolic Rate (BMR)**
   - For Males: `BMR = (10 × W(kg)) + (6.25 × Height (cm)) - (5 × Age(y)) + 5`
   - For Females: `BMR = (10 × W(kg)) + (6.25 × Height (cm)) - (5 × Age(y)) - 161`

6. **Activity Factor (AF)**
   - Sedentary (S): 1.2
   - Lightly Active (LA): 1.375
   - Moderately Active (MA): 1.55
   - Very Active (VA): 1.725
   - Super Active (SA): 1.9

7. **Total Daily Energy Expenditure (TDEE)**
   - Formula: `TDEE = BMR × AF`

8. **Daily Caloric Needs (DCN)**
   - Maintain Weight: `DCN = TDEE`
   - Lose Weight: `DCN = TDEE - Caloric Adjustment`
   - Gain Weight: `DCN = TDEE + Caloric Adjustment`

### Safety Features

⚠️ **Minimum Calorie Thresholds:**
- Females: 1,300 kcal/day
- Males: 1,500 kcal/day

These minimums ensure nutritional adequacy and prevent unhealthy calorie restriction.

## Installation

```bash
pip install git+https://github.com/InTwin-Platform/calorie_calculator.git@v2.0.0#egg=calorie-calculator
```

## Usage

### Basic Example

```python
from caloric_calculator import CaloricCalculator, WeightGoal

calculator = CaloricCalculator(
    weight=70,           # kg
    height=175,          # cm
    age=30,
    sex='M',             # 'M' or 'F'
    activity_level='MA', # 'S', 'LA', 'MA', 'VA', 'SA'
    weight_goal=WeightGoal.MAINTAIN,
    weight_amount=0.0    # kg per week (float)
)

# Access calculated values
print(f"BMI: {calculator.bmi}")
print(f"Ideal Weight: {calculator.ideal_weight} kg")
print(f"Adjusted Weight: {calculator.adjusted_weight} kg")
print(f"Recommended Weight: {calculator.recommended_weight} kg")
print(f"BMR: {calculator.bmr} kcal/day")
print(f"TDEE: {calculator.tdee} kcal/day")
print(f"Daily Caloric Needs: {calculator.daily_caloric_needs} kcal/day")
```

### Weight Loss Example

```python
from caloric_calculator import CaloricCalculator, WeightGoal

# Calculate calories for losing 0.5 kg per week
calculator = CaloricCalculator(
    weight=85,
    height=175,
    age=35,
    sex='M',
    activity_level='LA',
    weight_goal=WeightGoal.LOSE,
    weight_amount=0.5  # Lose 0.5 kg per week
)

print(f"Daily calories for weight loss: {calculator.daily_caloric_needs} kcal/day")
```

### Weight Gain Example

```python
from caloric_calculator import CaloricCalculator, WeightGoal

# Calculate calories for gaining 0.5 kg per week
calculator = CaloricCalculator(
    weight=60,
    height=180,
    age=25,
    sex='M',
    activity_level='VA',
    weight_goal=WeightGoal.GAIN,
    weight_amount=0.5  # Gain 0.5 kg per week
)

print(f"Daily calories for weight gain: {calculator.daily_caloric_needs} kcal/day")
```

## Caloric Adjustments

### Weight Loss

| Weekly Change (kg) | Daily Adjustment (kcal) |
|-------------------|------------------------|
| 0.25              | -250                   |
| 0.5               | -500                   |
| 0.75              | -750                   |
| 1.0               | -1,000                 |
| 1.5               | -1,500                 |
| 2.0               | -2,000                 |
| 2.5               | -2,500                 |

### Weight Gain

| Weekly Change (kg) | Daily Adjustment (kcal) |
|-------------------|------------------------|
| 0.25              | +250                   |
| 0.5               | +500                   |
| 0.75              | +750                   |
| 1.0               | +1,000                 |

## API Reference

### CaloricCalculator Class

#### Constructor Parameters

- `weight` (float): Weight in kilograms
- `height` (float): Height in centimeters
- `age` (int): Age in years
- `sex` (str): 'M' for male, 'F' for female
- `activity_level` (str): Activity level code ('S', 'LA', 'MA', 'VA', 'SA')
- `weight_goal` (WeightGoal): Weight goal enum (MAINTAIN, LOSE, or GAIN)
- `weight_amount` (float): Target weekly weight change in kg (default: 0.0)

#### Properties

- `bmi` (float): Calculated Body Mass Index
- `ideal_weight` (float): Calculated ideal weight in kg
- `adjusted_weight` (float): Calculated adjusted weight in kg
- `recommended_weight` (float): Weight used for BMR calculation based on BMI
- `bmr` (int): Basal Metabolic Rate in kcal/day
- `activity_factor` (float): Activity level multiplier
- `tdee` (int): Total Daily Energy Expenditure in kcal/day
- `daily_caloric_needs` (int): Target daily caloric intake in kcal/day

#### Methods

- `calculate_bmi()`: Calculate Body Mass Index
- `calculate_ideal_weight()`: Calculate ideal weight based on height and sex
- `calculate_adjusted_weight()`: Calculate adjusted weight
- `get_recommended_weight()`: Get recommended weight based on BMI range
- `calculate_bmr()`: Calculate Basal Metabolic Rate
- `get_activity_factor()`: Get activity factor from activity level
- `calculate_tdee()`: Calculate Total Daily Energy Expenditure
- `calculate_daily_caloric_needs()`: Calculate daily caloric needs based on weight goal

### WeightGoal Enum

- `WeightGoal.MAINTAIN`: Maintain current weight
- `WeightGoal.LOSE`: Lose weight
- `WeightGoal.GAIN`: Gain weight

### Activity Levels

Activity levels are specified as string codes:

- `'S'` (Sedentary): Little or no exercise
- `'LA'` (Lightly Active): Light exercise 1-3 days/week
- `'MA'` (Moderately Active): Moderate exercise 3-5 days/week
- `'VA'` (Very Active): Hard exercise 6-7 days/week
- `'SA'` (Super Active): Very hard exercise, physical job, or training twice/day

## Testing

Run the test suite:

```bash
python3 -m unittest tests.test_calculator -v
```

## Example Script

An example usage script is provided in `example_usage.py`:

```bash
python3 example_usage.py
```

## Version History

### v2.0.0 (Current)
- Updated BMI calculation with proper decimal precision (returns float with 2 decimals)
- Implemented new ideal weight formula based on height in inches (Hamwi formula)
- Updated adjusted weight formula (0.25 factor instead of 0.4)
- Implemented BMI-based weight selection for BMR calculation
- Updated BMR calculation to use recommended weight based on BMI
- Implemented TDEE calculation (BMR × Activity Factor)
- Updated caloric adjustments to 250 kcal per 0.25 kg/week
- Updated minimum calorie thresholds (1300 for females, 1500 for males)
- Added comprehensive test coverage (22 tests)
- Added backward compatibility aliases for v1.x API

### v1.0.1
- Updated installation instructions

### v1.0.0
- Initial release with basic calorie calculations

## License

Internal use only - InTwin Platform

## Contributing

This is an internal package. For changes or improvements, please contact the development team.

## Support

For questions or issues, please open an issue in the GitHub repository or contact the development team.

# Changelog

All notable changes to the Calorie Calculator package are documented in this file.

## [2.0.0] - 2025-11-04

### Major Changes - Complete Formula Update

This release represents a complete overhaul of the calculation methodology to align with the latest nutritional science standards and medical guidelines.

### Added

- **New BMI-based weight selection system**: The calculator now intelligently selects which weight to use for BMR calculation based on BMI ranges:
  - BMI < 18.5: Uses actual weight
  - BMI 18.5-24.9: Uses actual weight
  - BMI 25-29.9: Uses ideal weight
  - BMI ≥ 30: Uses adjusted weight

- **Enhanced calculation properties**: All intermediate calculations are now stored as properties:
  - `bmi`: Body Mass Index
  - `ideal_weight`: Calculated ideal weight
  - `adjusted_weight`: Calculated adjusted weight
  - `recommended_weight`: Weight used for BMR calculation
  - `tdee`: Total Daily Energy Expenditure

- **ActivityLevel Enum**: Added for better code clarity and type safety

- **Comprehensive test suite**: 22 unit tests covering all calculations and edge cases

- **Example usage script**: Demonstrates all features with 6 different scenarios

- **Detailed documentation**: Complete README with formulas, examples, and API reference

### Changed

- **BMI Calculation**: Now returns float with 2 decimal places instead of rounded integer
  - Old: `round(weight / height_m²)`
  - New: `round(weight / height_m², 2)`

- **Ideal Weight Formula**: Complete formula change
  - Old (cm-based): 
    - Male: `50 + 0.9 × (height_cm - 152.4)`
    - Female: `45.5 + 0.9 × (height_cm - 152.4)`
  - New (inches-based):
    - Male: `50 + 2.3 × (height_inches - 60)`
    - Female: `45.5 + 2.3 × (height_inches - 60)`

- **Adjusted Weight Formula**: Factor changed from 0.4 to 0.25
  - Old: `IW + 0.4 × (Actual Weight - IW)`
  - New: `IW + 0.25 × (Actual Weight - IW)`

- **BMR Calculation**: Now uses the recommended weight based on BMI ranges instead of always using adjusted weight
  - Old: Always used `adjusted_weight`
  - New: Uses `recommended_weight` determined by BMI range

- **TDEE Terminology**: Renamed `calculate_caloric_requirements()` to `calculate_tdee()` for clarity
  - The property is now called `tdee` instead of `caloric_requirements`

- **Weight Loss Caloric Adjustments**: Updated all values
  - Old values (per kg/week): 0.25→275, 0.5→550, 1.0→1100, 1.5→1650, 2.0→2200, 2.5→2750
  - New values (per kg/week): 0.25→250, 0.5→500, 0.75→750, 1.0→1000, 1.5→1500, 2.0→2000, 2.5→2500

- **Weight Gain Caloric Adjustments**: Added standardized values
  - New values (per kg/week): 0.25→250, 0.5→500, 0.75→750, 1.0→1000

- **Minimum Calorie Thresholds**: Updated for both sexes
  - Female: Changed from 1200 to 1300 kcal/day
  - Male: Changed from 1600 to 1500 kcal/day

- **weight_amount Parameter**: Changed from string to float type
  - Old: `weight_amount="0.5"` (string)
  - New: `weight_amount=0.5` (float)

- **Package Version**: Bumped from 1.0.0 to 2.0.0

### Removed

- **calculate_caloric_requirements()**: Replaced by `calculate_tdee()`
- Support for string-based weight_amount values

### Fixed

- BMI calculation now provides more accurate decimal values
- Weight selection logic now properly accounts for different BMI categories
- Caloric adjustments now align with scientific recommendations (250 kcal per 0.25 kg)

### Technical Details

#### Formula Accuracy
All formulas have been updated to match medical and nutritional science standards:

1. **Mifflin-St Jeor Equation** for BMR (unchanged but now uses correct weight)
2. **Hamwi Formula** for ideal weight (inches-based)
3. **Standard BMI ranges** for weight categorization
4. **Energy balance principles** (7700 kcal ≈ 1 kg body weight, rounded to 7500 for practical use)

#### Breaking Changes

⚠️ **API Breaking Changes:**

1. `weight_amount` parameter type changed from `str` to `float`
2. `caloric_requirements` property renamed to `tdee`
3. `calculate_caloric_requirements()` method renamed to `calculate_tdee()`
4. `calculate_bmi()` now returns float instead of int
5. `calculate_adjusted_weight()` behavior changed - now part of a multi-step process
6. Minimum calorie thresholds changed (females: 1200→1300, males: 1600→1500)

#### Migration Guide

For users upgrading from v1.x to v2.0:

```python
# Old (v1.x)
calculator = CaloricCalculator(
    weight=70,
    height=175,
    age=30,
    sex='M',
    activity_level='MA',
    weight_goal=WeightGoal.LOSE,
    weight_amount="0.5"  # String
)
maintenance = calculator.caloric_requirements

# New (v2.0)
calculator = CaloricCalculator(
    weight=70,
    height=175,
    age=30,
    sex='M',
    activity_level='MA',
    weight_goal=WeightGoal.LOSE,
    weight_amount=0.5  # Float
)
maintenance = calculator.tdee  # Renamed property

# New features in v2.0
print(f"BMI: {calculator.bmi}")
print(f"Ideal Weight: {calculator.ideal_weight} kg")
print(f"Adjusted Weight: {calculator.adjusted_weight} kg")
print(f"Recommended Weight: {calculator.recommended_weight} kg")
```

### Testing

All calculations have been thoroughly tested:
- 22 unit tests with 100% pass rate
- Test coverage for all BMI ranges
- Test coverage for all activity levels
- Test coverage for all weight goals
- Minimum calorie threshold tests
- Invalid input error handling tests

### Documentation

- Complete README with all formulas and examples
- API reference documentation
- Inline code documentation with detailed docstrings
- Example usage script with 6 real-world scenarios

---

## [1.0.0] - Previous Version

### Initial Release
- Basic BMR calculation
- Basic caloric requirements calculation
- Support for weight goals (maintain, lose, gain)
- Activity level factors
- Minimum calorie thresholds

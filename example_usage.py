"""
Example usage of the Caloric Calculator package.
Demonstrates the updated formulas based on the specification document.
"""

from src.caloric_calculator import CaloricCalculator, WeightGoal


def print_calculator_results(calc, description):
    """Print detailed results from a calculator instance."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"\n📊 Input Parameters:")
    print(f"   Weight: {calc.weight} kg")
    print(f"   Height: {calc.height} cm")
    print(f"   Age: {calc.age} years")
    print(f"   Sex: {calc.sex}")
    print(f"   Activity Level: {calc.activity_level}")
    print(f"   Weight Goal: {calc.weight_goal.value}")
    print(f"   Target Change: {calc.weight_amount} kg/week")
    
    print(f"\n📈 Calculated Values:")
    print(f"   BMI: {calc.bmi}")
    print(f"   Ideal Weight: {calc.ideal_weight} kg")
    print(f"   Adjusted Weight: {calc.adjusted_weight} kg")
    print(f"   Recommended Weight (for BMR): {calc.recommended_weight} kg")
    print(f"   BMR: {calc.bmr} kcal/day")
    print(f"   Activity Factor: {calc.activity_factor}")
    print(f"   TDEE: {calc.tdee} kcal/day")
    
    print(f"\n🎯 Daily Caloric Needs: {calc.daily_caloric_needs} kcal/day")
    print(f"{'='*60}\n")


def main():
    """Run example calculations."""
    
    # Example 1: Male with normal BMI maintaining weight
    calc1 = CaloricCalculator(
        weight=70,
        height=175,
        age=30,
        sex="M",
        activity_level="MA",  # Moderately Active
        weight_goal=WeightGoal.MAINTAIN,
        weight_amount=0
    )
    print_calculator_results(calc1, "Example 1: Male, Normal BMI, Maintaining Weight")
    
    # Example 2: Female trying to lose weight
    calc2 = CaloricCalculator(
        weight=68,
        height=165,
        age=28,
        sex="F",
        activity_level="LA",  # Lightly Active
        weight_goal=WeightGoal.LOSE,
        weight_amount=0.5  # Lose 0.5 kg per week
    )
    print_calculator_results(calc2, "Example 2: Female, Weight Loss Goal (0.5 kg/week)")
    
    # Example 3: Male with overweight BMI trying to lose weight
    calc3 = CaloricCalculator(
        weight=85,
        height=175,
        age=35,
        sex="M",
        activity_level="S",  # Sedentary
        weight_goal=WeightGoal.LOSE,
        weight_amount=0.75  # Lose 0.75 kg per week
    )
    print_calculator_results(calc3, "Example 3: Male, Overweight, Weight Loss Goal (0.75 kg/week)")
    
    # Example 4: Male with obese BMI
    calc4 = CaloricCalculator(
        weight=100,
        height=175,
        age=40,
        sex="M",
        activity_level="MA",
        weight_goal=WeightGoal.LOSE,
        weight_amount=1.0  # Lose 1 kg per week
    )
    print_calculator_results(calc4, "Example 4: Male, Obese BMI, Weight Loss Goal (1 kg/week)")
    
    # Example 5: Male trying to gain weight
    calc5 = CaloricCalculator(
        weight=60,
        height=180,
        age=25,
        sex="M",
        activity_level="VA",  # Very Active
        weight_goal=WeightGoal.GAIN,
        weight_amount=0.5  # Gain 0.5 kg per week
    )
    print_calculator_results(calc5, "Example 5: Male, Underweight, Weight Gain Goal (0.5 kg/week)")
    
    # Example 6: Female with very low calorie scenario (testing minimum threshold)
    calc6 = CaloricCalculator(
        weight=45,
        height=150,
        age=20,
        sex="F",
        activity_level="S",  # Sedentary
        weight_goal=WeightGoal.LOSE,
        weight_amount=1.0  # Lose 1 kg per week
    )
    print_calculator_results(calc6, "Example 6: Female, Low Weight, Testing Minimum Calorie Threshold")
    
    print("\n✅ All examples completed successfully!")
    print("\nNote: The system enforces minimum safe calorie thresholds:")
    print("   • Females: minimum 1300 kcal/day")
    print("   • Males: minimum 1500 kcal/day")


if __name__ == "__main__":
    main()

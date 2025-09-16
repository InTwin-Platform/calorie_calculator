import unittest
from src.calculator import CaloricCalculator, WeightGoal


class TestCaloricCalculator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.calculator = CaloricCalculator(
            weight=70,
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.MAINTAIN,
            weight_amount="0.0",
        )

    def test_calculate_bmi(self):
        """Test BMI calculation."""
        bmi = self.calculator.calculate_bmi()
        expected_bmi = round(70 / (1.75**2))  # 70 / 3.0625 ≈ 23
        self.assertEqual(bmi, expected_bmi)

    def test_calculate_adjusted_weight_male(self):
        """Test adjusted weight calculation for male."""
        adjusted_weight = self.calculator.calculate_adjusted_weight()
        self.assertIsInstance(adjusted_weight, float)
        self.assertGreater(adjusted_weight, 0)

    def test_calculate_adjusted_weight_female(self):
        """Test adjusted weight calculation for female."""
        female_calc = CaloricCalculator(
            weight=60,
            height=165,
            age=25,
            sex="F",
            activity_level="LA",
            weight_goal=WeightGoal.MAINTAIN,
        )
        adjusted_weight = female_calc.calculate_adjusted_weight()
        self.assertIsInstance(adjusted_weight, float)
        self.assertGreater(adjusted_weight, 0)

    def test_calculate_bmr(self):
        """Test BMR calculation."""
        bmr = self.calculator.calculate_bmr()
        self.assertIsInstance(bmr, int)
        self.assertGreater(bmr, 1000)  # Reasonable BMR should be > 1000

    def test_get_activity_factor(self):
        """Test activity factor retrieval."""
        factor = self.calculator.get_activity_factor()
        self.assertEqual(factor, 1.55)  # MA = 1.55

    def test_invalid_activity_level(self):
        """Test invalid activity level raises error."""
        with self.assertRaises(ValueError):
            CaloricCalculator(
                weight=70,
                height=175,
                age=30,
                sex="M",
                activity_level="INVALID",
                weight_goal=WeightGoal.MAINTAIN,
            )

    def test_calculate_caloric_requirements(self):
        """Test caloric requirements calculation."""
        calories = self.calculator.calculate_caloric_requirements()
        self.assertIsInstance(calories, int)
        self.assertGreater(calories, 1500)  # Should be reasonable amount

    def test_calculate_daily_caloric_needs_maintain(self):
        """Test daily caloric needs for maintenance."""
        calories = self.calculator.calculate_daily_caloric_needs()
        expected = self.calculator.caloric_requirements
        self.assertEqual(calories, expected)

    def test_calculate_daily_caloric_needs_lose(self):
        """Test daily caloric needs for weight loss."""
        lose_calc = CaloricCalculator(
            weight=70,
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.LOSE,
            weight_amount="0.5",
        )
        calories = lose_calc.calculate_daily_caloric_needs()
        maintenance_calories = lose_calc.caloric_requirements
        self.assertLess(calories, maintenance_calories)

    def test_calculate_daily_caloric_needs_gain(self):
        """Test daily caloric needs for weight gain."""
        gain_calc = CaloricCalculator(
            weight=70,
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.GAIN,
            weight_amount="0.5",
        )
        calories = gain_calc.calculate_daily_caloric_needs()
        maintenance_calories = gain_calc.caloric_requirements
        self.assertGreater(calories, maintenance_calories)

    def test_minimum_calories_female(self):
        """Test minimum calorie limit for females."""
        low_calc = CaloricCalculator(
            weight=40,  # Very low weight to trigger minimum
            height=150,
            age=20,
            sex="F",
            activity_level="S",
            weight_goal=WeightGoal.LOSE,
            weight_amount="2.0",
        )
        calories = low_calc.calculate_daily_caloric_needs()
        self.assertGreaterEqual(calories, 1200)

    def test_minimum_calories_male(self):
        """Test minimum calorie limit for males."""
        low_calc = CaloricCalculator(
            weight=50,  # Low weight to trigger minimum
            height=160,
            age=20,
            sex="M",
            activity_level="S",
            weight_goal=WeightGoal.LOSE,
            weight_amount="2.0",
        )
        calories = low_calc.calculate_daily_caloric_needs()
        self.assertGreaterEqual(calories, 1600)


if __name__ == "__main__":
    unittest.main()

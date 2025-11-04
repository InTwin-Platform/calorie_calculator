import unittest
from src.caloric_calculator import CaloricCalculator, WeightGoal


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
            weight_amount=0.0,
        )

    def test_calculate_bmi(self):
        """Test BMI calculation."""
        bmi = self.calculator.calculate_bmi()
        expected_bmi = round(70 / (1.75**2), 2)  # 70 / 3.0625 ≈ 22.86
        self.assertEqual(bmi, expected_bmi)

    def test_calculate_ideal_weight_male(self):
        """Test ideal weight calculation for male."""
        # Height 175 cm = 68.9 inches
        # IW = 50 + 2.3 × (68.9 - 60) = 50 + 2.3 × 8.9 = 50 + 20.47 = 70.47
        ideal_weight = self.calculator.calculate_ideal_weight()
        self.assertIsInstance(ideal_weight, float)
        self.assertAlmostEqual(ideal_weight, 70.47, places=1)

    def test_calculate_ideal_weight_female(self):
        """Test ideal weight calculation for female."""
        female_calc = CaloricCalculator(
            weight=60,
            height=165,
            age=25,
            sex="F",
            activity_level="LA",
            weight_goal=WeightGoal.MAINTAIN,
        )
        # Height 165 cm = 64.96 inches
        # IW = 45.5 + 2.3 × (64.96 - 60) = 45.5 + 2.3 × 4.96 = 45.5 + 11.41 = 56.91
        ideal_weight = female_calc.calculate_ideal_weight()
        self.assertIsInstance(ideal_weight, float)
        self.assertAlmostEqual(ideal_weight, 56.91, places=1)

    def test_calculate_adjusted_weight(self):
        """Test adjusted weight calculation."""
        # For the default setup: IW ≈ 70.47, weight = 70
        # AW = IW + 0.25 × (70 - 70.47) = 70.47 + 0.25 × (-0.47) = 70.35
        adjusted_weight = self.calculator.calculate_adjusted_weight()
        self.assertIsInstance(adjusted_weight, float)
        self.assertGreater(adjusted_weight, 0)

    def test_get_recommended_weight_normal_bmi(self):
        """Test recommended weight for normal BMI (18.5-24.9)."""
        # BMI = 22.86 (normal range), should use actual weight
        recommended = self.calculator.get_recommended_weight()
        self.assertEqual(recommended, self.calculator.weight)

    def test_get_recommended_weight_overweight(self):
        """Test recommended weight for overweight BMI (25-29.9)."""
        overweight_calc = CaloricCalculator(
            weight=85,  # BMI ≈ 27.8
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.MAINTAIN,
        )
        recommended = overweight_calc.get_recommended_weight()
        self.assertEqual(recommended, overweight_calc.ideal_weight)

    def test_get_recommended_weight_obese(self):
        """Test recommended weight for obese BMI (>= 30)."""
        obese_calc = CaloricCalculator(
            weight=100,  # BMI ≈ 32.7
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.MAINTAIN,
        )
        recommended = obese_calc.get_recommended_weight()
        self.assertEqual(recommended, obese_calc.adjusted_weight)

    def test_get_recommended_weight_underweight(self):
        """Test recommended weight for underweight BMI (< 18.5)."""
        underweight_calc = CaloricCalculator(
            weight=55,  # BMI ≈ 18.0
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.MAINTAIN,
        )
        recommended = underweight_calc.get_recommended_weight()
        self.assertEqual(recommended, underweight_calc.weight)

    def test_calculate_bmr_male(self):
        """Test BMR calculation for male."""
        bmr = self.calculator.calculate_bmr()
        self.assertIsInstance(bmr, int)
        self.assertGreater(bmr, 1000)  # Reasonable BMR should be > 1000

    def test_calculate_bmr_female(self):
        """Test BMR calculation for female."""
        female_calc = CaloricCalculator(
            weight=60,
            height=165,
            age=25,
            sex="F",
            activity_level="LA",
            weight_goal=WeightGoal.MAINTAIN,
        )
        bmr = female_calc.calculate_bmr()
        self.assertIsInstance(bmr, int)
        self.assertGreater(bmr, 1000)

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

    def test_calculate_tdee(self):
        """Test TDEE calculation."""
        tdee = self.calculator.calculate_tdee()
        expected_tdee = round(self.calculator.bmr * 1.55)
        self.assertEqual(tdee, expected_tdee)

    def test_calculate_daily_caloric_needs_maintain(self):
        """Test daily caloric needs for maintenance."""
        calories = self.calculator.calculate_daily_caloric_needs()
        self.assertEqual(calories, self.calculator.tdee)

    def test_calculate_daily_caloric_needs_lose(self):
        """Test daily caloric needs for weight loss."""
        lose_calc = CaloricCalculator(
            weight=70,
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.LOSE,
            weight_amount=0.5,
        )
        calories = lose_calc.calculate_daily_caloric_needs()
        expected_calories = lose_calc.tdee - 500  # 0.5 kg/week = -500 kcal/day
        self.assertEqual(calories, round(expected_calories))

    def test_calculate_daily_caloric_needs_lose_multiple_rates(self):
        """Test daily caloric needs for different weight loss rates."""
        test_cases = [
            (0.25, 250),
            (0.5, 500),
            (0.75, 750),
            (1.0, 1000),
            (1.5, 1500),
            (2.0, 2000),
            (2.5, 2500),
        ]
        
        for weight_amount, expected_deficit in test_cases:
            with self.subTest(weight_amount=weight_amount):
                calc = CaloricCalculator(
                    weight=90,
                    height=175,
                    age=30,
                    sex="M",
                    activity_level="MA",
                    weight_goal=WeightGoal.LOSE,
                    weight_amount=weight_amount,
                )
                calories = calc.calculate_daily_caloric_needs()
                expected = max(calc.tdee - expected_deficit, 1500)  # Male minimum is 1500
                self.assertEqual(calories, round(expected))

    def test_calculate_daily_caloric_needs_gain(self):
        """Test daily caloric needs for weight gain."""
        gain_calc = CaloricCalculator(
            weight=70,
            height=175,
            age=30,
            sex="M",
            activity_level="MA",
            weight_goal=WeightGoal.GAIN,
            weight_amount=0.5,
        )
        calories = gain_calc.calculate_daily_caloric_needs()
        expected_calories = gain_calc.tdee + 500  # 0.5 kg/week = +500 kcal/day
        self.assertEqual(calories, round(expected_calories))

    def test_calculate_daily_caloric_needs_gain_multiple_rates(self):
        """Test daily caloric needs for different weight gain rates."""
        test_cases = [
            (0.25, 250),
            (0.5, 500),
            (0.75, 750),
            (1.0, 1000),
        ]
        
        for weight_amount, expected_surplus in test_cases:
            with self.subTest(weight_amount=weight_amount):
                calc = CaloricCalculator(
                    weight=70,
                    height=175,
                    age=30,
                    sex="M",
                    activity_level="MA",
                    weight_goal=WeightGoal.GAIN,
                    weight_amount=weight_amount,
                )
                calories = calc.calculate_daily_caloric_needs()
                expected = calc.tdee + expected_surplus
                self.assertEqual(calories, round(expected))

    def test_minimum_calories_female(self):
        """Test minimum calorie limit for females (1300 kcal)."""
        low_calc = CaloricCalculator(
            weight=45,
            height=150,
            age=20,
            sex="F",
            activity_level="S",
            weight_goal=WeightGoal.LOSE,
            weight_amount=2.0,
        )
        calories = low_calc.calculate_daily_caloric_needs()
        self.assertGreaterEqual(calories, 1300)

    def test_minimum_calories_male(self):
        """Test minimum calorie limit for males (1500 kcal)."""
        low_calc = CaloricCalculator(
            weight=55,
            height=160,
            age=20,
            sex="M",
            activity_level="S",
            weight_goal=WeightGoal.LOSE,
            weight_amount=2.0,
        )
        calories = low_calc.calculate_daily_caloric_needs()
        self.assertGreaterEqual(calories, 1500)

    def test_all_activity_levels(self):
        """Test all activity levels work correctly."""
        activity_levels = {
            "S": 1.2,
            "LA": 1.375,
            "MA": 1.55,
            "VA": 1.725,
            "SA": 1.9,
        }
        
        for level, factor in activity_levels.items():
            with self.subTest(activity_level=level):
                calc = CaloricCalculator(
                    weight=70,
                    height=175,
                    age=30,
                    sex="M",
                    activity_level=level,
                    weight_goal=WeightGoal.MAINTAIN,
                )
                self.assertEqual(calc.activity_factor, factor)

    def test_invalid_sex(self):
        """Test invalid sex raises error."""
        with self.assertRaises(ValueError):
            CaloricCalculator(
                weight=70,
                height=175,
                age=30,
                sex="X",
                activity_level="MA",
                weight_goal=WeightGoal.MAINTAIN,
            )


if __name__ == "__main__":
    unittest.main()

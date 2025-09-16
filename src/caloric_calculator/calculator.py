from .models import WeightGoal


class CaloricCalculator:
    def __init__(
        self, weight, height, age, sex, activity_level, weight_goal, weight_amount="0.0"
    ):
        """
        Initialize the Caloric Calculator.

        Args:
            weight (float): Weight in kg
            height (float): Height in cm
            age (int): Age in years
            sex (str): 'M' for male, 'F' for female
            activity_level (str): 'S', 'LA', 'MA', 'VA', 'SA'
            weight_goal (WeightGoal): Weight goal enum
            weight_amount (str): Amount to lose/gain per week in kg
        """
        self.weight = weight
        self.height = height
        self.age = age
        self.sex = sex.upper()
        self.activity_level = activity_level.upper()
        self.weight_goal = weight_goal
        self.weight_amount = str(weight_amount)

        # Calculate derived values
        self.adjusted_weight = self.calculate_adjusted_weight()
        self.bmr = self.calculate_bmr()
        self.activity_factor = self.get_activity_factor()
        self.caloric_requirements = self.calculate_caloric_requirements()

    def calculate_bmi(self):
        # Convert height from centimeters to meters
        height_m = self.height / 100
        # Calculate BMI using the formula
        return round(self.weight / (height_m**2))

    def calculate_adjusted_weight(self):
        """
        Calculate the ideal and adjusted weights and return the appropriate weight based on the condition.

        Returns:
            float: The ideal weight or the adjusted weight based on the condition.
        """
        # Calculate Ideal Weight (IW) using height in cm
        if self.sex == "M":
            ideal_weight = 50 + 0.9 * (self.height - 152.4)
        elif self.sex == "F":
            ideal_weight = 45.5 + 0.9 * (self.height - 152.4)
        else:
            raise ValueError("Invalid gender. Please specify 'M' or 'F'.")

        # Calculate Adjusted Weight (AW)
        adjusted_weight = ideal_weight + 0.4 * (self.weight - ideal_weight)

        # Determine which weight to return
        if ideal_weight >= 0.7 * self.weight:
            return round(ideal_weight, 2)
        else:
            return round(adjusted_weight, 2)

    def calculate_bmr(self):
        if self.sex == "M":
            # For men:
            bmr = (
                (10 * self.adjusted_weight) + (6.25 * self.height) - (5 * self.age) + 5
            )
        elif self.sex == "F":
            # For women:
            bmr = (
                (10 * self.adjusted_weight)
                + (6.25 * self.height)
                - (5 * self.age)
                - 161
            )
        return round(bmr)

    def get_activity_factor(self):
        activity_factors = {"S": 1.2, "LA": 1.375, "MA": 1.55, "VA": 1.725, "SA": 1.9}
        activity_factor = activity_factors.get(self.activity_level, None)
        if activity_factor is None:
            raise ValueError(f"Invalid activity level: {self.activity_level}")
        return activity_factor

    def calculate_caloric_requirements(self):
        """
        This function calculates the adjusted Basal Metabolic Rate (BMR)
        by multiplying the initial BMR with the activity factor.
        """
        caloric_requirements = self.bmr * self.activity_factor
        return round(caloric_requirements)

    def calculate_daily_caloric_needs(self):
        """
        This function calculates the daily caloric intake required to reach a specific weight goal
        (maintain, lose, or gain weight) based on the adjusted BMR and the desired weight change.
        """
        calorie_deficit_per_kg_loss = {
            "0.0": 0,
            "0.25": 275.00,
            "0.45": 495.00,
            "0.5": 550.00,
            "1.0": 1100.00,
            "1.5": 1650.00,
            "2.0": 2200.00,
            "2.5": 2750.00,
            "3.0": 3300.00,
        }

        # Determine the weight goal value (caloric change per week) based on weight amount to lose/gain per week
        weight_goal_value = calorie_deficit_per_kg_loss.get(self.weight_amount, 0)

        # Calculate desired daily caloric intake based on weight goal
        if self.weight_goal == WeightGoal.MAINTAIN:
            return round(self.caloric_requirements)
        elif self.weight_goal == WeightGoal.LOSE:
            desired_daily_calories = self.caloric_requirements - weight_goal_value
        elif self.weight_goal == WeightGoal.GAIN:
            desired_daily_calories = self.caloric_requirements + weight_goal_value
        else:
            raise ValueError(
                "Invalid weight goal specified. Choose from WeightGoal enum values."
            )

        if self.sex == "F":
            desired_daily_calories = max(desired_daily_calories, 1200)
        elif self.sex == "M":
            desired_daily_calories = max(desired_daily_calories, 1600)

        return round(desired_daily_calories)

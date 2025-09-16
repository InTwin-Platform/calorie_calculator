class WeightGoal:
    MAINTAIN = "maintain"
    LOSE = "lose"
    GAIN = "gain"


def calculate_bmi(self):
    # Convert height from centimeters to meters
    height_m = self.height / 100
    # Calculate BMI using the formula
    return round(self.weight / (height_m**2))


def calculate_adjusted_weight(self):
    """
    Calculate the ideal and adjusted weights and return the appropriate weight based on the condition.

    Parameters:
    actual_weight (float): The patient's actual weight in kilograms.
    height_cm (float): The patient's height in centimeters.
    gender (str): The patient's gender ('male' or 'female').

    Returns:
    float: The ideal weight or the adjusted weight based on the condition.
    """
    # Calculate Ideal Weight (IW) using height in cm
    if self.sex == "M":
        ideal_weight = 50 + 0.9 * (self.height - 152.4)
    elif self.sex == "F":
        ideal_weight = 45.5 + 0.9 * (self.height - 152.4)
    else:
        raise ValueError("Invalid gender. Please specify 'male' or 'female'.")

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
        bmr = (10 * self.adjusted_weight) + (6.25 * self.height) - (5 * self.age) + 5
    elif self.sex == "F":
        # For women:
        bmr = (10 * self.adjusted_weight) + (6.25 * self.height) - (5 * self.age) - 161
    print("bmr:", bmr)
    return round(bmr)


def get_activity_factor(self):
    activity_factors = {"S": 1.2, "LA": 1.375, "MA": 1.55, "VA": 1.725, "SA": 1.9}
    activity_factor = activity_factors.get(self.activity_level, None)
    return activity_factor


def calculate_caloric_requirements(self):
    """
    This function calculates the adjusted Basal Metabolic Rate (BMR)
    by multiplyi[bng the initial BMR with the activity factor.
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
            "Invalid weight goal specified. Choose from 'maintain', 'lose', or 'gain'."
        )

    if self.sex == "F":
        desired_daily_calories = max(desired_daily_calories, 1200)
    elif self.sex == "M":
        desired_daily_calories = max(desired_daily_calories, 1600)

    return round(desired_daily_calories)

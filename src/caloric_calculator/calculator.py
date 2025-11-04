from .models import WeightGoal


class CaloricCalculator:
    def __init__(
        self, weight, height, age, sex, activity_level, weight_goal, weight_amount=0.0
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
            weight_amount (float): Amount to lose/gain per week in kg
        """
        self.weight = weight
        self.height = height
        self.age = age
        self.sex = sex.upper()
        self.activity_level = activity_level.upper()
        self.weight_goal = weight_goal
        self.weight_amount = float(weight_amount)

        # Calculate derived values
        self.bmi = self.calculate_bmi()
        self.ideal_weight = self.calculate_ideal_weight()
        self.adjusted_weight = self.calculate_adjusted_weight()
        self.recommended_weight = self.get_recommended_weight()
        self.bmr = self.calculate_bmr()
        self.activity_factor = self.get_activity_factor()
        self.tdee = self.calculate_tdee()
        self.daily_caloric_needs = self.calculate_daily_caloric_needs()
        
        # Backward compatibility alias
        self.caloric_requirements = self.tdee

    def calculate_bmi(self):
        """
        Calculate Body Mass Index (BMI).
        BMI = Weight (kg) / (Height (m))²
        
        Returns:
            float: BMI value rounded to 2 decimal places
        """
        height_m = self.height / 100
        return round(self.weight / (height_m ** 2), 2)

    def calculate_ideal_weight(self):
        """
        Calculate Ideal Weight (IW) using height in inches.
        For Males: IW = 50 + 2.3 × (Height (inches) - 60)
        For Females: IW = 45.5 + 2.3 × (Height (inches) - 60)
        
        Returns:
            float: Ideal weight in kg, rounded to 2 decimal places
        """
        # Convert height from cm to inches (1 inch = 2.54 cm)
        height_inches = self.height / 2.54
        
        if self.sex == "M":
            ideal_weight = 50 + 2.3 * (height_inches - 60)
        elif self.sex == "F":
            ideal_weight = 45.5 + 2.3 * (height_inches - 60)
        else:
            raise ValueError("Invalid gender. Please specify 'M' or 'F'.")
        
        return round(ideal_weight, 2)

    def calculate_adjusted_weight(self):
        """
        Calculate Adjusted Weight (AW).
        AW = IW + 0.25 × (Actual Weight - IW)
        
        Returns:
            float: Adjusted weight in kg, rounded to 2 decimal places
        """
        adjusted_weight = self.ideal_weight + 0.25 * (self.weight - self.ideal_weight)
        return round(adjusted_weight, 2)

    def get_recommended_weight(self):
        """
        Determine the recommended weight for calorie calculations based on BMI.
        
        BMI Range          | Weight Used
        < 18.5            | Actual Weight
        18.5 - 24.9       | Actual Weight
        >= 25 - 29.9      | Ideal Weight
        >= 30             | Adjusted Weight
        
        Returns:
            float: Recommended weight for calculations
        """
        if self.bmi < 18.5:
            return self.weight
        elif 18.5 <= self.bmi <= 24.9:
            return self.weight
        elif 25 <= self.bmi <= 29.9:
            return self.ideal_weight
        else:  # BMI >= 30
            return self.adjusted_weight

    def calculate_bmr(self):
        """
        Calculate Basal Metabolic Rate (BMR) using the recommended weight.
        For Males: BMR = (10 × W(kg)) + (6.25 × Height (cm)) - (5 × Age(y)) + 5
        For Females: BMR = (10 × W(kg)) + (6.25 × Height (cm)) - (5 × Age(y)) - 161
        
        Returns:
            int: BMR in kcal/day, rounded to nearest integer
        """
        weight_for_bmr = self.recommended_weight
        
        if self.sex == "M":
            bmr = (10 * weight_for_bmr) + (6.25 * self.height) - (5 * self.age) + 5
        elif self.sex == "F":
            bmr = (10 * weight_for_bmr) + (6.25 * self.height) - (5 * self.age) - 161
        else:
            raise ValueError("Invalid gender. Please specify 'M' or 'F'.")
        
        return round(bmr)

    def get_activity_factor(self):
        """
        Get the Activity Factor (AF) based on activity level.
        
        Activity Level | Code | Factor
        Sedentary      | S    | 1.2
        Lightly Active | LA   | 1.375
        Moderately Active | MA | 1.55
        Very Active    | VA   | 1.725
        Super Active   | SA   | 1.9
        
        Returns:
            float: Activity factor
        """
        activity_factors = {
            "S": 1.2,
            "LA": 1.375,
            "MA": 1.55,
            "VA": 1.725,
            "SA": 1.9
        }
        activity_factor = activity_factors.get(self.activity_level, None)
        if activity_factor is None:
            raise ValueError(f"Invalid activity level: {self.activity_level}")
        return activity_factor

    def calculate_tdee(self):
        """
        Calculate Total Daily Energy Expenditure (TDEE).
        TDEE = BMR × AF
        
        Returns:
            int: TDEE in kcal/day, rounded to nearest integer
        """
        tdee = self.bmr * self.activity_factor
        return round(tdee)
    
    def calculate_caloric_requirements(self):
        """
        Backward compatibility alias for calculate_tdee().
        
        .. deprecated:: 2.0.0
           Use :func:`calculate_tdee` instead.
        
        Returns:
            int: TDEE in kcal/day, rounded to nearest integer
        """
        return self.calculate_tdee()

    def calculate_daily_caloric_needs(self):
        """
        Calculate Daily Caloric Needs (DCN) based on weight goal.
        
        - Maintain Weight = TDEE
        - Lose Weight = TDEE - Caloric Adjustment kcal/day
        - Gain Weight = TDEE + Caloric Adjustment kcal/day
        
        Minimum safe thresholds are enforced:
        - Female: 1300 kcal/day
        - Male: 1500 kcal/day
        
        Returns:
            int: Daily caloric needs in kcal/day, rounded to nearest integer
        """
        # Caloric adjustments for weight loss (kcal/day)
        weight_loss_adjustments = {
            0.25: 250,
            0.5: 500,
            0.75: 750,
            1.0: 1000,
            1.5: 1500,
            2.0: 2000,
            2.5: 2500
        }
        
        # Caloric adjustments for weight gain (kcal/day)
        weight_gain_adjustments = {
            0.25: 250,
            0.5: 500,
            0.75: 750,
            1.0: 1000
        }
        
        # Calculate desired daily caloric intake based on weight goal
        if self.weight_goal == WeightGoal.MAINTAIN:
            daily_calories = self.tdee
        elif self.weight_goal == WeightGoal.LOSE:
            adjustment = weight_loss_adjustments.get(self.weight_amount, 0)
            daily_calories = self.tdee - adjustment
        elif self.weight_goal == WeightGoal.GAIN:
            adjustment = weight_gain_adjustments.get(self.weight_amount, 0)
            daily_calories = self.tdee + adjustment
        else:
            raise ValueError(
                "Invalid weight goal specified. Choose from WeightGoal enum values."
            )
        
        # Enforce minimum safe calorie thresholds
        if self.sex == "F":
            daily_calories = max(daily_calories, 1300)
        elif self.sex == "M":
            daily_calories = max(daily_calories, 1500)
        
        return round(daily_calories)

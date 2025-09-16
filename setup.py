from setuptools import setup, find_packages

setup(
    name="calorie-calculator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    author="InTwin",
    author_email="intixel.intwin@gmail.com",
    description="Caloric needs calculator",
    python_requires=">=3.7",
    url="https://github.com/InTwin-Platform/calorie_calculator.git",
)

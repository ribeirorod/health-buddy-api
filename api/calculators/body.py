from typing import Optional
from math import pow


class BODY:

    factor = {0: 1.2, 1: 1.375, 2: 1.55, 3: 1.725, 4: 1.9, 5: 2.3}

    def __init__(
        self, 
        weight: float, 
        height: int, 
        age: int, 
        sex: int, 
        activity: Optional[int], 
        lbp: Optional[int]
    ) -> None:

        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height
        self.activity = activity
        self.lbm = weight * (lbp / 100)

    def _harris_benedict(self) -> float:
        """
        For men:   BMR = 10 x weight (kg) + 6.25 x height (cm) – 5 x age (years) + 5
        For women: BMR = 10 x weight (kg) + 6.25 x height (cm) – 5 x age (years) – 161
        """
        sexFactor = 5 if self.sex else -161
        return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + sexFactor

    def _katch_mcArdle(self) -> float:
        "Katch = 370 + (21.6 * LBM)"
        return 370 + (21.6 * self.lbm)

    @property
    def bmr(self) -> float:
        method = self._katch_mcArdle() if self.lbm else self._harris_benedict()
        return method

    @property
    def tee(self):
        "Total Energy Expenditure per Day"
        return __class__.factor[self.activity] * self.bmr

    @property
    def bmi(self):
        "To be used on non-muscular body types"
        "< 18.5 Underweight, 18.5 -25 Normal Range, 25-30 Overwieght, 30-hi Obese"
        "BMI Prime = BMI / 25"
        "BMI = weight / height² - weight in kilograms and height in meters"
        return self.weight / pow(self.height/100, 2)

    @property
    def ffmi(self):
        """
        FFMI score	Muscle mass interpretation
        16 - 17	Below average
        18 - 19	Average
        20 - 21	Above average
        22	Excellent
        23 -25	Superior
        26 - 27	Suspicion of steroid use*
        28 - 30	Steroid usage likely**
        FFMI = (Lean Weight in Kg / 2.2) * 2.20462 / ( height in meters) 2
        """
        "Better measure than BMI for bodybuilders"
        """
        Fat-Free Mass Index. It describes the amount of your muscle mass in relation to height and weight.
        """
        return self.lbm/pow(self.height/100,2)

    def adffmi(self):
        """
        For Normalized FFMI use the equation: 
        normalized FFMI = FFMI [kg/m²] + 6.1 * (1.8 - height [m]). 
        The same unit as in FFMI [kg/m²].
        """
        return self.ffmi + (6.1 * (1.8 - self.height/100))
    
    def ajbw(self):
        """
        It is especially useful when the patient is overweight or obese. 
        As adipose tissue is less metabolically active than lean tissue, 
        using actual body weight for calculating one's energy requirements 
        might result in some overestimations for people above their healthy BMI. 
        Hence, it's often recommended to use AjBW instead."""

        """ Ideal Body Weight 
            for men: 52 kg + 1.9 kg per every inch over 5 feet
            for women: 49 kg + 1.7 kg per every inch over 5 feet
            1 inch = 2.54cm  5 feet = 152cm 
        """
        inches = (self.height - 152) // 2.5 if self.height - 152 > 0 else 0
        if self.sex:
            ibw = 52 + (1.9 * inches)
        else:
             ibw = 47 + (1.7 * inches)

        # AjBW = IBW + 0.4 * (ABW - IBW)
        return ibw + 0.4 * (self.weight - ibw)
    
    def absi(self):
        """ 
            WC in meters, Heigh in m and BMI in kg/m²

            ABSI = WC  / (pow(BMI, 2/3) * pow(height,1/2))

            ABSI z score = (ABSI - ABSImean) / ABSISD

        """


# https://www.omnicalculator.com/health/a-body-shape-index
# https://www.omnicalculator.com/health/ffmi
# https://www.omnicalculator.com/health/calorie-deficit
# https://www.omnicalculator.com/health/adjusted-weight
# https://www.omnicalculator.com/health/pregnancy-weight-gain


class Nutrition(BODY):
    def __init__(self, **kwargs) -> None:
        super.__init__(**kwargs)

    def sugar(self):
        """
        There are four calories in one gram, so if a product has 15 grams of sugar per serving,
        that’s 60 calories just from the sugar alone, not counting the other ingredients.

        For most American women, that’s no more than 100 calories per day,
        or about 6 teaspoons of sugar. For men, it’s 150 calories per day, or about 9 teaspoons.
        The AHA recommendations focus on all added sugars, without singling out any particular types such as high-fructose corn syrup.
        https://www.heart.org/en/healthy-living/healthy-eating/eat-smart/sugar/added-sugars
        """

    # https://www.omnicalculator.com/health/sugar-intake
    # https://www.omnicalculator.com/health/fiber
    # https://www.omnicalculator.com/health/keto#how-to-use-this-free-keto-calculator

    # Micronutrients calculator
    # https://www.ncbi.nlm.nih.gov/books/NBK545442/table/appJ_tab3/?report=objectonly

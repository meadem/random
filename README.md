# Income Comparison
This allows for the user to obtain a quick and dirty comparison of incomes in different locations in the U.S. This can help to illustrate situations where a position with a lower pay band is actually more favorable due to, e.g., reduced local cost-of-living. 

In an attempt to increase the accuracy of the comparison, the user's expenses are defined in two categories, or buckets: a) 'flex' expenses, such as groceries, rent, and other expenses that can be expected to differ between locations, and b) 'fixed' expenses, such as loan repayments, child support payments, and other expenses that can be reasonably expected to remain the same regardless of location. **The flex expenses are adjusted for COL, while the fixed expenses are not.**

Currently, the following states are available: OR, WA, CA, WI, CT

Taken into account for the comparison are:
- monetary compensation
- state income tax (filing Single only, for now) 
- local cost-of-living (using the [Forbes 2025 Cost of Living Calculator](https://www.forbes.com/advisor/mortgages/real-estate/cost-of-living-calculator/))
-----------------------------

After the package is imported, we need to define the following: 
- current income (or other income to be compared)
- current state
- monthly flex expenses
- monthly fixed expenses

```python
from income_comparison import income_comparison as compare

CURRENT_INCOME = 100000
CURRENT_STATE = "CA"
FLEX_EXPENSES_MONTHLY = 4650
FIXED_EXPENSES_MONTHLY = 2030

# Note to self: the calculation of yearly expenses should be moved into the code, since most people are more likely to have a picture of monthly expenses than yearly expenses, which can then be easily calculated as here.
FLEX_EXPENSES_YEARLY = 12 * FLEX_EXPENSES_MONTHLY
FIXED_EXPENSES_YEARLY = 12 * FIXED_EXPENSES_MONTHLY
```

Next we define the offer:

```python
OFFER = 60000
STATE = "WA"
COL_DIFFERENCE = -00.10     # value obtained from the Forbes Cost-of-Living Calculator
                            # if new location has 10% lower COL, then this value should be -0.10, as it is here.
```

The last variable represents the cost-of-living difference between the two locations, as pulled from the [Forbes Cost-of-Living Calculator](https://www.forbes.com/advisor/mortgages/real-estate/cost-of-living-calculator/) and formatted as a decimal percent value. I would love it if the code could pull this value automatically in the future. Maybe Forbes has some kind of API?..

Now the offers can be compared by calling compare() like this:

```python
prospect = compare(OFFER, STATE, COL_DIFFERENCE, 
                         CURRENT_INCOME, CURRENT_STATE,
                         FIXED_EXPENSES_YEARLY, FLEX_EXPENSES_YEARLY)

prospect.report()
```

Which produces the following print-out. AIF is Adjusted Income Factor, a term that I made up so I could store and retrieve the quantitative estimate of the comparison.

**Also note the last line, which shows the most important result, the change in effective take-home cash.**

![image](https://github.com/user-attachments/assets/b4caa0b8-1523-4ba9-8909-4a9145adda1c)

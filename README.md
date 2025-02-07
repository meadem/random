# Income Comparison
This allows for the user to obtain a quick and dirty comparison of incomes in different locations in the U.S. This can help to illustrate situations where a position with a lower pay band is actually more favorable due to, e.g., reduced local cost-of-living. 

In an attempt to increase the accuracy of the comparison, the user's expenses are defined in two categories, or buckets: a) 'flex' expenses, such as groceries, rent, and other expenses that can be expected to differ between locations, and b) 'fixed' expenses, such as loan repayments, child support payments, and other expenses that can be reasonably expected to remain the same regardless of location. **The flex expenses are adjusted for COL, while the fixed expenses are not.**

Currently, the following states are available: OR, WA, CA, WI, CT

Taken into account for the comparison are:
- monetary compensation
- state income tax (filing Single is the only available option, for now) 
- local cost-of-living (using the [Forbes 2025 Cost of Living Calculator](https://www.forbes.com/advisor/mortgages/real-estate/cost-of-living-calculator/))
-----------------------------

After the package is imported, we instantiate an Income Comparison object by passing it some information about your current job position: 

```python
from income_comparison import income_comparison


prospects = income_comparison(current_income = 116500,  # current position
                         current_state = 'CA',          # Oakland, CA
                         fixed_expenses_monthly = 2030, 
                         flex_expenses_monthly = 4650
                        )
```


Next we define any offers we have, real or hypothetical:

```python
prospects.compare(id='offer 1', 
             state='WA', 
             payment=80000, 
             COL_difference=-00.41  # Richland, WA
            )

prospects.compare(id='offer 2', 
             state='CT', 
             payment=110000, 
             COL_difference=-00.28 # New Haven, CT
            )

prospects.compare(id='offer 3', 
             state='WI', 
             payment=100000,
             COL_difference=-00.38  # Milwaukee, WI
            )

prospects.compare(id='offer 4', 
             state='CA', 
             payment=130000,
             COL_difference=00.23  # San Jose, CA
            )
```


The last variable passed to each offer instance represents the cost-of-living difference between the two locations, as pulled from the [Forbes Cost-of-Living Calculator](https://www.forbes.com/advisor/mortgages/real-estate/cost-of-living-calculator/) and formatted as a decimal percent value. I would love it if the code could pull this value automatically in the future. Maybe Forbes has some kind of API?..

Now we can print out a table summarizing everything like this:

```python
prospects.report()
```


Which produces the following print-out: 

![image](https://github.com/user-attachments/assets/1774978e-f0cc-4492-8eb3-85cae506d6b9)


(AIF is Adjusted Income Factor, a term that I made up that represents tax-adjusted income divided by COL-adjusted expenses.)

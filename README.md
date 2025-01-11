from income_comparison import income_comparison as compare

CURRENT_INCOME = 100000
CURRENT_STATE = "CA"

CURRENT_FLEX_EXPENSES_MONTHLY = 4650
CURRENT_FLEX_EXPENSES_YEARLY = 12 * CURRENT_FLEX_EXPENSES_MONTHLY

FIXED_EXPENSES_MONTHLY = 2030
FIXED_EXPENSES_YEARLY = 12 * FIXED_EXPENSES_MONTHLY


## Offer 1
OFFER = 80000
STATE = "WA"
COL_difference = -00.41       # Richland, WA

prospect = compare(OFFER, STATE, COL_difference, 
                         CURRENT_INCOME, CURRENT_STATE,
                         FIXED_EXPENSES_YEARLY, CURRENT_FLEX_EXPENSES_YEARLY)

prospect.report()


# Offer 2
OFFER = 110000
STATE = "CT"
COL_difference = -00.28       # New Haven, CT

prospect = compare(OFFER, STATE, COL_difference, 
                         CURRENT_INCOME, CURRENT_STATE,
                         FIXED_EXPENSES_YEARLY, CURRENT_FLEX_EXPENSES_YEARLY)

prospect.report()


# Offer 3
OFFER = 110000
STATE = "WI"
COL_difference = -00.38       # Milwaukee, WI

prospect = compare(OFFER, STATE, COL_difference, 
                         CURRENT_INCOME, CURRENT_STATE,
                         FIXED_EXPENSES, CURRENT_FLEX_EXPENSES)

prospect.report()

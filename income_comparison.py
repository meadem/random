import numpy as np
import matplotlib.pyplot as plt


'''
To do:
 - Add other detuctions? social security deduction? others?
 - write match() method for determining income required in a new location to reach disposable income parity with current income and location.
'''


class income_comparison():
    '''
    Compare job offers across U.S. locations by taking into account gross income, local cost-of-living, and state and federal taxes.
    '''

    def __init__(self, 
                 current_state=None, 
                 current_income=None, 
                 fixed_expenses_monthly=None, 
                 flex_expenses_monthly=None
                 ):
        
        self.offers = {}
        self.offers['Current'] = {}
        self.offers['Current']['State'] = current_state
        self.offers['Current']['Payment'] = current_income
        self.offers['Current']['Fixed Expenses'] = fixed_expenses_monthly * 12
        self.offers['Current']['Flex Expenses'] = flex_expenses_monthly * 12
        self.offers['Current']['Total Expenses'] = self.offers['Current']['Fixed Expenses'] + self.offers['Current']['Flex Expenses']
        
        # Calculate current AIF
        self.calculate_adjusted_income_factor('Current')
    
    def calculate_adjusted_income_factor(self, id):
        '''
        Calculate Adjusted Income Factor (AIF) as tax-adjusted income divided by COL-adjusted expenses.
        '''
        if id is None:
            return print("ERROR: Offer id is required to store AIF value.")
        
        state = self.offers[id]['State']
        income = self.offers[id]['Payment']
        expenses = self.offers[id]['Total Expenses']  # these should already be COL-adjusted

        federal_tax_burden = self.federal_tax_burden(id)
        state_tax_burden = self.state_tax_burden(id)
        tax_burden = federal_tax_burden + state_tax_burden
        tax_adjusted_income = income - tax_burden
        AIF = tax_adjusted_income / expenses

        self.offers[id]['Federal Tax Burden'] = federal_tax_burden
        self.offers[id]['State Tax Burden'] = state_tax_burden
        self.offers[id]['Tax Burden'] = tax_burden
        self.offers[id]['Tax Adjusted Income'] = tax_adjusted_income
        self.offers[id]['Monthly Disposable Income'] = (tax_adjusted_income - expenses)/12
        self.offers[id]['AIF'] = AIF
    
    def COL_adjusted_expenses(self, id):
        '''
        Apply Cost-of-Living difference to expenses for the specified offer.
        '''
        
        fixed_expenses = self.offers['Current']['Fixed Expenses']
        flex_expenses = self.offers['Current']['Flex Expenses']
        COL_difference = self.offers[id]['COL Difference']
        adjusted_flex_expenses = flex_expenses * ( 1 + COL_difference )
        result = fixed_expenses + adjusted_flex_expenses
        return result

    def compare(self, id=None, state=None, payment=None,  COL_difference=None):
        '''
        Register an offer for comparison against the null offer.
        NOTE: COL_difference should be provided as a percent difference, e.g., -0.10 for a payment offer 10% less than current income.
        '''
        
        self.offers[id] = {}
        self.offers[id]['State'] = state
        self.offers[id]['Payment'] = payment
        self.offers[id]['COL Difference'] = COL_difference
        self.offers[id]['Total Expenses'] = self.COL_adjusted_expenses(id)

        # Calculate prospective AIF
        self.calculate_adjusted_income_factor(id)
    
    def federal_tax_burden(self, id, status="single"):
        """
        For 2025. Does not provide accuracte values for incomes of $1,000,000+.
        """

        income = self.offers[id]['Payment']
        result = 0.0

        brackets = {
                    1:[0,11926,0.10],
                    2:[11926,48476,0.12],
                    3:[48476,103351,0.22],
                    4:[103351,197301,0.24],
                    5:[197301,250526,0.32],
                    6:[250526,626351,0.35],
                    7:[626351,1e6,0.37]
        }

        if status == "single":

            for bracket in brackets.values():

                lower_bracket_boundary = bracket[0]
                upper_bracket_boundary = bracket[1]
                bracket_rate = bracket[2]

                if income >= upper_bracket_boundary:
                    result += bracket_rate * ( upper_bracket_boundary - lower_bracket_boundary )

                elif income < upper_bracket_boundary:
                    result += bracket_rate * ( income - lower_bracket_boundary )
                    break

                else:
                    raise ValueError("Something went wrong...")

        else:
            raise NameError("Filing status '" + status + "' was not found. Only 'single' is enabled at this time.")

        return result

    def match(self, state, COL_difference):
        '''
        Returns the offer amount required to match the current spending cash (i.e., disposable income parity).
        use  self.offers[id]['Monthly Disposable Income']
        '''

    def report(self):
        '''
        Print a summary of the offers and how they compare.
        '''
        
        # print table header
        print('%-30s%-15s%-15s%-15s%-15s%-15s%-15s' 
              % 
              (' ',  
               'STATE', 
               'NET INCOME', 
               'EXPENSES',
               'DISP. INCOME', 
               '<-- CHANGE', 
               'AIF'
               ))
        print('%-30s%-15s%-15s%-15s%-15s%-15s%-15s' 
              % 
              ('------------------------------', 
               '---------------', 
               '---------------', 
               '---------------', 
               '---------------', 
               '---------------', 
               '---------------'
               ))
        
        # print table entries
        for offer in self.offers:
            disposable_delta = self.offers[offer]['Monthly Disposable Income'] - self.offers['Current']['Monthly Disposable Income']
            print('%-30s%-15s%-15s%-15s%-15s%-15s%-15s' 
                  % 
                  (offer, 
                   self.offers[offer]['State'], 
                   f"${self.offers[offer]['Tax Adjusted Income']:.2f}", 
                   f"${self.offers[offer]['Total Expenses']:.2f}", 
                   f"${self.offers[offer]['Monthly Disposable Income']:.2f}", 
                   f"${disposable_delta:.2f}", 
                   f"{self.offers[offer]['AIF']:.2f}"
                   ))
    
    def state_tax_burden(self, id, status="single"):
        """
        For 2025. May not provide accurate values for incomes of $1,000,000+.
        """

        state = self.offers[id]['State']
        income = self.offers[id]['Payment']
        result = 0.0
        
        # Tax brackets by state
        brackets = {
                    "CA":{
                          1:[0,10757,0.01],
                          2:[10757,25500,0.02],
                          3:[25500,40246,0.04],
                          4:[40246,55867,0.06],
                          5:[55867,70607,0.08],
                          6:[70607,360660,0.093],
                          7:[360660,432788,0.103],
                          8:[432788,721315,0.113],
                          9:[721315,1e6,0.123],
                        },
                    "CT":{
                          1:[0,10000,0.02],
                          2:[10000,50000,0.045],
                          3:[50000,100000,0.055],
                          4:[100000,200000,0.06],
                          5:[200000,250000,0.065],
                          6:[250000,500000,0.069],
                          7:[500000,1e6,0.0699],
                        },
                    "OR":{
                          1:[0,4300,0.0475],
                          2:[4300,10750,0.0675],
                          3:[10750,125000,0.0875],
                          4:[125000,1e6,0.099],
                        },
                    "WA":{
                          1:[0,1e6,0],
                        },
                    "WI":{
                          1:[0,14320,0.035],
                          2:[14320,28640,0.044],
                          3:[28640,315310,0.053],
                          4:[315310,1e6,0.0765],
                        }
        }

        if status == "single":

            #for state_ in brackets.keys():

                try:
                    if state in brackets:
                        for bracket in brackets[state].values():

                            lower_bracket_boundary = bracket[0]
                            upper_bracket_boundary = bracket[1]
                            bracket_rate = bracket[2]

                            if income >= upper_bracket_boundary:
                                result += bracket_rate * ( upper_bracket_boundary - lower_bracket_boundary )

                            elif income < upper_bracket_boundary:
                                result += bracket_rate * ( income - lower_bracket_boundary )
                                break

                            else:
                                raise ValueError("Something went wrong...")

                except:
                    raise NameError("State not found.")

        else:
            raise NameError("Filing status '" + status + "' was not found. Only 'single' is enabled at this time.")

        return result
    

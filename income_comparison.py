import numpy as np
import matplotlib.pyplot as plt

"""
To add:
 - social security deduction?
 - print method for exporting calculated values and saving them
# it would be cool to have a method that figures out how much you'd have to make in a new state to match your current cash

"""


class income_comparison():
    
    def __init__(self, offer, state, COL_difference, 
                 current_income, current_state, 
                 fixed_expenses, current_flex_expenses):
        
        
        self.COL_difference = COL_difference
        self.fixed_expenses = fixed_expenses
        self.current_flex_expenses = current_flex_expenses
        self.current_expenses = fixed_expenses + current_flex_expenses
        self.prospective_expenses = self.COL_adjusted_expenses()
        
        # Calculate current AIF
        self.calculate_adjusted_income_factor(current_income, "CA", current=True)
        
        # Calculate prospective AIF
        self.calculate_adjusted_income_factor(offer, state)
    
    
    def calculate_adjusted_income_factor(self, income, state, current=False):
        
        if current:
            federal_tax_burden = self.federal_tax_burden(income, status="single")
            state_tax_burden = self.state_tax_burden(income, state=state, status="single")
            tax_burden = self.tax_burden(federal_tax_burden, state_tax_burden)
            tax_adjusted_income = self.tax_adjusted_offer(income, tax_burden)
            current_AIF = self.adjusted_income_factor(tax_adjusted_income, self.current_expenses)
        
            self.current_federal_tax_burden = federal_tax_burden
            self.current_state_tax_burden = state_tax_burden
            self.current_tax_burden = tax_burden
            self.current_tax_adjusted_income = tax_adjusted_income
            self.current_AIF = current_AIF
        
        else:
            federal_tax_burden = self.federal_tax_burden(income, status="single")
            state_tax_burden = self.state_tax_burden(income, state=state, status="single")
            tax_burden = self.tax_burden(federal_tax_burden, state_tax_burden)
            tax_adjusted_income = self.tax_adjusted_offer(income, tax_burden)
            AIF = self.adjusted_income_factor(tax_adjusted_income, self.prospective_expenses)
        
            self.prospective_federal_tax_burden = federal_tax_burden
            self.prospective_state_tax_burden = state_tax_burden
            self.prospective_tax_burden = tax_burden
            self.prospective_tax_adjusted_income = tax_adjusted_income
            self.prospective_AIF = AIF
    
    
    def adjusted_income_factor(self, tax_adjusted_offer, COL_adjusted_expenses):
        result = tax_adjusted_offer / COL_adjusted_expenses
        return result


    def tax_adjusted_offer(self, offer, tax_burden):
        result = offer - tax_burden
        self.adjusted_offer = result
        return result


    def tax_burden(self, federal_tax_burden, state_tax_burden):
        result = federal_tax_burden + state_tax_burden
        self.tax_burden
        return result


    def federal_tax_burden(self, income, status="single"):
        """
        For 2025. Does not provide accuracte values for incomes of $1,000,000+.
        """

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


    def state_tax_burden(self, income, state="CA", status="single"):
        """
        For 2025. May not provide accurate values for incomes of $1,000,000+.
        """

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


    def COL_adjusted_expenses(self):
        adjusted_flex_expenses = self.current_flex_expenses * ( 1 + self.COL_difference )   # COL_difference should be provided as a percent difference, e.g., -0.10 for 10% less
        result = self.fixed_expenses + adjusted_flex_expenses
        return result
    
    
    def report(self):
        print("=============================")
        print("-----------CURRENT-----------")
        print("=============================")
        print(f"Federal tax burden = ${self.current_federal_tax_burden:.2f}")
        print(f"State tax burden = ${self.current_state_tax_burden:.2f}")
        print(f"Total tax burden = ${self.current_tax_burden:.2f}")
        print(f"Tax adjusted income = ${self.current_tax_adjusted_income:.2f}")
        print(f"Expenses = ${self.current_expenses:.2f}")
        print(f"Adjusted Income Factor = {self.current_AIF:.2f}")
        print("\n")
        print("=============================")
        print("---------PROSPECTIVE---------")
        print("=============================")
        print(f"Federal tax burden = ${self.prospective_federal_tax_burden:.2f}")
        print(f"State tax burden = ${self.prospective_state_tax_burden:.2f}")
        print(f"Total tax burden = ${self.prospective_tax_burden:.2f}")
        print(f"Tax adjusted offer = ${self.prospective_tax_adjusted_income:.2f}")
        print(f"expenses = ${self.prospective_expenses:.2f}")
        print(f"Adjusted Income Factor = {self.prospective_AIF:.2f}")
        print("\n")
        print("=============================")
        print("-----------SUMMARY-----------")
        print("=============================")
        self.analyze_prospect()
    
    
    def analyze_prospect(self):
        statement1 = print(f"Current AIF = {self.current_AIF:.2f}")
        statement2 = print(f"Prospective AIF = {self.prospective_AIF:.2f}")
        line_break = print("\n")
        
        disposable_current = self.current_tax_adjusted_income - self.current_expenses
        disposable_prospective = self.prospective_tax_adjusted_income - self.prospective_expenses
        disposable_delta = disposable_prospective - disposable_current
        
        ratio = self.prospective_AIF / self.current_AIF
        
        if ratio > 1:
            statement3 = print(f"Offer has a favorable AIF that is {ratio:.2f}x larger than current AIF, indicating a positive prospect.")
        else:
            statement3 = print(f"Offer has an unfavorable AIF that is {ratio:.2f}x that of the current AIF, indicating an uninviting prospect.")
        
        if disposable_delta > 0:
            statement4 = print(f"There is a projected ${disposable_delta:.2f} increase in spending cash (${disposable_delta/12:.2f}/month).")
        elif disposable_delta == 0:
            statement4 = print(f"There is no projected change in spending cash! It's exactly the same.. spooky...")
        else:
            statement4 = print(f"There is a projected ${abs(disposable_delta):.2f} decrease in spending cash (${abs(disposable_delta)/12:.2f}/month).")
    
        return statement1, statement2, line_break, statement3, statement4
    
    

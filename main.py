import math
import sys

def check_params(params):
    # Ensure all required parameters are provided
    required_params = ["--type", "--principal", "--periods", "--interest"]
    
    if "--type" not in params or params["--type"] not in ["diff", "annuity"]:
        return "Incorrect parameters"
    
    if params["--type"] == "diff" and "--payment" in params:
        return "Incorrect parameters"
    
    if "--interest" not in params:
        return "Incorrect parameters"
    
    # Ensure no negative values
    for key, value in params.items():
        if key != "--type" and float(value) < 0:
            return "Incorrect parameters"
    
    # At least 4 parameters are required
    if len(params) < 4:
        return "Incorrect parameters"
    
    return None

def differentiated_payments(principal, periods, interest):
    nominal_rate = interest / 12 / 100
    total_payment = 0
    
    for m in range(1, periods + 1):
        diff_payment = principal / periods + nominal_rate * (principal - (principal * (m - 1)) / periods)
        print(f"Month {m}: payment is {math.ceil(diff_payment)}")
        total_payment += math.ceil(diff_payment)
    
    overpayment = total_payment - principal
    print(f"Overpayment = {int(overpayment)}")

def annuity_payment(principal, periods, interest):
    nominal_rate = interest / 12 / 100
    annuity = principal * (nominal_rate * math.pow(1 + nominal_rate, periods)) / (math.pow(1 + nominal_rate, periods) - 1)
    annuity = math.ceil(annuity)
    
    overpayment = annuity * periods - principal
    print(f"Your annuity payment = {annuity}!")
    print(f"Overpayment = {int(overpayment)}")

def annuity_principal(payment, periods, interest):
    nominal_rate = interest / 12 / 100
    principal = payment / ((nominal_rate * math.pow(1 + nominal_rate, periods)) / (math.pow(1 + nominal_rate, periods) - 1))
    principal = math.floor(principal)
    
    overpayment = payment * periods - principal
    print(f"Your loan principal = {principal}!")
    print(f"Overpayment = {int(overpayment)}")

def annuity_periods(principal, payment, interest):
    nominal_rate = interest / 12 / 100
    periods = math.log(payment / (payment - nominal_rate * principal), 1 + nominal_rate)
    periods = math.ceil(periods)
    
    years = periods // 12
    months = periods % 12
    
    if years > 0:
        if months > 0:
            print(f"It will take {years} years and {months} months to repay this loan!")
        else:
            print(f"It will take {years} years to repay this loan!")
    else:
        print(f"It will take {months} months to repay this loan!")
    
    overpayment = payment * periods - principal
    print(f"Overpayment = {int(overpayment)}")

def main():
    # Parse command-line arguments
    args = sys.argv[1:]
    params = {}
    
    for arg in args:
        key, value = arg.split('=')
        params[key] = value
    
    # Validate parameters
    error = check_params(params)
    if error:
        print(error)
        return
    
    loan_type = params["--type"]
    principal = float(params["--principal"]) if "--principal" in params else None
    periods = int(params["--periods"]) if "--periods" in params else None
    interest = float(params["--interest"]) if "--interest" in params else None
    payment = float(params["--payment"]) if "--payment" in params else None
    
    if loan_type == "diff":
        differentiated_payments(principal, periods, interest)
    elif loan_type == "annuity":
        if principal and periods and interest and not payment:
            annuity_payment(principal, periods, interest)
        elif payment and periods and interest and not principal:
            annuity_principal(payment, periods, interest)
        elif principal and payment and interest and not periods:
            annuity_periods(principal, payment, interest)

if __name__ == "__main__":
    main()
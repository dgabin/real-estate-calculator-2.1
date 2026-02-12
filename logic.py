from typing import Dict, Any

def calculate_payment_plan(
    price: float,
    separation: float,
    initial_percent: float,
    total_during_construction_percent: float,
    months: int
) -> Dict[str, Any]:
    """Calcula el plan de pagos durante la construcción."""
    
    if price <= 0 or months <= 0:
        return {"error": "El precio y los meses deben ser mayores a cero."}
    if total_during_construction_percent < initial_percent:
        return {"error": "El % total durante construcción no puede ser menor que el % inicial."}

    total_equity_target = price * (total_during_construction_percent / 100)
    initial_signing_target = price * (initial_percent / 100)

    if initial_signing_target > separation:
        due_at_signing = initial_signing_target - separation
    else:
        due_at_signing = 0.0

    total_paid_upfront = separation + due_at_signing
    remaining_equity_to_pay = total_equity_target - total_paid_upfront
    
    if remaining_equity_to_pay < 0:
        remaining_equity_to_pay = 0

    monthly_payment = remaining_equity_to_pay / months
    final_payment = price - total_equity_target

    return {
        "summary": {
            "property_price": price,
            "separation_paid": separation,
            "due_at_signing": due_at_signing,
            "monthly_payment": monthly_payment,
            "number_of_months": months,
            "total_during_construction": remaining_equity_to_pay,
            "final_payment": final_payment,
            "total_equity_invested": total_equity_target,
        },
        "percentages": {
            "initial_target": initial_percent,
            "total_equity": total_during_construction_percent
        }
    }

def calculate_mortgage(
    loan_amount: float, 
    annual_interest_rate: float, 
    years: int,
    insurance_percent_annual: float = 1.0 
) -> Dict[str, float]:
    """
    Calcula la cuota nivelada del préstamo (Capital + Interés + Seguro).
    insurance_percent_annual: % anual sobre el monto del préstamo (ej. 0.8% - 1.2% es común).
    """
    if loan_amount <= 0:
        return {"monthly_total": 0, "monthly_principal_interest": 0, "monthly_insurance": 0}

    # Tasas mensuales
    monthly_rate = (annual_interest_rate / 100) / 12
    n_payments = years * 12
    
    # 1. Cuota del Préstamo (Formula de Amortización Francesa)
    if monthly_rate > 0:
        factor = (1 + monthly_rate) ** n_payments
        monthly_principal_interest = loan_amount * (monthly_rate * factor) / (factor - 1)
    else:
        monthly_principal_interest = loan_amount / n_payments

    # 2. Seguro (Estimado promedio mensual)
    monthly_insurance = loan_amount * (insurance_percent_annual / 100) / 12

    return {
        "monthly_principal_interest": monthly_principal_interest,
        "monthly_insurance": monthly_insurance,
        "monthly_total": monthly_principal_interest + monthly_insurance,
        "loan_amount": loan_amount,
        "rate": annual_interest_rate,
        "years": years
    }

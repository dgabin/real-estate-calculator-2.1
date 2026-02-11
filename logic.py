from typing import Dict, Any

def calculate_payment_plan(
    price: float,
    separation: float,
    initial_percent: float,  # This can now be 0 if only separation is needed
    total_during_construction_percent: float,
    months: int
) -> Dict[str, Any]:
    """
    Calculates the payment schedule for a pre-construction real estate property.
    Now handles 'Separation Only' contracts where initial_percent is 0.
    """
    
    # 1. Validation
    if price <= 0 or months <= 0:
        return {"error": "Price and months must be greater than zero."}
    if total_during_construction_percent < initial_percent:
        return {"error": "Total construction % cannot be less than the initial signing %."}

    # 2. Calculate Targets
    # The total cash the client must invest before delivery (e.g. 30% of 100k = 30k)
    total_equity_target = price * (total_during_construction_percent / 100)
    
    # The target for the specific "Contract Signing" event (e.g. 10% of 100k = 10k)
    initial_signing_target = price * (initial_percent / 100)

    # 3. Calculate "Due at Signing"
    # If the target is 0% (or less than separation), nothing extra is due at signing.
    if initial_signing_target > separation:
        due_at_signing = initial_signing_target - separation
    else:
        due_at_signing = 0.0

    # 4. Calculate "During Construction" Monthly Payments
    # Logic: Total Equity Target - (Everything Paid So Far)
    total_paid_upfront = separation + due_at_signing
    remaining_equity_to_pay = total_equity_target - total_paid_upfront
    
    # Guard clause: If for some reason they paid MORE upfront than the total equity target
    if remaining_equity_to_pay < 0:
        remaining_equity_to_pay = 0

    monthly_payment = remaining_equity_to_pay / months

    # 5. Calculate Final Payment ("Contra Entrega")
    # Logic: Property Price - Total Equity Target
    final_payment = price - total_equity_target

    return {
        "summary": {
            "property_price": price,
            "separation_paid": separation,
            "due_at_signing": due_at_signing, # This will be 0 if "Just Separation"
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

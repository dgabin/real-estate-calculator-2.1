from typing import Dict, Any

def calculate_payment_plan(
    price: float,
    separation: float,
    initial_percent: float,
    total_during_construction_percent: float,
    months: int
) -> Dict[str, Any]:
    """
    Calcula el plan de pagos para propiedades en pre-construcción.
    """
    
    # 1. Validación
    if price <= 0 or months <= 0:
        return {"error": "El precio y los meses deben ser mayores a cero."}
    if total_during_construction_percent < initial_percent:
        return {"error": "El % total durante construcción no puede ser menor que el % inicial."}

    # 2. Calcular Objetivos (Targets)
    # Total de capital que el cliente debe pagar antes de la entrega
    total_equity_target = price * (total_during_construction_percent / 100)
    
    # Objetivo para la firma del contrato
    initial_signing_target = price * (initial_percent / 100)

    # 3. Calcular "A la Firma" (Due at Signing)
    if initial_signing_target > separation:
        due_at_signing = initial_signing_target - separation
    else:
        due_at_signing = 0.0

    # 4. Calcular Cuotas Mensuales
    total_paid_upfront = separation + due_at_signing
    remaining_equity_to_pay = total_equity_target - total_paid_upfront
    
    if remaining_equity_to_pay < 0:
        remaining_equity_to_pay = 0

    monthly_payment = remaining_equity_to_pay / months

    # 5. Calcular Pago Final (Contra Entrega)
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

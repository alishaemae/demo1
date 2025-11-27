# app/utils/discount.py

def calculate_partner_discount(total_quantity):
    try:
        total = int(total_quantity)
    except Exception:
        return 0.0
    if total <= 10000:
        return 0.0
    if total <= 50000:
        return 0.05
    if total <= 300000:
        return 0.10
    return 0.15

# app/utils/material_calc.py
import math
from database import get_connection

def calculate_material_needed(product_type_id, material_type_id, produced_quantity, param_a, param_b):
    try:
        produced_quantity = int(produced_quantity)
        param_a = float(param_a)
        param_b = float(param_b)
    except Exception:
        return -1
    if produced_quantity <= 0 or param_a <= 0 or param_b <= 0:
        return -1

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT production_coefficient FROM product_type WHERE id=%s", (product_type_id,))
            pt = cur.fetchone()
            if not pt:
                return -1
            coeff = float(pt['production_coefficient'])
            cur.execute("SELECT defect_percent FROM material_type WHERE id=%s", (material_type_id,))
            mt = cur.fetchone()
            if not mt:
                return -1
            defect = float(mt['defect_percent'])

            material_per_unit = param_a * param_b * coeff
            total_material = material_per_unit * produced_quantity
            total_with_defect = total_material * (1 + defect)
            return int(math.ceil(total_with_defect))
    finally:
        conn.close()

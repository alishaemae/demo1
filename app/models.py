from database import get_connection

def fetch_partners():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT id, partner_type, name, director_fullname, phone, email, rating 
                           FROM partner 
                           WHERE deleted_at IS NULL
                           ORDER BY name""")
            return cur.fetchall()
    finally:
        conn.close()


def fetch_partner_by_id(partner_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM partner WHERE id=%s", (partner_id,))
            return cur.fetchone()
    finally:
        conn.close()


def insert_partner(data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO partner (partner_type, name, director_fullname, email, phone, legal_address, inn, rating, logo_path)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (data.get('partner_type'), data.get('name'), data.get('director_fullname'),
                         data.get('email'), data.get('phone'), data.get('legal_address'),
                         data.get('inn'), data.get('rating', 0), data.get('logo_path')))
            return cur.lastrowid
    finally:
        conn.close()


def delete_partner(partner_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE partner SET deleted_at = NOW() WHERE id=%s", (partner_id,))
            return cur.rowcount
    finally:
        conn.close()


def update_partner(partner_id, data):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""UPDATE partner SET partner_type=%s, name=%s, director_fullname=%s, email=%s, phone=%s,
                           legal_address=%s, inn=%s, rating=%s, logo_path=%s WHERE id=%s""",
                        (data.get('partner_type'), data.get('name'), data.get('director_fullname'), data.get('email'),
                         data.get('phone'), data.get('legal_address'), data.get('inn'), data.get('rating',0),
                         data.get('logo_path'), partner_id))
            return cur.rowcount
    finally:
        conn.close()


def fetch_sales_by_partner(partner_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT ps.id, p.name AS product_name, ps.quantity, ps.sale_date
                           FROM partner_sales ps
                           JOIN product p ON ps.product_id = p.id
                           WHERE ps.partner_id = %s
                           ORDER BY ps.sale_date DESC""", (partner_id,))
            return cur.fetchall()
    finally:
        conn.close()


def total_sales_quantity_for_partner(partner_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(SUM(quantity),0) AS total_q FROM partner_sales WHERE partner_id=%s", (partner_id,))
            row = cur.fetchone()
            return int(row['total_q']) if row else 0
    finally:
        conn.close()


def sample_min_product_price():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT MIN(min_price_for_partner) AS min_p FROM product")
            r = cur.fetchone()
            return float(r['min_p']) if r and r['min_p'] is not None else 0.0
    finally:
        conn.close()

def fetch_partner_history(partner_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""SELECT sale_date AS date, CONCAT('Продажа: ', quantity, ' шт. продукта ', product_id) AS action
                           FROM partner_sales
                           WHERE partner_id = %s
                           ORDER BY sale_date DESC""", (partner_id,))
            return cur.fetchall()
    finally:
        conn.close()

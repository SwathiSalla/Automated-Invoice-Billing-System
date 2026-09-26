import pandas as pd
import mysql.connector
from config import DB_CONFIG

def load_sample_dataset_to_db(data):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    grouped = data.groupby('InvoiceNo')

    for invoice_no, group in grouped:
        first_row = group.iloc[0]
        cust_id = str(first_row.get('CustomerID', 'GUEST'))
        cust_name = f"Customer_{cust_id}"
        country = str(first_row.get('Country', 'Unknown'))
        inv_date = pd.to_datetime(first_row.get('InvoiceDate')).strftime('%Y-%m-%d')

        cursor.execute(
            "INSERT INTO customers (customer_id, customer_name, country) VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE customer_name=%s",
            (cust_id, cust_name, country, cust_name)
        )

        subtotal = 0.0
        items = []
        for _, row in group.iterrows():
            qty = int(row.get('Quantity', 1))
            price = float(row.get('UnitPrice', 0.0))
            if qty <= 0 or price < 0:
                continue
            line_tot = qty * price
            subtotal += line_tot
            items.append((str(row.get('Description', 'Item')), qty, price, line_tot))

        tax = round(subtotal * 0.10, 2)
        total = round(subtotal + tax, 2)

        cursor.execute(
            "INSERT IGNORE INTO invoices (invoice_number, customer_id, invoice_date, subtotal, tax_amount, total_amount) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (str(invoice_no), cust_id, inv_date, subtotal, tax, total)
        )

        for desc, qty, price, line_tot in items:
            cursor.execute(
                "INSERT INTO invoice_items (invoice_number, description, quantity, unit_price, line_total) "
                "VALUES (%s, %s, %s, %s, %s)",
                (str(invoice_no), desc, qty, price, line_tot)
            )

    conn.commit()
    cursor.close()
    conn.close()
    print("Dataset records successfully loaded into MySQL.")

sample_df = pd.DataFrame([
    {"InvoiceNo": "INV-1001", "StockCode": "85123A", "Description": "WHITE HANGING HEART T-LIGHT HOLDER", "Quantity": 6, "InvoiceDate": "2026-03-01", "UnitPrice": 2.55, "CustomerID": 17850, "Country": "United Kingdom"},
    {"InvoiceNo": "INV-1001", "StockCode": "71053", "Description": "WHITE METAL LANTERN", "Quantity": 6, "InvoiceDate": "2026-03-01", "UnitPrice": 3.39, "CustomerID": 17850, "Country": "United Kingdom"},
    {"InvoiceNo": "INV-1002", "StockCode": "21212", "Description": "PACK OF 72 RETROSPOT TIN TINS", "Quantity": 24, "InvoiceDate": "2026-03-02", "UnitPrice": 0.55, "CustomerID": 13047, "Country": "United Kingdom"}
])

if __name__ == "__main__":
    load_sample_dataset_to_db(sample_df)
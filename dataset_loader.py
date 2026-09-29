import pandas as pd
import mysql.connector
import os
from config import DB_CONFIG

DATASET_FILE = "OnlineRetail.csv"

def load_local_dataset_to_db(limit=300):
    if not os.path.exists(DATASET_FILE):
        print(f"Error: {DATASET_FILE} not found in project directory.")
        return

    print(f"Reading dataset from local file: {DATASET_FILE}...")
    try:
        df = pd.read_csv(DATASET_FILE, encoding="ISO-8859-1")
        print(f"Successfully loaded dataset with {len(df)} total transaction records.")
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return

    # Data Cleaning
    df = df.dropna(subset=['CustomerID', 'Description'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]

    # Process sample
    df_sample = df.head(limit)

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    grouped = df_sample.groupby('InvoiceNo')

    print(f"Processing {len(grouped)} unique invoices into MySQL...")

    for invoice_no, group in grouped:
        first_row = group.iloc[0]
        cust_id = str(int(first_row['CustomerID']))
        cust_name = f"Customer_{cust_id}"
        country = str(first_row.get('Country', 'Unknown'))
        
        try:
            inv_date = pd.to_datetime(first_row['InvoiceDate']).strftime('%Y-%m-%d')
        except:
            inv_date = "2026-03-01"

        cursor.execute(
            "INSERT INTO customers (customer_id, customer_name, country) VALUES (%s, %s, %s) "
            "ON DUPLICATE KEY UPDATE customer_name=%s",
            (cust_id, cust_name, country, cust_name)
        )

        subtotal = 0.0
        items = []
        for _, row in group.iterrows():
            qty = int(row['Quantity'])
            price = float(row['UnitPrice'])
            line_tot = round(qty * price, 2)
            subtotal += line_tot
            items.append((str(row['Description']).strip(), qty, price, line_tot))

        subtotal = round(subtotal, 2)
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
    print("Dataset records successfully loaded into MySQL!")

if __name__ == "__main__":
    load_local_dataset_to_db(500)
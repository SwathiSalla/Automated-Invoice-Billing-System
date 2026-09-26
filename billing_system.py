import os
import mysql.connector
from config import DB_CONFIG, OUTPUT_DIR
from invoice_generator import build_pdf_invoice

class BillingManager:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)

    def fetch_invoice(self, invoice_number):
        cursor = self.conn.cursor(dictionary=True)
        
        query_inv = """
        SELECT i.invoice_number, i.invoice_date, i.subtotal, i.tax_amount, i.total_amount, 
               c.customer_id, c.customer_name
        FROM invoices i
        JOIN customers c ON i.customer_id = c.customer_id
        WHERE i.invoice_number = %s
        """
        cursor.execute(query_inv, (invoice_number,))
        invoice_details = cursor.fetchone()

        if not invoice_details:
            cursor.close()
            return None, []

        query_items = """
        SELECT description, quantity, unit_price, line_total 
        FROM invoice_items 
        WHERE invoice_number = %s
        """
        cursor.execute(query_items, (invoice_number,))
        items = cursor.fetchall()
        cursor.close()

        return invoice_details, items

    def generate_pdf_for_invoice(self, invoice_number):
        invoice_details, items = self.fetch_invoice(invoice_number)
        if not invoice_details:
            print(f"Invoice {invoice_number} not found.")
            return False

        output_path = os.path.join(OUTPUT_DIR, f"{invoice_number}.pdf")
        build_pdf_invoice(invoice_details, items, output_path)
        return True

    def close(self):
        self.conn.close()
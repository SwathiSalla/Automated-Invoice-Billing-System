import mysql.connector
from config import DB_CONFIG
from db_setup import initialize_database
from dataset_loader import load_internet_dataset_to_db
from billing_system import BillingManager

def generate_all_invoices():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT invoice_number FROM invoices")
    invoice_numbers = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    manager = BillingManager()
    print(f"\nFound {len(invoice_numbers)} unique invoices in database. Generating PDFs...")
    
    # Generate PDFs for the first 5 invoices in the dataset
    for inv_no in invoice_numbers[:5]:
        print(f"Generating PDF for Invoice: {inv_no}")
        manager.generate_pdf_for_invoice(inv_no)
        
    manager.close()

def main():
    print("=========================================================")
    print(" Automated Invoice Generator & Billing Management System ")
    print("=========================================================")
    
    # Step 1: Initialize Database
    initialize_database()

    # Step 2: Fetch Real Internet Dataset & Store in MySQL
    print("\n[Data Pipeline] Fetching retail dataset from internet...")
    load_internet_dataset_to_db(limit=200)

    # Step 3: Batch PDF Generation
    print("\n[PDF Pipeline] Generating PDF invoices from database records...")
    generate_all_invoices()

    print("\n[SUCCESS] Pipeline execution complete! PDF invoices generated in output_invoices/")

if __name__ == "__main__":
    main()
from db_setup import initialize_database
from dataset_loader import load_sample_dataset_to_db, sample_df
from billing_system import BillingManager

def main():
    print("--- Automated Invoice Generator & Billing Management System ---")
    
    initialize_database()

    print("\nLoading dataset records into MySQL...")
    load_sample_dataset_to_db(sample_df)

    manager = BillingManager()
    
    target_invoice = "INV-1001"
    print(f"\nGenerating PDF invoice for: {target_invoice}")
    manager.generate_pdf_for_invoice(target_invoice)

    manager.close()
    print("\nWorkflow completed successfully.")

if __name__ == "__main__":
    main()
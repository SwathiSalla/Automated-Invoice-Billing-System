import os

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Swathi@2008", 
    "database": "billing_system_db"
}

OUTPUT_DIR = "output_invoices"
os.makedirs(OUTPUT_DIR, exist_ok=True)
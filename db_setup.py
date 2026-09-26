import mysql.connector
from config import DB_CONFIG

def initialize_database():
    conn = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(50) PRIMARY KEY,
        customer_name VARCHAR(255) NOT NULL,
        country VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        invoice_number VARCHAR(50) PRIMARY KEY,
        customer_id VARCHAR(50),
        invoice_date DATE,
        subtotal DECIMAL(10, 2),
        tax_amount DECIMAL(10, 2),
        total_amount DECIMAL(10, 2),
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items (
        item_id INT AUTO_INCREMENT PRIMARY KEY,
        invoice_number VARCHAR(50),
        description VARCHAR(255),
        quantity INT,
        unit_price DECIMAL(10, 2),
        line_total DECIMAL(10, 2),
        FOREIGN KEY (invoice_number) REFERENCES invoices(invoice_number)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("MySQL Database and tables initialized successfully.")

if __name__ == "__main__":
    initialize_database()
import streamlit as st
import mysql.connector
import os
from config import DB_CONFIG, OUTPUT_DIR
from billing_system import BillingManager

st.set_page_config(page_title="Invoice Generator App", page_icon="🧾", layout="wide")

st.title("🧾 Automated Invoice Generator & Billing Management System")
st.write("Select an invoice number from the database to generate and view the PDF invoice.")

# Fetch invoice numbers from MySQL
def get_invoice_list():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_number FROM invoices")
        invoices = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return invoices
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return []

invoice_list = get_invoice_list()

if invoice_list:
    selected_invoice = st.selectbox("Select Invoice Number", invoice_list)
    
    if st.button("Generate & View Invoice PDF"):
        manager = BillingManager()
        success = manager.generate_pdf_for_invoice(selected_invoice)
        manager.close()
        
        if success:
            st.success(f"Invoice {selected_invoice} generated successfully!")
            pdf_path = os.path.join(OUTPUT_DIR, f"{selected_invoice}.pdf")
            
            # Display PDF download button
            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="📥 Download Invoice PDF",
                    data=file,
                    file_name=f"{selected_invoice}.pdf",
                    mime="application/pdf"
                )
else:
    st.warning("No invoices found in database. Make sure main.py has been executed.")
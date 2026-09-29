import streamlit as st
import mysql.connector
import pandas as pd
import os
from config import DB_CONFIG, OUTPUT_DIR
from billing_system import BillingManager


# Page Configuration
st.set_page_config(
    page_title="Enterprise Billing & Analytics System",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Enterprise Modern UI & Sidebar Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }

    .sub-title {
        font-size: 0.95rem;
        color: #64748B;
        margin-bottom: 1.2rem;
    }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }

    /* Custom Sidebar Header Box */
    .sidebar-brand {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        padding: 1.25rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    .sidebar-brand h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        margin: 0;
        font-size: 1.15rem;
    }

    .sidebar-brand p {
        color: #93C5FD !important;
        font-size: 0.78rem;
        margin: 0;
    }

    /* Status Badge in Sidebar */
    .status-badge {
        background-color: #1E293B;
        border-left: 4px solid #10B981;
        padding: 0.6rem 0.8rem;
        border-radius: 6px;
        font-size: 0.8rem;
        margin-top: 2rem;
    }

    /* Metric Summary Pills */
    .summary-pill {
        background-color: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        color: #1E293B;
    }

    /* Primary Action Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #1D4ED8;
    }
</style>
""", unsafe_allow_html=True)


def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return None


# Header Section
st.markdown(
    '<div class="main-title">🧾 Automated Invoice Generation & Billing Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Automated Retail Data Ingestion, Relational Management, and Dynamic PDF Generation</div>',
    unsafe_allow_html=True
)

st.divider()


# Upgraded Left Sidebar Section
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <h3>🧾 Retail Billing POS</h3>
            <p>Enterprise Billing System</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 📌 Operations Module")

    menu = st.radio(
        label="Select View",
        options=[
            "📊 Dashboard Analytics",
            "📄 PDF Generation Studio",
            "🛒 POS Billing Counter"
        ],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("""
        <div class="status-badge">
            <span style="color: #10B981 !important;">● System Online</span><br/>
            <span style="color: #94A3B8 !important; font-size: 0.75rem;">
                Connected to Cloud Database
            </span>
        </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------
# PAGE 1: DASHBOARD ANALYTICS
# -------------------------------------------------------------
if menu == "📊 Dashboard Analytics":

    conn = get_db_connection()

    if conn:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT COUNT(*) as total_inv, "
            "SUM(total_amount) as total_rev, "
            "AVG(total_amount) as avg_inv "
            "FROM invoices"
        )

        metrics = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) as total_cust FROM customers")
        cust_count = cursor.fetchone()['total_cust']

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                label="Total Invoices",
                value=f"{metrics['total_inv'] or 0:,}"
            )

        with c2:
            st.metric(
                label="Gross Revenue",
                value=f"${metrics['total_rev'] or 0:,.2f}"
            )

        with c3:
            st.metric(
                label="Avg Invoice Value",
                value=f"${metrics['avg_inv'] or 0:,.2f}"
            )

        with c4:
            st.metric(
                label="Total Customers",
                value=f"{cust_count or 0:,}"
            )

        st.divider()

        st.subheader("📋 Ingested Invoice Master Registry")

        query = """
        SELECT i.invoice_number AS `Invoice No`, 
               c.customer_name AS `Customer`, 
               c.country AS `Country`,
               i.invoice_date AS `Date`, 
               CONCAT('$', FORMAT(i.subtotal, 2)) AS `Subtotal`, 
               CONCAT('$', FORMAT(i.tax_amount, 2)) AS `Tax (10%)`, 
               CONCAT('$', FORMAT(i.total_amount, 2)) AS `Total Due`
        FROM invoices i 
        JOIN customers c ON i.customer_id = c.customer_id
        ORDER BY i.invoice_date DESC
        """

        df_invoices = pd.read_sql(query, conn)

        search_term = st.text_input(
            "🔍 Search Invoices by Number or Customer",
            ""
        )

        if search_term:
            df_invoices = df_invoices[
                df_invoices['Invoice No'].astype(str).str.contains(
                    search_term,
                    case=False
                )
                |
                df_invoices['Customer'].astype(str).str.contains(
                    search_term,
                    case=False
                )
            ]

        st.dataframe(
            df_invoices,
            use_container_width=True,
            hide_index=True
        )

        cursor.close()
        conn.close()


# -------------------------------------------------------------
# PAGE 2: GENERATE & VIEW PDF INVOICES
# -------------------------------------------------------------
elif menu == "📄 PDF Generation Studio":

    st.subheader("📄 PDF Generation Studio")

    conn = get_db_connection()

    if conn:

        cursor = conn.cursor()

        cursor.execute("SELECT invoice_number FROM invoices")

        invoice_list = [
            row[0]
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        if invoice_list:

            col1, col2 = st.columns([2, 1])

            with col1:
                selected_invoice = st.selectbox(
                    "Select Target Invoice Number",
                    invoice_list
                )

            if st.button(
                "Build PDF Document",
                type="primary"
            ):

                manager = BillingManager()

                success = manager.generate_pdf_for_invoice(
                    selected_invoice
                )

                manager.close()

                if success:

                    st.success(
                        f"Successfully generated PDF for **{selected_invoice}**"
                    )

                    pdf_path = os.path.join(
                        OUTPUT_DIR,
                        f"{selected_invoice}.pdf"
                    )

                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()

                    st.download_button(
                        label="📥 Download PDF Document",
                        data=pdf_bytes,
                        file_name=f"{selected_invoice}.pdf",
                        mime="application/pdf"
                    )

                    # Native Streamlit PDF Preview
                    st.subheader("📄 Invoice Preview")

                    st.pdf(
                        pdf_bytes,
                        height=700
                    )

        else:
            st.warning("No invoices found in database.")


# -------------------------------------------------------------
# PAGE 3: CREATE MANUAL INVOICE (POS COUNTER)
# -------------------------------------------------------------
elif menu == "🛒 POS Billing Counter":

    st.subheader("🛒 Interactive Retail POS Checkout Counter")

    if "cart_items" not in st.session_state:
        st.session_state.cart_items = []

    st.markdown("##### 👤 Customer & Order Metadata")

    with st.container():

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            inv_no = st.text_input(
                "Invoice Number",
                value="INV-5001"
            )

        with c2:
            cust_id = st.text_input(
                "Customer ID",
                value="CUST-808"
            )

        with c3:
            cust_name = st.text_input(
                "Customer Name",
                value="Global Enterprise Solutions"
            )

        with c4:
            country = st.text_input(
                "Country",
                value="United States"
            )

    st.divider()

    st.markdown("##### 📦 Add Products to Active Cart")

    col_item1, col_item2, col_item3, col_item4 = st.columns(
        [3, 1, 1, 1]
    )

    with col_item1:
        item_desc = st.text_input(
            "Item Description / Name",
            placeholder="e.g. Wireless Ergonomic Mouse"
        )

    with col_item2:
        item_qty = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1
        )

    with col_item3:
        item_price = st.number_input(
            "Unit Price ($)",
            min_value=0.01,
            value=25.00,
            step=1.00
        )

    with col_item4:

        st.write("")
        st.write("")

        if st.button("➕ Add Item to Bill"):

            if item_desc.strip():

                st.session_state.cart_items.append({
                    "Description": item_desc.strip(),
                    "Quantity": int(item_qty),
                    "Unit Price ($)": float(item_price),
                    "Line Total ($)": round(
                        int(item_qty) * float(item_price),
                        2
                    )
                })

                st.toast(
                    f"Added '{item_desc}' to bill!",
                    icon="✅"
                )

            else:
                st.warning(
                    "Please enter a valid item description."
                )

    if st.session_state.cart_items:

        st.markdown("##### 🧾 Scanned / Billed Items Table")

        df_cart = pd.DataFrame(
            st.session_state.cart_items
        )

        st.dataframe(
            df_cart,
            use_container_width=True,
            hide_index=True
        )

        subtotal = sum(
            item["Line Total ($)"]
            for item in st.session_state.cart_items
        )

        tax = round(
            subtotal * 0.10,
            2
        )

        total = round(
            subtotal + tax,
            2
        )

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(
                f'<div class="summary-pill">'
                f'Subtotal: ${subtotal:,.2f}'
                f'</div>',
                unsafe_allow_html=True
            )

        with m2:
            st.markdown(
                f'<div class="summary-pill">'
                f'Tax (10%): ${tax:,.2f}'
                f'</div>',
                unsafe_allow_html=True
            )

        with m3:
            st.markdown(
                f'<div class="summary-pill" '
                f'style="border-left-color: #16A34A; '
                f'color: #16A34A;">'
                f'Total Due: ${total:,.2f}'
                f'</div>',
                unsafe_allow_html=True
            )

        st.write("")

        btn_col1, btn_col2 = st.columns([1, 4])

        with btn_col1:

            if st.button(
                "💾 Complete Order & Print PDF",
                type="primary"
            ):

                conn = get_db_connection()

                if conn:

                    cursor = conn.cursor()

                    cursor.execute(
                        "INSERT INTO customers "
                        "(customer_id, customer_name, country) "
                        "VALUES (%s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "customer_name=%s",
                        (
                            cust_id,
                            cust_name,
                            country,
                            cust_name
                        )
                    )

                    cursor.execute(
                        "INSERT INTO invoices "
                        "(invoice_number, customer_id, invoice_date, "
                        "subtotal, tax_amount, total_amount) "
                        "VALUES (%s, %s, CURDATE(), %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "total_amount=%s",
                        (
                            inv_no,
                            cust_id,
                            subtotal,
                            tax,
                            total,
                            total
                        )
                    )

                    for item in st.session_state.cart_items:

                        cursor.execute(
                            "INSERT INTO invoice_items "
                            "(invoice_number, description, quantity, "
                            "unit_price, line_total) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (
                                inv_no,
                                item["Description"],
                                item["Quantity"],
                                item["Unit Price ($)"],
                                item["Line Total ($)"]
                            )
                        )

                    conn.commit()

                    cursor.close()
                    conn.close()

                    manager = BillingManager()

                    manager.generate_pdf_for_invoice(
                        inv_no
                    )

                    manager.close()

                    st.success(
                        f"Order **{inv_no}** completed! "
                        f"Saved to Cloud Database and PDF "
                        f"generated successfully."
                    )

                    st.session_state.cart_items = []

        with btn_col2:

            if st.button("🗑️ Clear Cart"):

                st.session_state.cart_items = []

                st.rerun()

    else:

        st.info(
            "Your active cart is empty. Enter product details "
            "above and click 'Add Item to Bill' to begin."
        )
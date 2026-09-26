# 📄 Automated Invoice Generator & Billing System

An end-to-end automated billing management and analytics system built using **Python**, **Streamlit**, **MySQL**, and **ReportLab**. This project processes real-world e-commerce retail data, manages client and invoice records, generates clean PDF receipts, and provides real-time financial dashboard analytics.

---

## 🚀 Features

* **📊 Live Dashboard Analytics:** Interactive Streamlit interface displaying key metrics such as total invoices, revenue generated, and average invoice amounts.
* **🧾 PDF Invoice Generation:** Dynamically creates formatted, professional PDF receipts using ReportLab.
* **💾 Database Storage:** Robust relational schema in MySQL for managing clients, line items, and invoice history.
* **📦 Retail Dataset Processing:** Automatic loading and cleaning of bulk transactional e-commerce datasets.
* **📁 Clean Project Architecture:** Modular codebase separated into database setup, invoice creation, data processing, and frontend UI.

---

## 🛠️ Project Structure

```text
Automated-Invoice-Billing-System/
├── app.py                 # Main Streamlit Dashboard Application
├── invoice_generator.py   # Engine for rendering PDF documents via ReportLab
├── dataset_loader.py      # Script to load and process retail dataset
├── db_setup.py            # MySQL database initialization & connection logic
├── billing_system.py      # Core business logic for invoice operations
├── main.py                # Pipeline execution script
├── config.py              # Configuration & environment settings
├── requirements.txt       # Project dependencies
├── OnlineRetail.csv       # E-Commerce dataset
└── README.md              # Project documentation
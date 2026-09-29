<div align="center">

# 🧾 Automated Invoice Generation & Billing Management System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)

[![MySQL](https://img.shields.io/badge/MySQL--Compatible-TiDB-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.tidbcloud.com/)

[![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Engine-00599C?style=for-the-badge)](https://www.reportlab.com/)

**An end-to-end Invoice Billing & Revenue Analytics Solution**

*Processes e-commerce transaction data, automates PDF invoice generation, and provides an interactive billing dashboard.*

[🚀 **Live Demo**](https://automated-invoice-billing-system-ljsufg9hgueydwbkrde5zw.streamlit.app/)

</div>

---

## 🌟 Key Highlights

- **📊 Dynamic Analytics Dashboard:**  
  Built with Streamlit to display invoice counts, total revenue, and average invoice values.

- **⚡ Automated PDF Invoice Generation:**  
  Uses ReportLab to generate PDF invoices dynamically from billing data.

- **🗄️ Cloud Database Integration:**  
  Uses TiDB Cloud, a MySQL-compatible database, to store customers, invoices, and invoice items.

- **📈 Real-World Dataset Pipeline:**  
  Processes and cleans the `OnlineRetail.csv` dataset and loads transaction data into the database.

- **🔄 Automated Billing Calculations:**  
  Calculates subtotals, tax amounts, and total invoice values automatically.

---

## 🖼️ Application Preview

<div align="center">

<img src="images/dashboard.png" alt="Streamlit Dashboard Preview" width="800"/>

<br/><br/>

<img src="images/invoice.png" alt="Generated PDF Invoice Preview" width="800"/>

</div>

---

## 🏗️ System Architecture

```text
        ┌────────────────────────┐
        │     OnlineRetail.csv   │
        │   E-Commerce Dataset   │
        └───────────┬────────────┘
                    │
                    ▼
        ┌────────────────────────┐
        │    dataset_loader.py   │
        │   Data Cleaning & ETL  │
        └───────────┬────────────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│       TiDB Cloud Database            │
│       MySQL-Compatible               │
│                                      │
│  - customers                         │
│  - invoices                          │
│  - invoice_items                     │
└──────────────────┬───────────────────┘
                   │
          ┌────────┴─────────┐
          ▼                  ▼
┌──────────────────┐  ┌──────────────────────┐
│     app.py       │  │ invoice_generator.py │
│    Streamlit UI  │  │   ReportLab PDFs     │
└──────────────────┘  └──────────────────────┘
<div align="center">

# 🧾 Automated Invoice Generation & Billing Management System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF_Engine-00599C?style=for-the-badge)](https://www.reportlab.com/)

**An end-to-end Capstone Billing & Revenue Analytics Solution**  
*Processes e-commerce datasets, automates PDF invoice rendering, and delivers live business intelligence.*

---

</div>

## 🌟 Key Highlights

- **📊 Dynamic Analytics Dashboard:** Built with Streamlit for real-time tracking of total revenue, invoice counts, and transaction averages.
- **⚡ Automated PDF Engine:** Uses ReportLab to generate dynamic, pixel-perfect invoice receipts automatically.
- **🗄️ Relational Database Core:** Backed by MySQL for reliable storage of clients, items, transactional ledgers, and billing statuses.
- **📈 Real-World Dataset Pipeline:** Automatically ingests and cleans the bulk `OnlineRetail` dataset for immediate analytical reporting.
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
       │   OnlineRetail.csv     │ (E-Commerce Ingestion)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │   dataset_loader.py    │ (ETL & Cleaning)
       └───────────┬────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│        MySQL Database (db_setup)     │
│  - clients   - invoices   - items    │
└──────────────────┬───────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌──────────────────┐  ┌──────────────────┐
│   app.py (UI)    │  │ invoice_generator│
│ Streamlit Visuals│  │  ReportLab PDFs  │
└──────────────────┘  └──────────────────┘
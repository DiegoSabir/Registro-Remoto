# Odoo Human Resources App

## Overview
Galvintec HR Management App is a Python-based solution that facilitates employee management, invoice tracking, and timekeeping for organizations using the Odoo ERP system. The app provides seamless integration with Odoo via XML-RPC, utilizing AI for enhanced invoice processing, and includes a mobile-friendly interface built with Flet.

---

## Features

### Authentication
- Secure login with saved credentials.
- Automatic connection to Odoo server.

### Employee Timekeeping
- Clock in and clock out functionalities.
- Tracks daily working hours.

### Invoice Management
- AI invoice analysis.
- Allows users to register and list invoices.
- Supports photo attachments for invoices.

### Expense Tracking
- View and delete employee expenses.
- Retrieve product data from Odoo.

### Theme Support
- Dark mode and light mode with seamless switching.

---

## Installation

### Prerequisites
- Python 3.10+
- Docker (optional for development)
- Odoo server

---

### Steps
1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd app-odoo-hr
   
2. Install dependencies:

   ```bash
   pip install -r flet/src/requirements.txt
   
3. Run the application:

   ```bash
   python flet/src/main.py

---

## Usage

### Sign In
- Enter your credentials (email, password, server URL, and database).
- Log in to access the main menu.

<img src="/flet/src/assets/images/signin_light.jpg" alt="Sign In Light Mode" title="Sign In Light Mode" style="width: 30%; height: auto;"/>

### Menu
- Clock In/Out: Record your working hours with a single click.
- Invoice Management:
  - Attach a photo of your invoice.
  - Use AI analysis to extract invoice details.
  - Register the invoice into Odoo.
- Expense Tracking:
  - View your recorded expenses.
  - Delete unnecessary entries.

<div style="display: flex; gap: 10px; justify-content: center; align-items: center; flex-wrap: wrap;">
  <img src="/flet/src/assets/images/menu_light.jpg" alt="Menu Light Mode" title="Menu Light Mode" style="width: 30%; height: auto;"/>
  <img src="/flet/src/assets/images/invoice_light.jpg" alt="Invoice Light Mode" title="Invoice Light Mode" style="width: 30%; height: auto;"/>
  <img src="/flet/src/assets/images/list_light.jpg" alt="List Light Mode" title="List Light Mode" style="width: 30%; height: auto;"/>
</div>

---

## Credits
- Developed by [Galvintec Team](https://www.galvintec.com/) - [Diego Ribas González](https://github.com/DiegoSabir) | [Abel Rodriguez Pastoriza](https://github.com/havelrp).
- Built with [Flet](https://flet.dev/).
- AI-powered invoice analysis powered by [OpenAI](https://openai.com/).

StakeZenith - Simulated Trading Platform

Repository: https://github.com/saulnyongesa/StakeZenith.git

*** DISCLAIMER: FOR EDUCATIONAL AND LEARNING PURPOSES ONLY ***
This project is a simulated financial trading platform built strictly for educational purposes, portfolio demonstration, and learning backend architecture, real-time data visualization, and payment gateway integration. It is NOT a real brokerage or financial application. The creator and contributors are not responsible for any misuse of this software, nor does it provide real financial advice or real-market execution.

-------------------------------------------------------------------

ABOUT THE PROJECT
StakeZenith Trading is a web-based simulation platform designed to mimic the experience of trading digital assets or synthetic markets. It allows users to create accounts, analyze price movements via interactive charts, and execute simulated Buy/Sell orders. 

The project demonstrates full-stack capabilities, integrating a Django backend with a dynamic, responsive frontend. It also features a sandbox payment integration to simulate how users would fund their trading accounts in a real-world scenario.

FEATURES
- Interactive Price Charts: Visual representation of asset price movements using JavaScript charting libraries for technical analysis.
- Order Execution Engine: Simulated market and limit orders allowing users to "Buy" and "Sell" assets in real-time.
- Portfolio Management: Real-time tracking of user balances, open positions, active trades, and historical profit/loss (P&L).
- M-Pesa Integration: 
  * Simulated push-to-phone deposit system via the Daraja API sandbox.
  * Controlled withdrawal system for educational demonstration of payment flows.
- User Authentication: Secure login and registration system protecting user data and trade history.
- Admin Dashboard: Backend controls for managing users, monitoring simulated transactions, and adjusting market parameters.

BUILT WITH
- Frontend: HTML5, TailwindCSS, Vanilla JavaScript, Charting Libraries (e.g., Chart.js / TradingView Lightweight Charts)
- Backend: Django (Python)
- Database: SQLite (Development) / PostgreSQL (Production ready)
- Payments: Safaricom Daraja API (Sandbox)

-------------------------------------------------------------------

GETTING STARTED
Follow these instructions to set up and run the trading platform on your local machine.

Prerequisites
Ensure you have the following installed on your local machine:
- Python (3.8 or higher)
- pip (Python package installer)
- Git

Installation & Setup

1. Clone the repository
   git clone https://github.com/saulnyongesa/StakeZenith.git
   cd StakeZenith

2. Create and activate a virtual environment (Recommended)
   Windows:
   python -m venv venv
   venv\Scripts\activate

   macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. Install backend dependencies
   pip install -r requirements.txt

4. Setup environment variables
   Create a .env file in the root directory to store your Django secret key and Daraja (M-Pesa) API credentials:
   
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   MPESA_CONSUMER_KEY=your_consumer_key
   MPESA_CONSUMER_SECRET=your_consumer_secret
   MPESA_PASSKEY=your_passkey

5. Apply database migrations
   python manage.py makemigrations
   python manage.py migrate

6. Create a superuser (Admin)
   python manage.py createsuperuser

Running the Application
Start the Django development server:
   python manage.py runserver

Open your web browser and navigate to:
   http://127.0.0.1:8000/

-------------------------------------------------------------------

LICENSE
This project is intended for personal portfolio use, technical demonstration, and educational study.

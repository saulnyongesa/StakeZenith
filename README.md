StakeZenith - Aviator Simulation

Repository: https://github.com/saulnyongesa/StakeZenith.git

*** DISCLAIMER: FOR EDUCATIONAL AND LEARNING PURPOSES ONLY ***
This project is a simulation of a crash-style betting game built strictly for educational purposes, portfolio demonstration, and learning UI/UX design, HTML5 Canvas animations, and payment gateway integration. It is NOT a real gambling application. The creator and contributors are not responsible for any misuse of this software.

-------------------------------------------------------------------

ABOUT THE PROJECT
StakeZenith is a web-based crash game simulation inspired by the popular "Aviator" game. It features a fully responsive, highly polished frontend built with TailwindCSS and Vanilla JavaScript, integrated with a Django backend.

The game includes a deterministic (admin-controlled) flight engine, a simulated live betting feed, and seamless UI state management to mimic the tension and interactions of a real-time betting platform.

FEATURES
- HTML5 Canvas Flight Engine: Smooth, mathematical curve rendering with moving background grids and randomized plane wobble for realism.
- Deterministic Crash Sequence: The flight outcomes are read from a predefined array, allowing full administrative control over the simulation.
- Dual Betting Panels: Users can place and manage two simultaneous bets with dynamic multiplier calculations.
- M-Pesa Integration: 
  * Simulated push-to-phone deposit modal.
  * Rigged withdrawal system designed to simulate transaction failures for educational demonstration.
- Micro-Interactions: Loading spinners, strict balance checking, dynamic button states (Bet, Cancel, Cash Out), and sound effects.
- Simulated Live Feed: Auto-generating live bets feed to populate the UI with realistic player activity.

BUILT WITH
- Frontend: HTML5, TailwindCSS, Vanilla JavaScript, SweetAlert2
- Graphics: HTML5 <canvas>, Inline SVG
- Backend: Django (Python)

-------------------------------------------------------------------

GETTING STARTED
Follow these instructions to set up and run the project on your local machine.

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

7. Add the static audio asset
   Ensure you have an audio file named aviator.mpeg (or .mp3 depending on your template setup) placed inside your Django app's static folder so the flight sound plays correctly.

Running the Application
Start the Django development server:
   python manage.py runserver

Open your web browser and navigate to:
   http://127.0.0.1:8000/

-------------------------------------------------------------------

HOW TO CONTROL THE CRASH SEQUENCE
This simulation uses a predetermined array to control exactly when the plane crashes. 

To edit the sequence, open the main HTML template containing the JavaScript engine and locate the crashSequence array:

// --- ADMIN CRASH SEQUENCE ---
// The game will perfectly hit these exact multipliers sequentially.
const crashSequence = [1.12, 2.45, 1.05, 5.50, 1.80, 1.00, 3.45, 12.00, 1.20, 2.10];

Modify these numbers to dictate the outcome of the upcoming rounds. The engine loops back to the beginning of the array once it reaches the end.

-------------------------------------------------------------------

LICENSE
This project is intended for personal portfolio use and educational study.

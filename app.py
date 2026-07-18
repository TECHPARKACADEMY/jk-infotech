import smtplib
import sqlite3
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, flash, redirect, url_for, session

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'jk_infotech_secret_secure_key')
DB_NAME = "queries.db"

# ==========================================================================
# 🔐 ADMIN SECURE STATIC CREDENTIALS SETTINGS
# ==========================================================================
# Render dashboard-la intha variables credentials dynamic-ah update pannikalam
ADMIN_USERNAME = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "JkInfo@26031995")

# ==========================================================================
# ✉️ TITAN WEBMAIL ENVIRONMENT CONFIGURATION
# ==========================================================================
SENDER_EMAIL = os.environ.get("TITAN_EMAIL", "info@jkinfotech.in")
SENDER_PASSWORD = os.environ.get("TITAN_PASSWORD") 
RECEIVER_EMAIL = "info@jkinfotech.in" 

SMTP_SERVER = "smtp.titan.email"
SMTP_PORT = 465  

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_query_to_db(name, email, phone, message):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customer_queries (name, email, phone, message)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, message))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database Storage Error: {e}")
        return False

# Trigger table initializations
init_db()

def send_query_email(customer_name, customer_email, customer_phone, customer_msg):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"🚀 New Contact Inquiry From: {customer_name}"

        body = f"""
==================================================
            NEW CUSTOMER QUERY RECEIVED
==================================================
👤 Name          : {customer_name}
📧 Email Address : {customer_email}
📞 Phone Number  : {customer_phone}
💬 Message / Requirement:
--------------------------------------------------
{customer_msg}
==================================================
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Titan SSL SMTP Engine Critical Error Trace: {e}")
        return False

# ==========================================================================
# 🌐 STANDARD USER INTERFACE PAGES
# ==========================================================================
@app.route('/')
def index(): return render_template('index.html')

@app.route('/about')
def about(): return render_template('about.html')

@app.route('/services')
def services(): return render_template('services.html')

@app.route('/products')
def products(): return render_template('products.html')

@app.route('/training')
def training(): return render_template('training.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        db_saved = save_query_to_db(name, email, phone, message)
        email_sent = send_query_email(name, email, phone, message)
        
        if db_saved and email_sent:
            flash("Thank you! Your inquiry has been registered successfully.", "success")
        elif db_saved and not email_sent:
            flash("Inquiry saved locally, but email server failed to forward.", "warning")
        else:
            flash("Server infrastructure configuration error. Try again later.", "error")
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ==========================================================================
# 🔐 NEW ADMIN CONTROL PANEL LAYERS ROUTING (NO MORE 404!)
# ==========================================================================
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Credentials Entry!", "error")
            
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # Session checking auth logic to prevent direct structural hack bypass
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    # Fetch data directly from SQLite database table layer
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customer_queries ORDER BY timestamp DESC')
    queries = cursor.fetchall()
    conn.close()
    
    return render_template('admin_dashboard.html', queries=queries)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
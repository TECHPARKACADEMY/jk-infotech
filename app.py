import os
import sqlite3
import requests  # Clean Web HTTP API calls tracking bypass for Render
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ============================================================
# FLASK APP CONFIGURATION
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "jk_infotech_secret_secure_key"
)


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "queries.db"


# ============================================================
# ADMIN LOGIN
# ============================================================

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USER",
    "admin"
)

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASS",
    "JkInfo@26031995"
)


# ============================================================
# BREVO EMAIL API CONFIGURATION
# ============================================================

# SENDER_EMAIL matches verified identity info@jkinfotech.in
SENDER_EMAIL = os.environ.get("TITAN_EMAIL", "info@jkinfotech.in")
RECEIVER_EMAIL = "info@jkinfotech.in"


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


# ============================================================
# SAVE QUERY TO DATABASE
# ============================================================

def save_query_to_db(name, email, phone, message):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customer_queries
            (name, email, phone, message)
            VALUES (?, ?, ?, ?)
        """, (name, email, phone, message))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("DATABASE ERROR")
        print(e)
        return False


# ============================================================
# INITIALIZE DATABASE
# ============================================================
init_db()


# ============================================================
# SEND EMAIL FUNCTION (VIA BREVO HTTP API)
# ============================================================

def send_query_email(customer_name, customer_email, customer_phone, customer_msg):
    try:
        # 🚀 Reading using the clean, exact named variable from Render config setup screen
        api_key = os.environ.get("BREVO_API_KEY")
        if not api_key:
            print("ERROR: BREVO_API_KEY ENVIRONMENT VARIABLE MISSING")
            return False

        url = "https://api.brevo.com/v3/smtp/email"
        
        headers = {
            "accept": "application/json",
            "api-key": api_key,
            "content-type": "application/json"
        }

        body_content = f"""
====================================================
NEW CUSTOMER ENQUIRY
====================================================
Name      : {customer_name}
Email     : {customer_email}
Phone     : {customer_phone}
----------------------------------------------------
Message:
----------------------------------------------------
{customer_msg}
====================================================
"""

        payload = {
            "sender": {"name": "JK Infotech Website", "email": SENDER_EMAIL},
            "to": [{"email": RECEIVER_EMAIL, "name": "Admin Info"}],
            "subject": f"New Contact Inquiry - {customer_name}",
            "textContent": body_content
        }

        # Secure HTTP protocol triggers to bypass Render timeout walls
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        
        if response.status_code in [200, 201, 202]:
            print("EMAIL SENT SUCCESSFULLY VIA BREVO API")
            return True
        else:
            print(f"BREVO API ERROR: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print("EMAIL TRANSMISSION API ERROR")
        print(e)
        return False


# ============================================================
# USER PAGES
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/training")
def training():
    return render_template("training.html")


# ============================================================
# CONTACT PAGE
# ============================================================

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")

        db_saved = save_query_to_db(name, email, phone, message)
        email_sent = False

        try:
            email_sent = send_query_email(name, email, phone, message)
        except Exception as e:
            print("Contact routing email trigger error:", e)

        if db_saved and email_sent:
            flash(
                "Thank you! Your enquiry has been submitted successfully.",
                "success"
            )
        elif db_saved:
            flash(
                "Your enquiry has been saved successfully. Email notification could not be sent.",
                "warning"
            )
        else:
            flash(
                "Something went wrong. Please try again later.",
                "danger"
            )

        return redirect(url_for("contact"))

    return render_template("contact.html")


# ============================================================
# ADMIN LOGIN
# ============================================================

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("Login Successful.", "success")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid Username or Password.", "danger")

    return render_template("admin_login.html")


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        flash("Please login first.", "warning")
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM customer_queries
        ORDER BY timestamp DESC
    """)
    queries = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", queries=queries)


# ============================================================
# DELETE QUERY
# ============================================================

@app.route("/delete_query/<int:query_id>")
def delete_query(query_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM customer_queries WHERE id=?",
            (query_id,)
        )
        conn.commit()
        conn.close()
        flash("Customer enquiry deleted successfully.", "success")
    except Exception as e:
        print(e)
        flash("Unable to delete enquiry.", "danger")

    return redirect(url_for("admin_dashboard"))


# ============================================================
# ADMIN LOGOUT
# ============================================================

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("admin_login"))


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
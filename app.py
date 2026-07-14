import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'jk_infotech_secret_secure_key'

# ✉️ EMAIL CONFIGURATION HUB
SENDER_EMAIL = "your-gmail-username@gmail.com" 
SENDER_PASSWORD = "your-app-password" # Add your 16-character App Password here
RECEIVER_EMAIL = "jk8056828383@gmail.com"  

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
👤 Name         : {customer_name}
📧 Email Address : {customer_email}
📞 Phone Number  : {customer_phone}
💬 Message / Requirement:
--------------------------------------------------
{customer_msg}
==================================================
        """
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls() 
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/training')
def training():
    return render_template('training.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        if send_query_email(name, email, phone, message):
            flash("Thank you! Your message has been sent successfully.", "success")
        else:
            flash("Server error. Please contact via WhatsApp.", "error")
        return redirect(url_for('contact'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
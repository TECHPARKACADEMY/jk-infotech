from flask import Flask, render_template, request

app = Flask(__name__)

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
        # Logic to handle corporate quote entries can be integrated here safely
        pass
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
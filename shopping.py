from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "super-secret-key-for-demo"

# Fake Products
PRODUCTS = [
    {"id":1,"name":"Sony Headphones","price":398,"category":"electronics","image":"https://picsum.photos/id/20/300/300"},
    {"id":2,"name":"Nike Sneakers","price":129,"category":"fashion","image":"https://picsum.photos/id/201/300/300"},
    {"id":3,"name":"Instant Pot","price":89,"category":"home","image":"https://picsum.photos/id/251/300/300"},
    {"id":4,"name":"Samsung Watch","price":279,"category":"electronics","image":"https://picsum.photos/id/180/300/300"},
    {"id":5,"name":"Dyson Vacuum","price":649,"category":"home","image":"https://picsum.photos/id/64/300/300"},
]

# Weak Admin Credentials (for Hydra demo)
ADMIN_CREDENTIALS = {
    "admin": "password123",
    "admin123": "admin",
    "user": "123456"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['admin'] = True
            return jsonify({"status": "success", "message": "Login Successful!"})
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    return render_template('index.html', show_admin=True)

@app.route('/api/products')
def get_products():
    return jsonify(PRODUCTS)

@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    return jsonify({"status": "success", "message": "Added to cart (Fake)"})

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

if __name__ == '__main__':
    print("🌐 PrimeCart Started → http://127.0.0.1:5000")
    print("Admin Login: http://127.0.0.1:5000/admin")
    print("Weak password example: admin / password123")
    app.run(debug=True, port=5000)

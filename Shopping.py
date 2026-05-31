from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulated products
PRODUCTS = [
    {"id": 1, "name": "Sony WH-1000XM5", "price": 398, "category": "electronics", "image": "https://picsum.photos/id/20/300/300"},
    {"id": 2, "name": "Nike Air Max", "price": 129, "category": "fashion", "image": "https://picsum.photos/id/201/300/300"},
    {"id": 3, "name": "Instant Pot", "price": 89, "category": "home", "image": "https://picsum.photos/id/251/300/300"},
    {"id": 4, "name": "Samsung Watch", "price": 279, "category": "electronics", "image": "https://picsum.photos/id/180/300/300"},
    {"id": 5, "name": "Dyson Vacuum", "price": 649, "category": "home", "image": "https://picsum.photos/id/64/300/300"},
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('index.html', active='shop')

@app.route('/cart')
def cart():
    return render_template('index.html', active='cart')

@app.route('/search')
def google_search():
    query = request.args.get('q', '')
    # Simulate Google-like search
    results = [p for p in PRODUCTS if query.lower() in p['name'].lower()]
    return jsonify({"query": query, "results": results or PRODUCTS})

@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    return jsonify({"status": "success", "product": data})

if __name__ == '__main__':
    print("🌐 PrimeCart running → http://localhost:5000")
    print("Directories: /, /shop, /cart")
    app.run(debug=True, port=5000)

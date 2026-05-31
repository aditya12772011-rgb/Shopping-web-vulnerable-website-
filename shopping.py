from flask import Flask, render_template_string, jsonify, request
import json

app = Flask(__name__)

# ==================== HTML + CSS + JS (All in one) ====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PrimeCart - Shop Everything</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');
        
        body { font-family: 'Inter', system-ui, sans-serif; }
        .hero-bg {
            background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)), 
                        url('https://picsum.photos/id/1015/2000/800');
            background-size: cover;
            background-position: center;
        }
        .product-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .product-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25);
        }
        .nav-link:after {
            content: ''; position: absolute; width: 0; height: 2px; bottom: -2px; left: 0;
            background-color: #2563eb; transition: width 0.3s;
        }
        .nav-link:hover:after { width: 100%; }
    </style>
</head>
<body class="bg-gray-50">

    <!-- HEADER -->
    <header class="bg-white border-b sticky top-0 z-50 shadow">
        <div class="max-w-7xl mx-auto px-6">
            <!-- Top Bar -->
            <div class="bg-blue-600 text-white text-sm py-2">
                <div class="flex justify-between items-center">
                    <div>Free Shipping on Orders Over $50 | 30-Day Returns</div>
                    <div>Hello, AaditYa | Prime Member</div>
                </div>
            </div>

            <!-- Main Header -->
            <div class="py-4 flex items-center justify-between">
                <div onclick="navigateTo('home')" class="flex items-center gap-2 cursor-pointer">
                    <span class="text-4xl font-bold text-blue-600">prime</span>
                    <span class="text-4xl font-bold">cart</span>
                </div>

                <div class="flex-1 max-w-2xl mx-8">
                    <div class="relative">
                        <input id="search-input" type="text" 
                               placeholder="Search in PrimeCart..." 
                               class="w-full border border-gray-300 rounded-full py-3 px-6 focus:outline-none focus:border-blue-500"
                               onkeyup="if(event.key==='Enter') searchProducts()">
                        <button onclick="searchProducts()" 
                                class="absolute right-3 top-1/2 -translate-y-1/2 bg-blue-600 text-white px-8 py-2 rounded-full">
                            <i class="fas fa-search"></i>
                        </button>
                    </div>
                </div>

                <div class="flex items-center gap-8">
                    <div onclick="toggleWishlist()" class="cursor-pointer hover:text-blue-600">
                        <i class="fas fa-heart text-2xl"></i>
                    </div>
                    <div onclick="toggleCart()" class="relative cursor-pointer hover:text-blue-600">
                        <i class="fas fa-shopping-cart text-2xl"></i>
                        <span id="cart-count" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">0</span>
                    </div>
                </div>
            </div>

            <!-- Categories -->
            <nav class="flex gap-8 text-sm font-medium border-t py-3 overflow-x-auto">
                <a onclick="filterCategory('all')" class="nav-link cursor-pointer text-blue-600">All</a>
                <a onclick="filterCategory('electronics')" class="nav-link cursor-pointer hover:text-blue-600">Electronics</a>
                <a onclick="filterCategory('fashion')" class="nav-link cursor-pointer hover:text-blue-600">Fashion</a>
                <a onclick="filterCategory('home')" class="nav-link cursor-pointer hover:text-blue-600">Home & Kitchen</a>
                <a onclick="filterCategory('beauty')" class="nav-link cursor-pointer hover:text-blue-600">Beauty</a>
                <a onclick="filterCategory('sports')" class="nav-link cursor-pointer hover:text-blue-600">Sports</a>
                <a onclick="filterCategory('books')" class="nav-link cursor-pointer hover:text-blue-600">Books</a>
            </nav>
        </div>
    </header>

    <!-- HERO -->
    <div class="hero-bg h-[500px] flex items-center text-white">
        <div class="max-w-7xl mx-auto px-6">
            <h1 class="text-6xl font-bold mb-4">Big Summer Sale</h1>
            <p class="text-2xl mb-8">Up to 70% OFF on Top Brands</p>
            <button onclick="shopNow()" 
                    class="bg-white text-blue-700 px-10 py-4 rounded-full text-xl font-semibold hover:bg-gray-100">
                Shop Now →
            </button>
        </div>
    </div>

    <main class="max-w-7xl mx-auto px-6 py-10">
        <h2 class="text-3xl font-bold mb-6">Featured Products</h2>
        
        <div id="products-grid" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            <!-- Populated by JavaScript -->
        </div>
    </main>

    <!-- CART SIDEBAR -->
    <div id="cart-sidebar" class="fixed top-0 right-0 h-full w-96 bg-white shadow-2xl transform translate-x-full transition-all duration-300 z-50">
        <div class="h-full flex flex-col">
            <div class="p-6 border-b flex justify-between items-center">
                <h3 class="text-2xl font-semibold">Your Cart</h3>
                <button onclick="toggleCart()" class="text-4xl">×</button>
            </div>
            <div id="cart-items" class="flex-1 p-6 overflow-auto"></div>
            <div class="p-6 border-t">
                <div class="flex justify-between text-xl mb-4">
                    <span>Total</span>
                    <span id="cart-total" class="font-bold">$0</span>
                </div>
                <button onclick="checkout()" 
                        class="w-full bg-blue-600 text-white py-4 rounded-2xl text-lg font-semibold">
                    Proceed to Checkout
                </button>
            </div>
        </div>
    </div>

    <script>
        let products = [
            {id:1, name:"Sony WH-1000XM5", price:398, category:"electronics", image:"https://picsum.photos/id/20/300/300", rating:4.8},
            {id:2, name:"Nike Air Max 270", price:129, category:"fashion", image:"https://picsum.photos/id/201/300/300", rating:4.6},
            {id:3, name:"Instant Pot 7-in-1", price:89, category:"home", image:"https://picsum.photos/id/251/300/300", rating:4.9},
            {id:4, name:"Samsung Galaxy Watch 6", price:279, category:"electronics", image:"https://picsum.photos/id/180/300/300", rating:4.7},
            {id:5, name:"Dyson V15 Vacuum", price:649, category:"home", image:"https://picsum.photos/id/64/300/300", rating:4.5},
            {id:6, name:"The Psychology of Money", price:18, category:"books", image:"https://picsum.photos/id/201/300/300", rating:4.8},
            {id:7, name:"MacBook Air M3", price:1099, category:"electronics", image:"https://picsum.photos/id/20/300/300", rating:5},
            {id:8, name:"Lakmé Beauty Kit", price:45, category:"beauty", image:"https://picsum.photos/id/64/300/300", rating:4.4}
        ];

        let cart = [];

        function renderProducts(filteredProducts) {
            const grid = document.getElementById('products-grid');
            grid.innerHTML = '';
            
            filteredProducts.forEach(product => {
                const div = document.createElement('div');
                div.className = "product-card bg-white rounded-3xl overflow-hidden cursor-pointer";
                div.innerHTML = `
                    <img src="${product.image}" class="w-full h-56 object-cover">
                    <div class="p-5">
                        <h3 class="font-semibold text-lg line-clamp-2">${product.name}</h3>
                        <p class="text-2xl font-bold mt-2">$${product.price}</p>
                        <button onclick="addToCart(${product.id}); event.stopImmediatePropagation()" 
                                class="mt-4 w-full bg-blue-600 text-white py-3 rounded-2xl font-medium">
                            Add to Cart
                        </button>
                    </div>
                `;
                div.onclick = () => alert(`Product: ${product.name}\\nPrice: $${product.price}`);
                grid.appendChild(div);
            });
        }

        function addToCart(id) {
            const product = products.find(p => p.id === id);
            const existing = cart.find(item => item.id === id);
            if (existing) existing.quantity = (existing.quantity || 1) + 1;
            else cart.push({...product, quantity: 1});
            
            document.getElementById('cart-count').textContent = cart.reduce((a, c) => a + (c.quantity || 1), 0);
            showToast(`${product.name} added to cart!`);
        }

        function toggleCart() {
            const sidebar = document.getElementById('cart-sidebar');
            if (sidebar.classList.contains('translate-x-full')) {
                renderCart();
                sidebar.classList.remove('translate-x-full');
            } else {
                sidebar.classList.add('translate-x-full');
            }
        }

        function renderCart() {
            let html = '';
            let total = 0;
            cart.forEach((item, i) => {
                const itemTotal = item.price * (item.quantity || 1);
                total += itemTotal;
                html += `
                    <div class="flex gap-4 mb-6">
                        <img src="${item.image}" class="w-20 h-20 object-cover rounded-2xl">
                        <div class="flex-1">
                            <p class="font-medium">${item.name}</p>
                            <p class="text-blue-600">$${item.price}</p>
                            <div class="flex gap-3 mt-2">
                                <button onclick="changeQty(${i}, -1)" class="px-3 border rounded">-</button>
                                <span>${item.quantity || 1}</span>
                                <button onclick="changeQty(${i}, 1)" class="px-3 border rounded">+</button>
                            </div>
                        </div>
                        <p class="font-bold">$${itemTotal}</p>
                    </div>`;
            });
            document.getElementById('cart-items').innerHTML = html || '<p class="text-center text-gray-400 py-10">Cart is empty</p>';
            document.getElementById('cart-total').textContent = '$' + total;
        }

        function changeQty(index, change) {
            cart[index].quantity = Math.max(1, (cart[index].quantity || 1) + change);
            renderCart();
        }

        function checkout() {
            if (cart.length === 0) return;
            alert("🎉 Thank you for shopping with PrimeCart! (Demo Order Placed)");
            cart = [];
            document.getElementById('cart-count').textContent = '0';
            toggleCart();
        }

        function searchProducts() {
            const query = document.getElementById('search-input').value.toLowerCase();
            const filtered = products.filter(p => p.name.toLowerCase().includes(query));
            renderProducts(filtered.length ? filtered : products);
        }

        function filterCategory(cat) {
            if (cat === 'all') renderProducts(products);
            else renderProducts(products.filter(p => p.category === cat));
        }

        function shopNow() {
            window.scrollTo({top: 600, behavior: 'smooth'});
        }

        function showToast(msg) {
            const t = document.createElement('div');
            t.style.cssText = 'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#1f2937;color:white;padding:16px 24px;border-radius:9999px;z-index:9999;';
            t.textContent = msg;
            document.body.appendChild(t);
            setTimeout(() => t.remove(), 2000);
        }

        function navigateTo(page) {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        // Initialize
        window.onload = () => renderProducts(products);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# Optional API
@app.route('/api/products')
def get_products():
    return jsonify([])

if __name__ == '__main__':
    print("🚀 PrimeCart is running at http://localhost:5000")
    app.run(debug=True, port=5000)

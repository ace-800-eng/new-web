import os
from flask import Flask, render_template, redirect, url_for, session, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

# ---------------------------------------------------------------------------
# In-memory product catalog (in a real app this would live in a database)
# ---------------------------------------------------------------------------
PRODUCTS = [
    {
        "id": "orbit-phone-15",
        "name": "Orbit Phone 15",
        "tagline": "Titanium. Turbocharged.",
        "category": "Phone",
        "price": 999,
        "color_options": ["Natural Titanium", "Blue Titanium", "White Titanium", "Black Titanium"],
        "description": (
            "A leap forward for the phone that changed everything. Forged from "
            "aerospace-grade titanium, with a display that stretches edge to edge "
            "and a chip that makes everything feel instant."
        ),
        "specs": ["6.7-inch Super Retina display", "A18 chip", "48MP camera system", "Up to 29 hours video playback"],
        "gradient": "linear-gradient(135deg, #e8e9eb 0%, #b8bcc4 100%)",
        "hero_emoji": "📱",
    },
    {
        "id": "orbit-book-pro",
        "name": "Orbit Book Pro",
        "tagline": "Mind-blowing. Head-turning.",
        "category": "Laptop",
        "price": 1999,
        "color_options": ["Space Black", "Silver"],
        "description": (
            "The most advanced laptop for the most demanding work. A stunning "
            "Liquid Retina XDR display, all-day battery life, and enough power "
            "to edit, render, and build without ever slowing down."
        ),
        "specs": ['16.2-inch Liquid Retina XDR display', "M4 Pro chip", "22-hour battery life", "1TB SSD storage"],
        "gradient": "linear-gradient(135deg, #3a3a3c 0%, #1d1d1f 100%)",
        "hero_emoji": "💻",
    },
    {
        "id": "orbit-watch-ultra",
        "name": "Orbit Watch Ultra",
        "tagline": "Adventure awaits.",
        "category": "Watch",
        "price": 799,
        "color_options": ["Titanium", "Black Titanium"],
        "description": (
            "Built for the extremes. A rugged titanium case, the brightest "
            "display yet, and precision dual-frequency GPS so you're always "
            "exactly where you think you are."
        ),
        "specs": ["49mm titanium case", "3000 nits display", "36-hour battery life", "100m water resistance"],
        "gradient": "linear-gradient(135deg, #d97b3f 0%, #8a4a1f 100%)",
        "hero_emoji": "⌚",
    },
    {
        "id": "orbit-pods-pro",
        "name": "Orbit Pods Pro",
        "tagline": "Hear, and be heard, differently.",
        "category": "Audio",
        "price": 249,
        "color_options": ["White"],
        "description": (
            "Immersive sound, re-engineered. Adaptive noise cancellation "
            "adjusts to your environment in real time, so all you hear is "
            "what you want to hear."
        ),
        "specs": ["Active noise cancellation", "Adaptive audio", "Up to 6 hours listening time", "MagSafe charging case"],
        "gradient": "linear-gradient(135deg, #f5f5f7 0%, #d2d2d7 100%)",
        "hero_emoji": "🎧",
    },
    {
        "id": "orbit-pad-air",
        "name": "Orbit Pad Air",
        "tagline": "Light. Bright. Full of might.",
        "category": "Tablet",
        "price": 599,
        "color_options": ["Blue", "Purple", "Starlight", "Space Gray"],
        "description": (
            "Serious performance in a thin, light design. A stunning Liquid "
            "Retina display and all-day battery make it the ultimate everyday "
            "companion for work and play."
        ),
        "specs": ["10.9-inch Liquid Retina display", "M2 chip", "10-hour battery life", "Compatible with stylus"],
        "gradient": "linear-gradient(135deg, #7c9cbf 0%, #4a6b8a 100%)",
        "hero_emoji": "📱",
    },
    {
        "id": "orbit-mini",
        "name": "Orbit Mini",
        "tagline": "Big things, small package.",
        "category": "Phone",
        "price": 699,
        "color_options": ["Midnight", "Starlight", "Pink", "Blue"],
        "description": (
            "All the power of Orbit, scaled down to fit in your pocket and "
            "the palm of your hand. Compact doesn't mean compromise."
        ),
        "specs": ["5.4-inch Super Retina display", "A17 chip", "Dual-camera system", "Up to 20 hours video playback"],
        "gradient": "linear-gradient(135deg, #f7a8b8 0%, #e06b8a 100%)",
        "hero_emoji": "📱",
    },
]


def get_product(product_id):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def get_cart_items():
    """Resolve session cart (id -> qty) into full product dicts with line totals."""
    cart = session.get("cart", {})
    items = []
    total = 0
    for product_id, qty in cart.items():
        product = get_product(product_id)
        if product:
            line_total = product["price"] * qty
            total += line_total
            items.append({**product, "qty": qty, "line_total": line_total})
    return items, total


@app.context_processor
def inject_cart_count():
    cart = session.get("cart", {})
    return {"cart_count": sum(cart.values())}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.route("/product/<product_id>")
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("index"))
    return render_template("product.html", product=product)


@app.route("/cart/add/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    if not get_product(product_id):
        return redirect(url_for("index"))
    cart = session.get("cart", {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session["cart"] = cart
    return redirect(request.referrer or url_for("index"))


@app.route("/cart/remove/<product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    if product_id in cart:
        del cart[product_id]
        session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/cart/decrease/<product_id>", methods=["POST"])
def decrease_qty(product_id):
    cart = session.get("cart", {})
    if product_id in cart:
        cart[product_id] -= 1
        if cart[product_id] <= 0:
            del cart[product_id]
        session["cart"] = cart
    return redirect(url_for("view_cart"))


@app.route("/cart")
def view_cart():
    items, total = get_cart_items()
    return render_template("cart.html", items=items, total=total)


@app.route("/checkout", methods=["POST"])
def checkout():
    session["cart"] = {}
    return render_template("checkout.html")


if __name__ == "__main__":
    # debug=True is fine locally, but never in production.
    # Elastic Beanstalk runs this via gunicorn (see Procfile), not this block.
    app.run(debug=False)

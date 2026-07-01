# Orbit Store

A small Flask storefront styled after Apple's product pages — sticky blurred nav,
big hero sections, product grid, a bag/cart, and checkout flow.

## Run it

```bash
pip install flask
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Structure

```
app.py                  Routes, in-memory product catalog, session-based cart
templates/
  base.html             Nav + footer shell
  index.html            Homepage — hero + product grid by category
  product.html          Product detail page
  cart.html             Bag page
  checkout.html         Order confirmation
static/css/style.css    All styling
```

## Notes

- Products live in a Python list in `app.py` — swap this for a database (SQLite,
  Postgres, etc.) for a real app.
- The cart is stored in the Flask session, so it's per-browser and resets when
  the session cookie clears.
- "Orbit" is a fictional brand invented for this demo, not a real company.

from flask import Flask, render_template, request, session
from data import db_session
from data.products import Product

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/products', methods=['GET', 'POST'])
def products():
    db_sess = db_session.create_session()

    if request.method == 'POST':
        product_id = request.form.get('product_id')
        if product_id:
            # add the product to the cart in the session
            if 'cart' not in session:
                session['cart'] = {}
            cart = session['cart']
            cart[product_id] = cart.get(product_id, 0) + 1
            session['cart'] = cart

    products = db_sess.query(Product).all()

    # render the HTML template and pass in the products data
    return render_template('products.html', products=products)


def main():
    db_session.global_init("db/goods.db")
    app.run()


if __name__ == '__main__':
    main()
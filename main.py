from flask import Flask, render_template, request, session, redirect, url_for
from data import db_session
from data.products import Product
from data.users import User
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/products')
    return render_template('register.html', title='Регистрация', form=form)


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
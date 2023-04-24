from flask import Flask, render_template, request, session, redirect, jsonify
from flask_restful import Resource, Api
from flask_login import LoginManager, login_user, login_required, logout_user
from data import db_session
from data.products import Product
from data.users import User
from forms.user import RegisterForm, LoginForm
from resources.resources import ProductResource, ProductListResource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:product_id>')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    db_sess = db_session.create_session()

    return render_template('index.html')


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
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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


@app.route('/cart')
def cart():
    db_sess = db_session.create_session()

    cart = session.get('cart', {})

    product_ids = list(cart.keys())

    products = db_sess.query(Product).filter(Product.id.in_(product_ids)).all()

    total = sum([product.price * cart[str(product.id)] for product in products])

    return render_template('cart.html', products=products, cart=cart, total=total)


def main():
    db_session.global_init("db/goods.db")
    app.run()


if __name__ == '__main__':
    main()
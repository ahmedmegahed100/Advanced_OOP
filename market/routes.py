from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

from market.services import user_service
from market.services.ItemServiceImpl import ItemServiceImpl
from market.services.base_service import BaseService
from market.services.item_service import ItemService
from market.services.user_service import UserService
user_service: BaseService = UserService()
item_service: ItemService = ItemServiceImpl()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        if item_service.purchase_item(purchased_item, current_user.id):
            flash(f"Congratulations! You purchased {purchased_item}!", category='success')
        else:
            flash(f"Unfortunately, you don't have enough money to purchase {purchased_item}!", category='danger')

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        if item_service.sell_item(sold_item, current_user.id):
            flash(f"Congratulations! You sold {sold_item} back to market!", category='success')
        else:
            flash(f"Something went wrong with selling {sold_item}", category='danger')

        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = item_service.get_all_items()
        owned_items = item_service.get_owned_items(current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email_address.data
        password = form.password1.data
        if user_service.register_user(username, email, password):
            # Registration successful
            flash(f"Account created successfully! You are now logged in as {username}", category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or email address already exists! Please try a different one', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = user_service.login_user(username, password)
        if user:
            login_user(user)
            flash(f'Success! You are logged in as: {username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))











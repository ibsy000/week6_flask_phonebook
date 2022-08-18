from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import PhonebookForm, LoginForm
from app.models import Entry, LoginUser


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    form = PhonebookForm()

    if form.validate_on_submit():
        print('Form has been validated! Yippee Ki-Yay!')
        name = form.name.data
        phone_number = form.phone_number.data
        street_address = form.street_address.data
        city = form.city.data
        state = form.state.data
        email = form.email.data
        
        new_entry = Entry(name=name, phone_number=phone_number, street_address=\
            street_address, city=city, state=state, email=email)
        print(f"{new_entry.name} has been added to entries.")
        
    return render_template('add_entry.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print('Form has been validated! Yippee Ki-Yay!')
        email = form.email.data
        password = form.password.data
        logged_in = LoginUser(email=email, password=password)

        flash(f"{logged_in.email} has logged in successfully", "success")
        return redirect(url_for('add_entry'))

    return render_template('login.html', form=form)
    
from app import app
from flask import render_template, redirect, url_for, flash
from app.forms import PhonebookForm, LoginForm, SignUpForm
from app.models import Entry, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    entries = Entry.query.all()
    return render_template('index.html', entries=entries)

@app.route('/add-entry', methods=['GET', 'POST'])
@login_required # user has to be logged in, into order to add entries
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
            street_address, city=city, state=state, email=email, user_id=current_user.id)

        # add a flash message once an entry has been added
        flash(f'{new_entry.name} has been added to your phonebook entries!', 'success')
        print(f"{new_entry.name} has been added to entries.")

        # after entry is created send user back to home page
        return redirect(url_for('index'))
        
    return render_template('add_entry.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print('Form has been validated! Yippee Ki-Yay!')
        # get username and password from form
        username = form.username.data
        password = form.password.data
        # Query the user table for a user with the same username as the form 
        confirm_user = User.query.filter_by(username=username).first()

        # if the user exists and the password is correct for that user
        if confirm_user is not None and confirm_user.check_password(password):
            # log the user in with the login_user function form flask_login
            login_user(confirm_user)
            # flash a success message
            flash(f"Welcome back! {confirm_user.username} has logged in successfully", "success")
            # redirect back to the home page
            return redirect(url_for('index'))
        # if no user with that username or password is incorrect
        else:
            # flash a danger message
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        print('Form has been validated! Hooray!!!')

        email = form.email.data
        username = form.username.data
        password = form.password.data
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()

        if existing_user:
            flash("A user with that username or email already exists.", "danger")
            return redirect(url_for('signup')) 

        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have successfully logged out. Thanks for coming by!', 'success')
    return redirect(url_for('index'))
    

@app.route('/<entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry_to_edit = Entry.query.get_or_404(entry_id)

    # make sure the entry to edit is owned by the current user
    if entry_to_edit.owner != current_user:
        flash('You do not have permission to edit this entry', 'danger')
        return redirect(url_for('login'))

    form = PhonebookForm()
    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        street_address = form.street_address.data
        city = form.city.data
        state = form.state.data
        email = form.email.data

        entry_to_edit.update(name=name, phone_number=phone_number, street_address=\
            street_address, city=city, state=state, email=email)
        flash(f'{entry_to_edit.name} has been updated!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_entry.html', entry=entry_to_edit, form=form)


@app.route('/<entry_id>/delete')
@login_required
def delete_entry(entry_id):
    entry_to_delete = Entry.query.get_or_404(entry_id)

    if entry_to_delete.owner != current_user:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('index'))
    
    entry_to_delete.delete()
    flash(f'{entry_to_delete.name} has been deleted.', 'success')

    return redirect(url_for('index'))
from app import app
from flask import render_template
from app.forms import PhonebookForm


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = PhonebookForm()
    if form.validate_on_submit():
        print('Form has been validated! Yippee Ki-Yay!')
        # name = form.name.data
        # address = form.address.data
        # phone_number = form.phone_number.data
        # email = form.email.data
        # new_entry = 
    return render_template('register.html', form=form)
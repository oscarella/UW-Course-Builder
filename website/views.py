from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Term

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        name = request.form.get('new_name')
        if not name:
            flash('The title cannot be empty.', category='error')
        elif len(name) > 20:
            flash('The term\'s title should be maximum 20 characters.', category='error')
        else:
            flash('Term has been successfully created.', category='success')
            new_term = Term(name=name)
            current_user.terms.append(new_term)
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)

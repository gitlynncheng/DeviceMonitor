import json
import time

from flask import Blueprint
from flask import Flask, render_template, jsonify, request, redirect, flash, url_for

# 從其他.py裡import的內容
from main import app, db
from models import Permission, User
from database import Database
from decorators import permission_required

# login功能使用
from models import login_manager
from forms import RegistrationForm, ServerAdd, ServerModify
from flask_login import login_required

from datetime import datetime

# 使用configparser
configparserdb = Database()
subregister = Blueprint('subregister', __name__)

# register
@subregister.route('/register', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.Admin)
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('subdashboard.dashboard'))
    return render_template('register.html', form=form, current_time=datetime.utcnow())

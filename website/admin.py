from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Customer
from flask_sqlalchemy import SQLAlchemy
from . import db
from flask_login import login_user, logout_user, login_required, current_user
import hashlib

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def dashboard():
    return render_template('admin/dashboard.html')
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('user/index.html',user=current_user)

@views.route('/product')
def product():
    return render_template('user/product.html')

@views.route('/about')
def about():
    return render_template('user/about.html')

@views.route('/testimonial')
def testimonial():
    return render_template('user/testimonial.html')

@views.route('/blog_list')
def blog_list():
    return render_template('user/blog_list.html')

@views.route('/contact')
def contact():
    return render_template('user/contact.html')

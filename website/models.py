from . import db
from flask_login import UserMixin

class Customer(db.Model,UserMixin):
    __tablename__ = 'Customer'
    
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cus_name = db.Column(db.String(256))
    cus_email = db.Column(db.String(256))
    cus_phone = db.Column(db.String(10))
    cus_username = db.Column(db.String(50), unique=True)
    cus_password = db.Column(db.String(100))
    cus_group = db.Column(db.String(50), default='silver')
    total_spent = db.Column(db.Numeric(10, 2), default=0)
      # Nếu không kế thừa UserMixin, thêm phương thức get_id():
    def get_id(self):
        return str(self.cus_id)
    
    # # Khóa ngoại đến bảng Orders
    # orders = db.relationship('Order', backref='customer', lazy=True)
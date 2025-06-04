from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db

class Customer(db.Model):
    __tablename__ = 'Customer'
    cus_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cus_name = db.Column(db.String(256))
    cus_email = db.Column(db.String(256), unique=True)
    cus_phone = db.Column(db.String(10))
    cus_username = db.Column(db.String(50), unique=True)
    cus_password = db.Column(db.String(64))  # store hashed password
    cus_group = db.Column(db.String(50), default='Silver')
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    total_spent = db.Column(db.Numeric(10, 2), default=0)
    def get_id(self):
        # trả về id user dưới dạng string
        return str(self.cus_id)
class Supplier(db.Model):
    __tablename__ = 'Supplier'
    supply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supply_name = db.Column(db.String(256))

class Catalogue(db.Model):
    __tablename__ = 'Catalogue'
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(256))

class Products(db.Model):
    __tablename__ = 'Products'
    prod_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prod_name = db.Column(db.String(256))
    prod_received = db.Column(db.Integer)
    prod_sold = db.Column(db.Integer)
    # prod_stock là trường tính toán: prod_received - prod_sold, bạn có thể làm property
    prod_price = db.Column(db.Numeric(10, 2))
    prod_discount = db.Column(db.Numeric(5, 2))
    cat_id = db.Column(db.Integer, db.ForeignKey('Catalogue.cat_id'))
    supply_id = db.Column(db.Integer, db.ForeignKey('Supplier.supply_id'))
    prod_description = db.Column(db.Text)

    catalogue = db.relationship('Catalogue', backref='products')
    supplier = db.relationship('Supplier', backref='products')

    @property
    def prod_stock(self):
        return (self.prod_received or 0) - (self.prod_sold or 0)

class Coupon(db.Model):
    __tablename__ = 'Coupon'
    coupon_code = db.Column(db.String(50), primary_key=True)
    discount_type = db.Column(db.String(10))  # 'percentage' or 'fixed'
    discount_value = db.Column(db.Numeric(10, 2))
    min_order_value = db.Column(db.Numeric(10, 2))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    usage_limit = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(10), default='active')  # 'active' or 'inactive'
    customer_group = db.Column(db.String(50))

class CouponShip(db.Model):
    __tablename__ = 'Coupon_Ship'
    couponship_code = db.Column(db.String(50), primary_key=True)
    discount_type = db.Column(db.String(10))
    discount_value = db.Column(db.Numeric(10, 2))
    min_order_value = db.Column(db.Numeric(10, 2))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    usage_limit = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(10), default='active')
    customer_group = db.Column(db.String(50))

class Orders(db.Model):
    __tablename__ = 'Orders'
    orders_id = db.Column(db.String(10), primary_key=True)  # char(10)
    orders_date = db.Column(db.Date, default=datetime.utcnow)
    cus_id = db.Column(db.Integer, db.ForeignKey('Customer.cus_id'))
    orders_status = db.Column(db.String(20))  # pending, shipped, completed, cancelled
    orders_total = db.Column(db.Numeric(10, 2), default=0)
    shipping_fee = db.Column(db.Numeric(10, 2), default=0)
    coupon_code = db.Column(db.String(50), db.ForeignKey('Coupon.coupon_code'))
    couponship_code = db.Column(db.String(50), db.ForeignKey('Coupon_Ship.couponship_code'))

    customer = db.relationship('Customer', backref='orders')
    coupon = db.relationship('Coupon', backref='orders')
    coupon_ship = db.relationship('CouponShip', backref='orders')
    order_details = db.relationship('OrderDetails', backref='order', cascade="all, delete-orphan")

class OrderDetails(db.Model):
    __tablename__ = 'OrderDetails'
    ordersdtl_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orders_id = db.Column(db.String(10), db.ForeignKey('Orders.orders_id'))
    prod_id = db.Column(db.Integer, db.ForeignKey('Products.prod_id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))

    product = db.relationship('Products', backref='order_details')

class RoleAdmins(db.Model):
    __tablename__ = 'roleAdmins'
    role_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)

class Admins(db.Model):
    __tablename__ = 'Admins'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String(256), nullable=False)
    admin_username = db.Column(db.String(50), unique=True, nullable=False)
    admin_password = db.Column(db.String(64), nullable=False)  # hashed password
    role_id = db.Column(db.Integer, db.ForeignKey('roleAdmins.role_id'))

    role = db.relationship('RoleAdmins', backref='admins')

class ProductImages(db.Model):
    __tablename__ = 'ProductImages'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('Products.prod_id'))
    image_data = db.Column(db.LargeBinary)
    is_primary = db.Column(db.Boolean, default=False)

    product = db.relationship('Products', backref='images')

class CustomerGroups(db.Model):
    __tablename__ = 'CustomerGroups'
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_description = db.Column(db.String(255))
    min_purchase = db.Column(db.Numeric(10, 2), default=0)

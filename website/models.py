from . import db
import uuid
from flask_login import UserMixin
from datetime import date
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

    def get_id(self):
        return str(self.cus_id)

class Supplier(db.Model,UserMixin):
    __tablename__= 'Supplier'
    supply_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    supply_name = db.Column(db.String(256))
    def get_id(self):
        return str(self.supply_id)

class Catalogue(db.Model,UserMixin):
    __tablename__= 'Catalogue'
    cat_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(256))


class Products(db.Model,UserMixin):
    __tablename__='Products'
    prod_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    prod_name = db.Column(db.String(256))
    prod_received=db.Column(db.Integer) # Số lượng nhập
    prod_stock=db.Column(db.Integer) # Số lượng tồn kho
    prod_sold=db.Column(db.Integer) #Số lượng đã bán
    prod_price = db.Column(db.Numeric(10, 2))
    prod_discount =db.Column(db.Numeric(5, 2))
    cat_id=db.Column(db.Integer, db.ForeignKey('Catalogue.cat_id'))
    supply_id=db.Column(db.Integer,  db.ForeignKey('Supplier.supply_id'))
    prod_description=db.Column(db.Text)

    category = db.relationship('Catalogue', backref='products_cat', lazy=True) 
     # Mối quan hệ với OrderDetails
    order_details = db.relationship('OrderDetails', backref='product_dtl', lazy=True)

class Orders(db.Model,UserMixin):
    __tablename__='Orders'
    orders_id = db.Column(db.String(10), primary_key = True) 
    orders_date = db.Column(db.Date, default=db.func.now())
    cus_id = db.Column(db.Integer,db.ForeignKey('Customer.cus_id'))
    orders_status = db.Column(Enum('pending', 'shipped', 'completed', 'cancelled', name='order_status_enum'))
    orders_total = db.Column(db.Numeric(10,2), default = 0)
    shipping_fee = db.Column(db.Numeric(10,2), default = 0)
    def get_id(self):
        return str(self.orders_id)
     # Mối quan hệ nhiều-nhiều với Products thông qua bảng phụ
    order_detail = db.relationship('OrderDetails', backref='order', uselist=False, lazy=True)

class OrderDetails(db.Model,UserMixin):
    __tablename__= 'OrderDetails'
    orders_id = db.Column(db.String(10), db.ForeignKey('Orders.orders_id'))
    prod_id = db.Column(db.Integer,db.ForeignKey('Products.prod_id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10,2))
    def get_id(self):
        return str(self.order_detail_id)
    product_dtl = db.relationship('Products', backref='order_details', lazy=True)
    
class Coupon(db.Model,UserMixin ):
    __tablename__='Coupon'
    coupon_id = db.Column(db.Integer, primary_key = True,  autoincrement=True) # Sử dụng IDENTITY để tự động tăng giá trị
    coupon_code = db.Column(db.VARCHAR(50),  nullable=False)                    # Mã giảm giá
    discount_type = db.Column(db.Enum('percentage', 'fixed', name='discount_type_enum'), nullable=False)ay thế ENUM bằng VARCHAR
    discount_value = db.Column(db.Numberic(10,2),  nullable=False)      #Giá trị giảm giá
    min_order_value =db.Column(db.Numberic(10,2),  nullable=False)             # Giá trị đơn hàng tối thiểu
    start_date = db.Column(Date,nullable=False)              #Ngày bắt đầu
    end_date = db.Column(Date,nullable=False) #                     -- Ngày kết thúc
    usage_limit = db.Column(db.Integer)             # Số lần sử dụng tối đa
    used_count = db.Column(db.Integer, default = 0)                        # Số lần đã sử dụng
    status = db.Column(db.Enum('active', 'inactive', name='status_enum'), nullable=False, default='active')
    customer_group = db.Column(db.VARCHAR(50))      # Nhóm khách hàng
    #Ràng buộc
    __table_args__=(
        CheckConstraint('discount_value >= 0', name='chk_discount_value'),
        CheckConstraint('min_order_value >= 0', name='chk_min_order_value'),
    )
    def get_id(self):
        return str(self.coupon_id)
    coupon_order = db.relationship('Orders',  backref='order_coupon', lazy=True)
class OrderCoupons(db.Model, UserMixin):
    __tablename__='OrderCoupons'
    order_coupon_id =db.Column(db.Integer, primary_key = True,  autoincrement=True) 
    orders_id = db.Column(db.String(10), db.ForeignKey('Orders.orders_id'))
    coupon_id=db.Column(db.Integer,  db.ForeignKey('Coupon.coupon_id'))
    discount_value=db.Column(db.Numeric(10,2)) #-- Giá trị giảm giá sau khi áp dụng coupon
    def get_id(self):
        return str(self.supply_id)
    
    coupon_ord = db.relationship('Orders', backref='products', lazy=True) 
    coupon_ord = db.relationship('Coupon', backref='products', lazy=True) 

class roleAdmins(db.Model, UserMixin):
    __tablename__='roleAdmins'
    role_id =db.Column(db.Integer, primary_key = True,  autoincrement=True) 
    role_name = db.Column(db.String(10), nullable = False)
    def get_id(self):
        return str(self.role_id)
class Admins (db.Model, UserMixin):
    __tablename__='Admins'
    admin_id =db.Column(db.Integer, primary_key = True,  autoincrement=True) 
    admin_name = db.Column(db.String(10), nullable = False)
    admin_username = db.Column(db.String(10), nullable = False, unique=True)
    admin_password = db.Column(db.String(100))
    admin_id =db.Column(db.Integer, db.ForeignKey('roleAdmins.role_id'))#Khóa ngoại liên kết với vai trò
    def get_id(self):
        return str(self.admin_id)
class ProductImages (db.Model, UserMixin):
    __tablename__='ProductImages'
    image_id =db.Column(db.Integer, primary_key = True,  autoincrement=True)   # ID của hình ảnh
    prod_id =db.Column(db.Integer,db.ForeignKey('Products.prod_id'))                  #Khóa ngoại liên kết với bảng Products
    image_path = db.Column(db.String(100))          # Đường dẫn hoặc URL đến hình ảnh
    is_primary = db.Column(db.Boolean, default=False)   # Cột này xác định hình ảnh nào là hình ảnh chính của sản phẩm (false = không phải, true = hình ảnh chính)
    def get_id(self):
        return str(self.image_id)
class CustomerGroups(db.Model, UserMixin):
    __tablename__='CustomerGroups'
    group_id =db.Column(db.Integer, primary_key = True,  autoincrement=True)# ID nhóm, tự động tăng
    group_description = db.Column(db.String(256))#,     -- Mô tả nhóm, có thể để trống
    min_purchase=db.Column(db.Numberic(10,2), default=0)# Giá trị mua tối thiểu để vào nhóm, mặc định là 0
    def get_id(self):
        return str(self.group_id)
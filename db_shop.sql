create database db_shop;

USE db_shop;
GO
create table Customer(
	cus_id int primary key IDENTITY, 
	cus_name VARCHAR(256),
	cus_email VARCHAR(256),
	cus_phone char(10),
	cus_username VARCHAR(50) UNIQUE,
	cus_password char(100),
	cus_group VARCHAR(50) DEFAULT 'silver',
	total_spent DECIMAL(10, 2) DEFAULT 0 
);

create table Supplier(
	supply_id int primary key IDENTITY, 
	supply_name VARCHAR(256)
);

create table Catalogue(
	cat_id int primary key IDENTITY, 
	cat_name VARCHAR(256),
);

Create table Products(
	prod_id int primary key IDENTITY, 
	prod_name VARCHAR(256),
	prod_received INT, -- Số lượng nhập
    prod_stock AS (prod_received - prod_sold) PERSISTED, -- Số lượng tồn kho
    prod_sold INT, -- Số lượng đã bán
	prod_price DECIMAL(10, 2),
	prod_discount DECIMAL(5, 2),
	cat_id int,
	supply_id int,
	prod_description text,
	FOREIGN KEY (cat_id) REFERENCES Catalogue(cat_id),
    FOREIGN KEY (supply_id) REFERENCES Supplier(supply_id)
);

create table Orders(
	orders_id CHAR(10) PRIMARY KEY DEFAULT LEFT(REPLACE(NEWID(), '-', ''), 10), 
	orders_date DATE DEFAULT GETDATE(),
	cus_id int,
	orders_status VARCHAR(20) CHECK (orders_status IN ('pending', 'shipped', 'completed','cancelled')),
	orders_total DECIMAL(10, 2) DEFAULT 0,
	shipping_fee DECIMAL(10, 2) DEFAULT 0,
    coupon_code VARCHAR(50) DEFAULT NULL,
    couponship_code VARCHAR(50) DEFAULT NULL,
    FOREIGN KEY (coupon_code) REFERENCES Coupon(coupon_code),
    FOREIGN KEY (couponship_code) REFERENCES Coupon_Ship(couponship_code),
	FOREIGN KEY (cus_id) REFERENCES Customer(cus_id)
);

CREATE TABLE OrderDetails (
    orders_id CHAR(10),
    prod_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (orders_id) REFERENCES Orders(orders_id),
    FOREIGN KEY (prod_id) REFERENCES Products(prod_id)
);

CREATE TABLE Coupon (
    coupon_code VARCHAR(50) PRIMARY KEY NOT NULL,             -- Mã giảm giá
    discount_type VARCHAR(10) NOT NULL,           -- Thay thế ENUM bằng VARCHAR
    discount_value DECIMAL(10, 2) NOT NULL,       -- Giá trị giảm giá
    min_order_value DECIMAL(10, 2),               -- Giá trị đơn hàng tối thiểu
    start_date DATE NOT NULL,                     -- Ngày bắt đầu
    end_date DATE NOT NULL,                       -- Ngày kết thúc
    usage_limit INT DEFAULT NULL,                 -- Số lần sử dụng tối đa
    used_count INT DEFAULT 0,                     -- Số lần đã sử dụng
    status VARCHAR(10) NOT NULL DEFAULT 'active', -- Trạng thái, thay ENUM bằng VARCHAR
    customer_group VARCHAR(50),                   -- Nhóm khách hàng
    -- Ràng buộc CHECK để giới hạn giá trị hợp lệ cho discount_type và status
    CONSTRAINT chk_discount_type CHECK (discount_type IN ('percentage', 'fixed')),
    CONSTRAINT chk_status CHECK (status IN ('active', 'inactive')),
	CONSTRAINT chk_discount_value CHECK (discount_value >= 0),
    CONSTRAINT chk_min_order_value CHECK (min_order_value >= 0)
);

CREATE TABLE Coupon_Ship (          -- Sử dụng IDENTITY để tự động tăng giá trị
    couponship_code VARCHAR(50) PRIMARY KEY NOT NULL,             -- Mã giảm giá
    discount_type VARCHAR(10) NOT NULL,           -- Thay thế ENUM bằng VARCHAR
    discount_value DECIMAL(10, 2) NOT NULL,       -- Giá trị giảm giá
    min_order_value DECIMAL(10, 2),               -- Giá trị đơn hàng tối thiểu
    start_date DATE NOT NULL,                     -- Ngày bắt đầu
    end_date DATE NOT NULL,                       -- Ngày kết thúc
    usage_limit INT DEFAULT NULL,                 -- Số lần sử dụng tối đa
    used_count INT DEFAULT 0,                     -- Số lần đã sử dụng
    status VARCHAR(10) NOT NULL DEFAULT 'active', -- Trạng thái, thay ENUM bằng VARCHAR
    customer_group VARCHAR(50),                   -- Nhóm khách hàng
    -- Ràng buộc CHECK để giới hạn giá trị hợp lệ cho discount_type và status
    CONSTRAINT chk_discount_type CHECK (discount_type IN ('percentage', 'fixed')),
    CONSTRAINT chk_status CHECK (status IN ('active', 'inactive')),
	CONSTRAINT chk_discount_value CHECK (discount_value >= 0),
    CONSTRAINT chk_min_order_value CHECK (min_order_value >= 0)
);

-- CREATE TABLE OrderCoupons (
--     order_coupon_id INT PRIMARY KEY IDENTITY,
--     orders_id CHAR(10),
--     coupon_code VARCHAR(50),
--     couponship_code VARCHAR(50),
--     FOREIGN KEY (orders_id) REFERENCES Orders(orders_id),
--     FOREIGN KEY (coupon_code) REFERENCES Coupon(coupon_code),
--     FOREIGN KEY (couponship_code) REFERENCES Coupon_Ship(coupon_code)
-- );
 
-- Bảng lưu vai trò của Admin
CREATE TABLE roleAdmins (
    role_id INT PRIMARY KEY IDENTITY,  -- Tự động tăng
    role_name VARCHAR(50) UNIQUE NOT NULL 
);

-- Bảng Admins
CREATE TABLE Admins (
    admin_id INT PRIMARY KEY IDENTITY,  -- Tạo khóa chính tự động tăng
    admin_name VARCHAR(256) NOT NULL,   -- Tên quản trị viên
    admin_username VARCHAR(50) UNIQUE NOT NULL,  -- Tên đăng nhập quản trị viên
    admin_password CHAR(64) NOT NULL,   -- Mật khẩu đã băm
    role_id INT,                        -- Khóa ngoại liên kết với vai trò
    FOREIGN KEY (role_id) REFERENCES roleAdmins(role_id) -- Ràng buộc khóa ngoại
);

CREATE TABLE ProductImages (
    image_id INT PRIMARY KEY IDENTITY,  -- ID của hình ảnh
    prod_id INT,                        -- Khóa ngoại liên kết với bảng Products
  
    image_data VARBINARY(MAX),          -- Lưu trữ hình ảnh dưới dạng nhị phân (nếu cần)
    is_primary BIT DEFAULT 0,           -- Cột này xác định hình ảnh nào là hình ảnh chính của sản phẩm (0 = không phải, 1 = hình ảnh chính)
    FOREIGN KEY (prod_id) REFERENCES Products(prod_id)
);

CREATE TABLE CustomerGroups (
    group_id INT PRIMARY KEY IDENTITY,  -- ID nhóm, tự động tăng
    group_description VARCHAR(255),     -- Mô tả nhóm, có thể để trống
    min_purchase DECIMAL(10, 2) DEFAULT 0 -- Giá trị mua tối thiểu để vào nhóm, mặc định là 0
);

go 

-- CREATE TRIGGER UpdateOrdersTotalOnCouponChange
-- ON OrderCoupons
-- AFTER INSERT, UPDATE, DELETE
-- AS
-- BEGIN
--     SET NOCOUNT ON;

--     -- Lấy danh sách các orders_id bị ảnh hưởng
--     DECLARE @UpdatedOrders TABLE (orders_id CHAR(10));
--     INSERT INTO @UpdatedOrders (orders_id)
--     SELECT DISTINCT orders_id
--     FROM 
--         INSERTED
--         UNION
--         SELECT DISTINCT orders_id
--         FROM DELETED;

--     -- Cập nhật lại orders_total cho các đơn hàng bị ảnh hưởng
--     UPDATE Orders
--     SET orders_total = (
--         SELECT o.orders_total - COALESCE(SUM(OC.discount_value), 0)
--         FROM OrderCoupons OC
--         WHERE OC.orders_id = o.orders_id
--     )
--     FROM Orders o
--     WHERE o.orders_id IN (SELECT orders_id FROM @UpdatedOrders);
-- END;

GO
CREATE TRIGGER UpdateOrdersTotal
ON Orders
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Cập nhật giá trị tổng đơn hàng
    UPDATE Orders
    SET orders_total = (
        -- Tính tổng giá trị sản phẩm trong đơn hàng
        SELECT SUM(OD.quantity * OD.price) 
        FROM OrderDetails OD
        WHERE OD.orders_id = Orders.orders_id
    ) - COALESCE((
        SELECT C.discount_value
        FROM Coupon C
        WHERE C.coupon_code=Orders.coupon_code
    ), 0) - COALESCE((
        SELECT CS.discount_value
        FROM Coupon_Ship CS
        WHERE CS.couponship_code=Orders.couponship_code
    ), 0)
    WHERE orders_id IN (SELECT orders_id FROM INSERTED);
END;

go
CREATE TRIGGER trg_InsteadOfInsertCustomer
ON Customer
INSTEAD OF INSERT
AS
BEGIN
    -- Xóa các khai báo biến trùng lặp
    DECLARE @password NVARCHAR(50);
    DECLARE @hashed_password CHAR(64);

    -- Lấy mật khẩu từ dữ liệu mới
    SELECT @password = cus_password FROM INSERTED;

    -- Băm mật khẩu với SHA-256
    SET @hashed_password = CONVERT(CHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(50), @password)), 2);

    -- Chèn dữ liệu vào bảng Customer, thay mật khẩu bằng mật khẩu đã băm
    -- Chú ý: Đảm bảo bạn không chèn giá trị cho cột cus_id (cột identity)
    INSERT INTO Customer (cus_name, cus_email, cus_phone, cus_username, cus_password)
    SELECT cus_name, cus_email, cus_phone, cus_username, @hashed_password
    FROM INSERTED;
END;
go
CREATE TRIGGER trg_InsteadOfInsertAdmin
ON Admins
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @password NVARCHAR(50);
    DECLARE @hashed_password CHAR(64);

    -- Lấy mật khẩu từ dữ liệu mới
    SELECT @password = admin_password FROM INSERTED;

    -- Băm mật khẩu với SHA-256
    SET @hashed_password = CONVERT(CHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(50), @password)), 2);

    -- Chèn dữ liệu vào bảng Admins, thay mật khẩu bằng mật khẩu đã băm
    INSERT INTO Admins (admin_name, admin_username, admin_password, role_id)  -- Chú ý sử dụng 'role_id' thay vì 'role'
    SELECT admin_name, admin_username, @hashed_password, role_id  -- 'role_id' thay vì 'role'
    FROM INSERTED;
END;
go
CREATE TRIGGER trg_UpdateTotalSpent
ON Orders
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    -- Cập nhật tổng chi tiêu cho khách hàng khi có đơn hàng mới
    UPDATE c
    SET c.total_spent = c.total_spent + (
        SELECT o.orders_total
        FROM INSERTED o
        WHERE o.cus_id = c.cus_id
    )
    FROM Customer c
    WHERE c.cus_id IN (SELECT DISTINCT cus_id FROM INSERTED);
END;
GO

CREATE TRIGGER trg_UpdateCustomerGroup
ON Customer
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Cập nhật nhóm khách hàng dựa trên tổng chi tiêu
    UPDATE c
    SET c.cus_group = CASE
        WHEN c.total_spent >= 25000000 THEN 'Plantinium'
        WHEN c.total_spent >= 15000000 THEN 'Gold'
        ELSE 'Silver'
    END
    FROM Customer c
    WHERE c.cus_id IN (SELECT DISTINCT cus_id FROM INSERTED);
END;
GO
go
INSERT INTO Customer (cus_name, cus_email, cus_phone, cus_username, cus_password)
VALUES 
('Văn An', 'vananhtran@gmail.com', '0987654321', 'nvana23', '123456'),
('Thị Bình', 'thibinhn@gmail.com', '0912345678', 'ttb11', '987654'),
('Minh Cường', 'minhcuong@gmail.com', '0938765432', 'lmc5', '246802'),
('Thị Dương', 'thiduong@gmail.com', '0961234567', 'ptd34', '123456'),
('Minh Tuấn', 'minhtuantran@gmail.com', '0923456789', 'dmt43', '123456'),
('Khả Duy', 'trinhkhaduy@gmail.com', '0123456793', 'tkd42', '123456'),
('Văn Thịnh', 'vanthinhnguyen@gmail.com', '0891234567', 'vtt423', '123456'),
('Tuấn Phạm', 'phamminhtuan@gmail.com', '0909876543', 'pmt543', '123456');

INSERT INTO Supplier (supply_name)
VALUES 
('Thế Giới Di Động'),
('CellphoneS'),
('Điện Máy Chợ Lớn'),
('Hoàng Hà Mobile');

INSERT INTO Catalogue (cat_name)
VALUES 
('Điện thoại'),
('Laptop'),
('Phụ kiện'),
('Máy tính bảng');

-- Thêm vào bảng Products, cần chỉ định cat_id và supply_id
INSERT INTO Products (prod_name, prod_received, prod_sold, prod_price, prod_discount, cat_id, supply_id, prod_description)
VALUES 
('Điện thoại iPhone 16 Pro Max', 200, 10, 30000000, 0, 1, 1, 'Latest model of smartphone with a high-quality camera'),
('Điện thoại iPhone 16', 200, 4, 30000000, 0.00, 1, 1, 'Fresh bananas sourced from local farms'),
('Laptop Asus Vivobook Go 15', 340, 6, 20000000, 0, 2, 2, 'Comfortable cotton t-shirt available in multiple colors'),
('Laptop Lenovo Ideapad Slim 3', 80, 5, 12000000, 0, 2, 3, 'Durable soccer ball for all levels of play'),
('Máy tính bảng iPad 10', 120, 10, 9500000, 0, 3, 1, 'Moisturizing lip balm for smooth lips'),
('Máy tính bảng Samsung Galaxy Tab S10 Ultra 5G', 100, 50, 14000000, 0, 3, 2, 'Latest model of smartphone with a high-quality camera'),
('Điện thoại Samsung Galaxy S24 Ultra 5G', 200, 20, 25000000, 0.00, 1, 4, 'Fresh bananas sourced from local farms'),
('Cáp Type C 1m Xmobile TC27-1000', 150, 40, 100000, 0, 4, 1, 'Comfortable cotton t-shirt available in multiple colors');

INSERT INTO roleAdmins (role_name) 
VALUES 
('Administrator'), 
('Manager'), 
('Admin');

INSERT INTO Admins (admin_name, admin_username, admin_password, role_id)
VALUES
('Gia Hân', 'adminA', '123456', 1),
('Ngân Lê', 'adminB', '123456', 3),
('Hải Mi', 'adminC', '123456', 2);

-- Thêm vào bảng Coupon
INSERT INTO Coupon (coupon_code, discount_type, discount_value, min_order_value, start_date, end_date, status, customer_group)
VALUES 
('DISCOUNT10', 'percentage', 10, 10000000, '2024-01-01', '2024-12-31', 'active', 'silver'),
('DISCOUNT20', 'fixed', 2000000, 15000000, '2024-01-01', '2024-12-31', 'active', 'gold'),
('FREESHIP', 'fixed', 20000, 0, '2024-01-01', '2024-12-31', 'active', null);

INSERT INTO CustomerGroups (group_description, min_purchase)
VALUES 
('Silver', 0),  -- Nhóm khách hàng Silver, không yêu cầu mua tối thiểu
('Gold', 15000000),  -- Nhóm khách hàng Gold, yêu cầu mua tối thiểu 15 triệu
('Plantinium', 20000000)-- Nhóm khách hàng Plantinium, yêu cầu mua tối thiểu 20 triệu

-- 1. Create database
CREATE DATABASE PeacefulPagesSanctuary;
GO
USE PeacefulPagesSanctuary;
GO

-- 2. Tables
CREATE TABLE Customer (
    cus_id INT PRIMARY KEY IDENTITY,
    cus_name VARCHAR(256),
    cus_email VARCHAR(256) UNIQUE,
    cus_phone VARCHAR(10),
    cus_username VARCHAR(50) UNIQUE,
    cus_password VARCHAR(64),  -- SHA256 hash length
    cus_group VARCHAR(50) DEFAULT 'Silver',
    is_verified BIT DEFAULT 0,
    is_active BIT NOT NULL DEFAULT 1;
    total_spent DECIMAL(10, 2) DEFAULT 0
);

CREATE TABLE Supplier (
    supply_id INT PRIMARY KEY IDENTITY,
    supply_name VARCHAR(256)
);

CREATE TABLE Catalogue (
    cat_id INT PRIMARY KEY IDENTITY,
    cat_name VARCHAR(256)
);

CREATE TABLE Products (
    prod_id INT PRIMARY KEY IDENTITY,
    prod_name VARCHAR(256),
    prod_received INT,
    prod_sold INT,
    prod_stock AS (prod_received - prod_sold) PERSISTED,
    prod_price DECIMAL(10, 2),
    prod_discount DECIMAL(5, 2),
    cat_id INT,
    supply_id INT,
    prod_description VARCHAR(MAX),
    FOREIGN KEY (cat_id) REFERENCES Catalogue(cat_id),
    FOREIGN KEY (supply_id) REFERENCES Supplier(supply_id)
);

CREATE TABLE Coupon (
    coupon_code VARCHAR(50) PRIMARY KEY,
    discount_type VARCHAR(10),
    discount_value DECIMAL(10, 2),
    min_order_value DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    usage_limit INT DEFAULT NULL,
    used_count INT DEFAULT 0,
    status VARCHAR(10) DEFAULT 'active',
    customer_group VARCHAR(50),
    CONSTRAINT chk_coupon_discount_type CHECK (discount_type IN ('percentage', 'fixed')),
    CONSTRAINT chk_coupon_status CHECK (status IN ('active', 'inactive')),
    CONSTRAINT chk_coupon_discount_value CHECK (discount_value >= 0),
    CONSTRAINT chk_coupon_min_order_value CHECK (min_order_value >= 0)
);

CREATE TABLE Coupon_Ship (
    couponship_code VARCHAR(50) PRIMARY KEY,
    discount_type VARCHAR(10),
    discount_value DECIMAL(10, 2),
    min_order_value DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    usage_limit INT DEFAULT NULL,
    used_count INT DEFAULT 0,
    status VARCHAR(10) DEFAULT 'active',
    customer_group VARCHAR(50),
    CONSTRAINT chk_discount_type CHECK (discount_type IN ('percentage', 'fixed')),
    CONSTRAINT chk_status CHECK (status IN ('active', 'inactive')),
    CONSTRAINT chk_discount_value CHECK (discount_value >= 0),
    CONSTRAINT chk_min_order_value CHECK (min_order_value >= 0)
);

CREATE TABLE Orders (
    orders_id VARCHAR(10) PRIMARY KEY,
    orders_date DATE DEFAULT GETDATE(),
    cus_id INT,
    orders_status VARCHAR(20) CHECK (orders_status IN ('pending', 'shipped', 'completed', 'cancelled')),
    orders_total DECIMAL(10, 2) DEFAULT 0,
    shipping_fee DECIMAL(10, 2) DEFAULT 0,
    coupon_code VARCHAR(50),
    couponship_code VARCHAR(50),
    FOREIGN KEY (cus_id) REFERENCES Customer(cus_id),
    FOREIGN KEY (coupon_code) REFERENCES Coupon(coupon_code),
    FOREIGN KEY (couponship_code) REFERENCES Coupon_Ship(couponship_code)
);

CREATE TABLE OrderDetails (
    ordersdtl_id INT IDENTITY(1,1) PRIMARY KEY,
    orders_id VARCHAR(10),
    prod_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (orders_id) REFERENCES Orders(orders_id),
    FOREIGN KEY (prod_id) REFERENCES Products(prod_id)
);

CREATE TABLE roleAdmins (
    role_id INT PRIMARY KEY IDENTITY,
    role_name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Admins (
    admin_id INT PRIMARY KEY IDENTITY,
    admin_name VARCHAR(256) NOT NULL,
    admin_username VARCHAR(50) UNIQUE NOT NULL,
    admin_password VARCHAR(64) NOT NULL,
    role_id INT,
    FOREIGN KEY (role_id) REFERENCES roleAdmins(role_id)
);

CREATE TABLE ProductImages (
    image_id INT PRIMARY KEY IDENTITY,
    prod_id INT,
    image_data VARBINARY(MAX),
    is_primary BIT DEFAULT 0,
    FOREIGN KEY (prod_id) REFERENCES Products(prod_id)
);

CREATE TABLE CustomerGroups (
    group_id INT PRIMARY KEY IDENTITY,
    group_description VARCHAR(255),
    min_purchase DECIMAL(10, 2) DEFAULT 0
);

-- 3. Triggers

-- Hash password trigger for Customer
CREATE TRIGGER trg_InsteadOfInsertCustomer
ON Customer
INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO Customer (cus_name, cus_email, cus_phone, cus_username, cus_password)
    SELECT 
        cus_name, 
        cus_email, 
        cus_phone, 
        cus_username, 
        CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(50), cus_password)), 2)
    FROM INSERTED;
END;

-- Hash password trigger for Admins
CREATE TRIGGER trg_InsteadOfInsertAdmin
ON Admins
INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO Admins (admin_name, admin_username, admin_password, role_id)
    SELECT 
        admin_name, 
        admin_username, 
        CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', CONVERT(NVARCHAR(50), admin_password)), 2),
        role_id
    FROM INSERTED;
END;

-- Trigger to auto-generate Orders.orders_id (10 chars from NEWID)
CREATE TRIGGER trg_InsertOrdersID
ON Orders
INSTEAD OF INSERT
AS
BEGIN
    INSERT INTO Orders (orders_id, orders_date, cus_id, orders_status, orders_total, shipping_fee, coupon_code, couponship_code)
    SELECT 
        LEFT(REPLACE(NEWID(), '-', ''), 10),
        ISNULL(orders_date, GETDATE()),
        cus_id,
        orders_status,
        orders_total,
        shipping_fee,
        coupon_code,
        couponship_code
    FROM INSERTED;
END;

-- Update Orders Total when OrderDetails or Orders updated
CREATE TRIGGER UpdateOrdersTotal
ON Orders
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE O
    SET orders_total = 
        ISNULL((
            SELECT SUM(OD.quantity * OD.price)
            FROM OrderDetails OD
            WHERE OD.orders_id = O.orders_id
        ), 0)
        - ISNULL((
            SELECT CASE 
                    WHEN C.discount_type = 'percentage' THEN
                        (SELECT SUM(OD.quantity * OD.price) FROM OrderDetails OD WHERE OD.orders_id = O.orders_id) * C.discount_value / 100
                    ELSE C.discount_value
                END
            FROM Coupon C WHERE C.coupon_code = O.coupon_code
        ), 0)
        - ISNULL((
            SELECT CASE 
                    WHEN CS.discount_type = 'percentage' THEN
                        (SELECT SUM(OD.quantity * OD.price) FROM OrderDetails OD WHERE OD.orders_id = O.orders_id) * CS.discount_value / 100
                    ELSE CS.discount_value
                END
            FROM Coupon_Ship CS WHERE CS.couponship_code = O.couponship_code
        ), 0)
    FROM Orders O
    WHERE O.orders_id IN (SELECT orders_id FROM INSERTED);
END;

-- Update Customer total_spent after Orders inserted
CREATE TRIGGER trg_UpdateTotalSpent
ON Orders
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE c
    SET c.total_spent = c.total_spent + o.orders_total
    FROM Customer c
    JOIN INSERTED o ON o.cus_id = c.cus_id;
END;

-- Update Customer group based on total_spent after Customer update
CREATE TRIGGER trg_UpdateCustomerGroup
ON Customer
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE c
    SET c.cus_group = CASE
        WHEN c.total_spent >= 25000000 THEN 'Platinum'
        WHEN c.total_spent >= 15000000 THEN 'Gold'
        ELSE 'Silver'
    END
    FROM Customer c
    WHERE c.cus_id IN (SELECT DISTINCT cus_id FROM INSERTED);
END;

-- 4. Sample inserts
-- Insert Customers
INSERT INTO Customer (cus_name, cus_email, cus_phone, cus_username, cus_password, cus_group, is_verified, total_spent)
VALUES
('Alice Nguyen', 'alice.nguyen@gmail.com', '0987654321', 'alice_n', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'password123'), 2), 'Silver', 1, 12000000),
('Bob Tran', 'bob.tran@gmail.com', '0912345678', 'bobt', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'password123'), 2), 'Gold', 1, 16000000),
('Carol Le', 'carol.le@gmail.com', '0938765432', 'caroll', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'password123'), 2), 'Platinum', 1, 27000000),
('David Pham', 'david.pham@gmail.com', '0978123456', 'davidp', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'pass456'), 2), 'Silver', 0, 5000000),
('Ellen Tran', 'ellen.tran@gmail.com', '0909123456', 'ellent', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'ellenpass'), 2), 'Silver', 1, 2000000);

-- Insert Suppliers
INSERT INTO Supplier (supply_name)
VALUES
('Book World Inc.'),
('Readers Paradise Ltd.'),
('Knowledge Source Co'),
('Global Books Ltd.'),
('Urban Reads');

-- Insert Catalogue
INSERT INTO Catalogue (cat_name)
VALUES
('Fiction'),
('Non-Fiction'),
('Science'),
('Technology'),
('Children'),
('History');

-- Insert Products
INSERT INTO Products (prod_name, prod_received, prod_sold, prod_price, prod_discount, cat_id, supply_id, prod_description)
VALUES
('The Great Gatsby', 100, 20, 150000, 10, 1, 1, 'Classic novel by F. Scott Fitzgerald'),
('A Brief History of Time', 50, 5, 200000, 0, 3, 2, 'Stephen Hawking’s book about cosmology'),
('Learn Python Programming', 70, 15, 180000, 5, 4, 3, 'Comprehensive guide to Python programming'),
('Children Stories', 120, 40, 90000, 15, 5, 4, 'Collection of short stories for kids'),
('World War II Chronicles', 80, 10, 220000, 20, 6, 5, 'Detailed history of the second world war');

-- Insert Coupon
INSERT INTO Coupon (coupon_code, discount_type, discount_value, min_order_value, start_date, end_date, usage_limit, used_count, status, customer_group)
VALUES
('SUMMER10', 'percentage', 10, 50000, '2025-06-01', '2025-08-31', 100, 25, 'active', 'Silver'),
('GOLD15', 'percentage', 15, 100000, '2025-05-01', '2025-12-31', 50, 10, 'active', 'Gold'),
('WELCOME50', 'fixed', 50000, 200000, '2025-01-01', '2025-12-31', NULL, 5, 'active', NULL);

-- Insert Coupon_Ship
INSERT INTO Coupon_Ship (couponship_code, discount_type, discount_value, min_order_value, start_date, end_date, usage_limit, used_count, status, customer_group)
VALUES
('SHIPFREE', 'fixed', 30000, 100000, '2025-06-01', '2025-12-31', 200, 80, 'active', NULL),
('SHIP10', 'percentage', 10, 50000, '2025-05-01', '2025-09-30', 100, 45, 'active', 'Silver');

-- Insert Orders
INSERT INTO Orders (orders_id, orders_date, cus_id, orders_status, orders_total, shipping_fee, coupon_code, couponship_code)
VALUES
('ORD000001', '2025-06-01', 1, 'completed', 270000, 30000, 'SUMMER10', 'SHIPFREE'),
('ORD000002', '2025-06-03', 2, 'shipped', 380000, 0, 'GOLD15', NULL),
('ORD000003', '2025-06-05', 3, 'pending', 90000, 30000, NULL, 'SHIP10'),
('ORD000004', '2025-06-06', 4, 'cancelled', 0, 0, NULL, NULL);

-- Insert OrderDetails
INSERT INTO OrderDetails (orders_id, prod_id, quantity, price)
VALUES
('ORD000001', 1, 1, 150000),
('ORD000001', 4, 1, 90000),
('ORD000002', 2, 2, 200000),
('ORD000003', 4, 1, 90000);

-- Insert roleAdmins
INSERT INTO roleAdmins (role_name)
VALUES
('SuperAdmin'),
('Manager'),
('Staff');

-- Insert Admins
INSERT INTO Admins (admin_name, admin_username, admin_password, role_id)
VALUES
('Admin One', 'admin1', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'adminpass1'), 2), 1),
('Manager One', 'manager1', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'managerpass'), 2), 2),
('Staff One', 'staff1', CONVERT(VARCHAR(64), HASHBYTES('SHA2_256', 'staffpass'), 2), 3);

-- Insert ProductImages
-- Giả sử ảnh được lưu dưới dạng varbinary, ở đây ví dụ NULL để làm mẫu
INSERT INTO ProductImages (prod_id, image_data, is_primary)
VALUES
(1, NULL, 1),
(2, NULL, 1),
(3, NULL, 1),
(4, NULL, 1),
(5, NULL, 1);

-- Insert CustomerGroups
INSERT INTO CustomerGroups (group_description, min_purchase)
VALUES
('Silver customers with purchases below 15 million VND', 0),
('Gold customers with purchases between 15 million and 25 million VND', 15000000),
('Platinum customers with purchases above 25 million VND', 25000000);

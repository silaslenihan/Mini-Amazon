CREATE TABLE Users
(username VARCHAR(256) NOT NULL PRIMARY KEY,
 password VARCHAR(256) NOT NULL,
 name VARCHAR(256) NOT NULL,
 email VARCHAR(256) NOT NULL,
 address VARCHAR(256) NOT NULL,
 balance DECIMAL(10,2) NOT NULL,
 isPrime BOOLEAN NOT NULL,
 secret VARCHAR(256) NOT NULL);

CREATE TABLE Sellers
(username VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Users(username));

CREATE TABLE Buyers
(username VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Users(username));

CREATE TABLE Category
(cat_name VARCHAR(256) NOT NULL PRIMARY KEY,
description VARCHAR(256) NOT NULL);

CREATE TABLE Items
(item_id INTEGER NOT NULL PRIMARY KEY,
cat_name VARCHAR(256) NOT NULL REFERENCES Category(cat_name),
name VARCHAR (256) NOT NULL,
avg_rate DECIMAL(10, 2) NOT NULL CHECK(avg_rate >= 1 AND avg_rate <= 5),
description VARCHAR(256) NOT NULL);

CREATE TABLE Orders
(buyer_username VARCHAR(256) NOT NULL REFERENCES Buyers(username),
 order_id INTEGER NOT NULL,
 payment_amount DECIMAL(10, 2) NOT NULL,
 date_of_purchase DATE NOT NULL,
 date_of_delivery DATE NOT NULL CHECK(date_of_delivery >= date_of_purchase),
 PRIMARY KEY(buyer_username,order_id));

CREATE TABLE Reviews 
(username VARCHAR(256) NOT NULL REFERENCES Users(username),
 item_id INTEGER NOT NULL REFERENCES Items(item_id),
 date_time DATE NOT NULL,
 content VARCHAR(256) NOT NULL,
 rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
 PRIMARY KEY(username,item_id,date_time));

CREATE TABLE OrderItems
(order_id INTEGER NOT NULL REFERENCES Orders(order_id),
item_id INTEGER NOT NULL REFERENCES Items(item_id),
cat_name VARCHAR(256) NOT NULL REFERENCES Category(cat_name),
quantity INTEGER NOT NULL CHECK(quantity >= 0),
PRIMARY KEY(order_id, item_id));

CREATE TABLE SellsItem
(seller_username VARCHAR(256) NOT NULL REFERENCES Sellers(username),
item_id  INTEGER NOT NULL REFERENCES Items(item_id),
cat_name VARCHAR(256) NOT NULL REFERENCES Category(cat_name),
price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
stock INTEGER NOT NULL CHECK(stock >= 0),
PRIMARY KEY(seller_username, item_id));

CREATE TABLE Cart
(item_id INTEGER NOT NULL REFERENCES Items(item_id),
username VARCHAR(256) NOT NULL REFERENCES Buyers(username),
quantity INTEGER NOT NULL CHECK(quantity >= 0),
price_per_item DECIMAL(10, 2) NOT NULL CHECK(price_per_item >= 0),
PRIMARY KEY(username, item_id));

CREATE VIEW CartSummary AS 
SELECT C.username as username, SUM(C.quantity*C.price_per_item) as total_price, COUNT(C.quantity) as total_quantity FROM Cart C GROUP BY C.username;


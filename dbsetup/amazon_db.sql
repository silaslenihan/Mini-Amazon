CREATE TABLE Users
(username VARCHAR(256) NOT NULL PRIMARY KEY,
 password VARCHAR(256) NOT NULL,
 name VARCHAR(256) NOT NULL,
 email VARCHAR(256) NOT NULL,
 address VARCHAR(256) NOT NULL,
 balance DECIMAL(10,2) NOT NULL,
 isPrime BOOLEAN NOT NULL);

--TODO: default balance to 0, make sure email and address are valid formats, make sure passwd fits constraints?

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
rec_score DECIMAL(10, 2) NOT NULL CHECK(rec_score >= 0),
description VARCHAR(256) NOT NULL);

--TODO: AVG rating? do we need to specify constraints, or 

--TODO: Add Image? How do we do this in a postgres database? Can descriptions be left out or are they mandatory?

CREATE TABLE Orders
(order_id INTEGER NOT NULL PRIMARY KEY,
 payment_amount DECIMAL(10, 2) NOT NULL,
 date_of_purchase DATE NOT NULL,
 date_of_delivery DATE NOT NULL);

CREATE TABLE Reviews 
(username VARCHAR(256) NOT NULL REFERENCES Users(username),
 item_id INTEGER NOT NULL REFERENCES Items(item_id),
 date_time DATE NOT NULL,
 content VARCHAR(256) NOT NULL,
 rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
 PRIMARY KEY(username,item_id,date_time));

--TODO: make sure DATETIME in right format, is content long enough?

CREATE TABLE OrderHistory
(seller_username VARCHAR(256) NOT NULL REFERENCES Sellers(username),
 order_id INTEGER NOT NULL REFERENCES Orders(order_id),
 buyer_username VARCHAR(256) NOT NULL REFERENCES Buyers(username),
 PRIMARY KEY(seller_username,order_id));

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

--TODO: triggers for when loading db, auto fill who sells what and orders what upon trying to insert orders or reviews and whatnot?

--TODO: RAISE EXCEPTIONS for following issues:
	-- -prevent selling item or ordering items that have stock below 0
	-- -make sure everything being purchased can be afforded - use balance to ensure not below 0
	-- -possible check for similar item in other cats?
	-- -multiple users with one username acting as seller?

CREATE VIEW CartSummary AS 
SELECT C.username as username, SUM(C.quantity*C.price_per_item) as total_price, COUNT(C.quantity) as total_quantity FROM Cart C GROUP BY C.username;





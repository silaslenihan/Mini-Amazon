CREATE TABLE Users
(username VARCHAR(256) NOT NULL PRIMARY KEY,
 password VARCHAR(256) NOT NULL,
 name VARCHAR(256) NOT NULL,
 email VARCHAR(256) NOT NULL,
 address VARCHAR(256) NOT NULL,
 balance INTEGER NOT NULL);

--TODO: default balance to 0, make sure email and address are valid formats, make sure passwd fits constraints?

CREATE TABLE Sellers
(username VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Users(username));

CREATE TABLE Buyers
(username VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Users(username));

CREATE TABLE Reviews
(username VARCHAR(256) NOT NULL REFERENCES Users(username),
 item_id INTEGER NOT NULL REFERENCES Items(item_id),
 date_time DATE NOT NULL,
 content VARCHAR(256) NOT NULL,
 rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
 PRIMARY KEY(username,item_id,date_time));

--TODO: make sure DATETIME in right format, is content long enough?

CREATE TABLE Orders
(order_id INTEGER NOT NULL PRIMARY KEY,
 payment_amount DECIMAL(10, 2) NOT NULL,
 date_of_purchase DATE NOT NULL,
 date_of_delivery DATE NOT NULL);

CREATE TABLE OrderHistory
(seller_username VARCHAR(256) NOT NULL REFERENCES Sellers(username),
 order_id INTEGER NOT NULL REFERENCES Orders(order_id),
 buyer_username VARCHAR(256) NOT NULL REFERENCES Buyers(username),
 PRIMARY KEY(seller_username,order_id));

CREATE TABLE OrderItems
(order_id INTEGER NOT NULL PRIMARY KEY REFERENCES Orders(order_id),
item_id INTEGER NOT NULL PRIMARY KEY REFERENCES Items(item_id),
cat_name VARCHAR(20) NOT NULL PRIMARY KEY REFERENCES Category(cat_name),
quantity INTEGER NOT NULL CHECK(quantity >= 0));


CREATE TABLE SellsItem
(seller_username VARCHAR(20) NOT NULL PRIMARY KEY REFERENCES Sellers(username),
item_id  INTEGER NOT NULL PRIMARY KEY REFERENCES Items(item_id),
cat_name VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Category(cat_name),
price FLOAT NOT NULL CHECK(price >= 0),
stock INTEGER NOT NULL CHECK(stock >= 0));


CREATE TABLE Cart
(item_id INTEGER NOT NULL PRIMARY KEY REFERENCES Items(item_id),
cat_name VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Category(cat_name),
isPrime BOOLEAN NOT NULL,
quantity INTEGER NOT NULL CHECK(quantity >= 0),
totalPrice FLOAT NOT NULL CHECK(totalPrice >= 0));


CREATE TABLE Items
(item_id INTEGER NOT NULL PRIMARY KEY 
cat_name VARCHAR(256) NOT NULL PRIMARY KEY REFERENCES Category(cat_name),
name VARCHAR (256) NOT NULL,
avg_rate FLOAT NOT NULL CHECK(avg_rate >= 0),
score INTEGER NOT NULL CHECK(score >= 0),
image,
description VARCHAR(256));


CREATE TABLE Category
(cat_name VARCHAR(256) NOT NULL PRIMARY KEY,
description VARCHAR(256) NOT NULL);

CREATE TABLE Users
(username VARCHAR(256) NOT NULL PRIMARY KEY,
 password VARCHAR(256) NOT NULL,
 name VARCHAR(256) NOT NULL,
 email VARCHAR(256) NOT NULL,
 address VARCHAR(256) NOT NULL,
 balance INTEGER NOT NULL);

--TODO: default balance to 0, make sure email and address are valid formats, make sure passwd fits constraints?

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

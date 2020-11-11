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
total_ratings INTEGER NOT NULL,
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
WITH 
cart_sum AS (SELECT C.username as username, SUM(C.quantity*C.price_per_item) as total_price, COUNT(C.quantity) as total_quantity FROM Cart C GROUP BY C.username),
user_list AS (SELECT U.username as username FROM Users U)
SELECT COALESCE(U.username,C.username) AS username, COALESCE(C.total_price,0) AS total_price, COALESCE(C.total_quantity,0) AS total_quantity FROM user_list U FULL OUTER JOIN cart_sum C ON U.username = C.username;


CREATE FUNCTION TF_Modify_buyer_balance_on_order() RETURNS TRIGGER AS $$
BEGIN
  UPDATE Users
  SET balance = balance - NEW.payment_amount
  WHERE username = NEW.buyer_username;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Modify_buyer_balance_on_order
  AFTER INSERT ON Orders
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Modify_buyer_balance_on_order();

CREATE FUNCTION TF_Check_balance_enough_on_order() RETURNS TRIGGER AS $$
BEGIN
  IF NOT EXISTS(SELECT * FROM Users U WHERE U.balance >= NEW.payment_amount AND U.username = NEW.buyer_username) THEN
    RAISE EXCEPTION 'The balance of User % is not high enough to afford placing this order.', NEW.buyer_username;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Check_balance_enough_on_order
  BEFORE INSERT ON Orders
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Check_balance_enough_on_order();


CREATE FUNCTION TF_Check_balance_enough() RETURNS TRIGGER AS $$
BEGIN
	IF NOT EXISTS(SELECT * FROM Users U, CartSummary CS WHERE U.balance >= CS.total_price + NEW.quantity*NEW.price_per_item AND U.username = NEW.username AND U.username = CS.username) THEN
	  RAISE EXCEPTION 'The balance of User % is not high enough to afford this item.', NEW.username;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Check_balance_enough
  BEFORE INSERT ON Cart
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Check_balance_enough();


CREATE FUNCTION TF_Modify_stock_item_on_cart_add() RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'INSERT') THEN
  	UPDATE SellsItem
  	SET stock = stock - NEW.quantity
  	WHERE item_id = NEW.item_id;
  ELSIF (TG_OP = 'UPDATE') THEN
  	UPDATE SellsItem
  	SET stock = stock - (NEW.quantity - OLD.quantity)
  	WHERE item_id = NEW.item_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Modify_stock_item_on_cart_add
  AFTER INSERT OR UPDATE ON Cart
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Modify_stock_item_on_cart_add();


CREATE FUNCTION TF_PasswordLength() RETURNS TRIGGER AS $$
BEGIN
  IF (char_length(NEW.password) < 8) THEN
    RAISE EXCEPTION 'password must be at least 8 characters long';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_PasswordLength
  BEFORE INSERT OR UPDATE ON Users
  FOR EACH ROW
  EXECUTE PROCEDURE TF_PasswordLength();


CREATE FUNCTION TF_UpdateAverageRtg() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM Items WHERE item_id = NEW.item_id AND total_ratings = 0) THEN
    UPDATE Items
    SET 
      avg_rate = NEW.rating,
      total_ratings = 1
    WHERE item_id = NEW.item_id;
  ELSE
    UPDATE Items
    SET 
      avg_rate = (total_ratings * avg_rate + NEW.rating)/(total_ratings + 1),
      total_ratings = total_ratings + 1
    WHERE item_id = NEW.item_id;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_UpdateAverageRtg
  AFTER INSERT ON Reviews
  FOR EACH ROW
  EXECUTE PROCEDURE TF_UpdateAverageRtg();


CREATE FUNCTION TF_SellerNoReview() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM SellsItem S WHERE S.item_id = NEW.item_id AND S.seller_username = NEW.username) THEN
    RAISE EXCEPTION 'user % cannot review an item they are selling.', NEW.username;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_SellerNoReview
  BEFORE INSERT ON Reviews
  FOR EACH ROW
  EXECUTE PROCEDURE TF_SellerNoReview();

CREATE FUNCTION TF_ReviewNotSeller() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM Reviews R WHERE R.item_id = NEW.item_id AND R.username = NEW.seller_username) THEN
    RAISE EXCEPTION 'user % cannot sell an item they are reviewing.', NEW.seller_username;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_ReviewNotSeller
  BEFORE INSERT ON SellsItem
  FOR EACH ROW
  EXECUTE PROCEDURE TF_ReviewNotSeller();


CREATE FUNCTION TF_Check_stock_item_on_cart_add() RETURNS TRIGGER AS $$
BEGIN
  IF (TG_OP = 'INSERT') THEN
    IF EXISTS (SELECT * FROM SellsItem S WHERE NEW.quantity > S.stock AND NEW.item_id = S.item_id) THEN
      RAISE EXCEPTION 'there is not enough remaining stock of item % to purchase % of that item', NEW.item_id, NEW.quantity;
    END IF;
  ELSIF (TG_OP = 'UPDATE') THEN
    IF EXISTS (SELECT * FROM SellsItem S WHERE NEW.quantity - OLD.quantity > S.stock AND NEW.item_id = S.item_id) THEN
      RAISE EXCEPTION 'there is not enough remaining stock of item % to purchase % of that item', NEW.item_id, NEW.quantity;
    END IF;
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Check_stock_item_on_cart_add
  BEFORE INSERT OR UPDATE ON Cart
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Check_stock_item_on_cart_add();

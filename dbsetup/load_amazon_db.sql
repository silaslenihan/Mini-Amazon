INSERT INTO Category VALUES('Media', 'Television and Movie related media products');
INSERT INTO Category VALUES('Clothing', 'Clothes products');

INSERT INTO Items VALUES(1, 'Media', 'Friends: Season 1', 4.8, 2, 'Season 1 of popular tv show friends.');
INSERT INTO Items VALUES(2, 'Clothing', 'Banana Republic T-Shirt', 4.1, 1, 'grey tshirt from banana republic.');
INSERT INTO Items VALUES(3, 'Media', 'Friends: Season 2', 4.5, 0, 0, 'Season 2 of popular tv show friends.');
INSERT INTO Items VALUES(4, 'Media', 'White Collar: Season 3', 3.9, 0, 'Season 3 of popular tv show white collar.');
INSERT INTO Items VALUES(5, 'Media', 'Prison Break: Season 2', 4.2, 1, 'Season 2 of popular tv show prison break.');
INSERT INTO Items VALUES(6, 'Clothing', 'J-Crew T-Shirt', 4.2, 1, 'white tshirt from j crew.');
INSERT INTO Items VALUES(7, 'Clothing', 'Lucky Brand Jeans', 3.7, 1, 'Soft, light jeans from lucky brand.');
INSERT INTO Items VALUES(8, 'Clothing', 'Nike Running Shoes', 4.3, 1, 'white and yellow, lightweight running sneakers.');
INSERT INTO Items VALUES(9, 'Clothing', 'Nike Ankle Socks', 4.0, 1, 'Soft, white ankle length socks.');
INSERT INTO Items VALUES(10, 'Media', 'Lost: Season 1', 4.4, 1, 'Season 1 of popular tv show lost.');

--TO DO: Average rating based on the reviews (not hard coded)? / Same thing for score

INSERT INTO Users VALUES('johndoe','pass1234','John Doe', 'jdoe@gmail.com','1 Main St, Durham, NC', 1000, True, 'abc');
INSERT INTO Users VALUES('janedoe','pass1234','Jane Doe', 'jadoe1@gmail.com','2 Main St, Durham, NC', 10000, True, 'def');
INSERT INTO Users VALUES('mikey2','pass1234','Michael', 'mike@gmail.com','3 Main St, Durham, NC', 5000, True, 'ghi');
INSERT INTO Users VALUES('sarah1','pass1234','Sarah', 'sarah@gmail.com','4 Main St, Durham, NC', 2000, True, 'jkl');
INSERT INTO Users VALUES('evan7','pass1234','Evan', 'evan@gmail.com','5 Main St, Durham, NC', 2000, True, 'mno');

INSERT INTO Buyers VALUES('johndoe');
INSERT INTO Buyers VALUES('mikey2');
INSERT INTO Buyers VALUES('sarah1');

INSERT INTO Sellers VALUES('evan7');
INSERT INTO Sellers VALUES('janedoe');

INSERT INTO Cart VALUES(2, 'johndoe', 5, 17.50);
INSERT INTO Cart VALUES(1, 'johndoe', 3, 19.99);
INSERT INTO Cart VALUES(3, 'johndoe', 1, 19.99);
INSERT INTO Cart VALUES(4, 'johndoe', 2, 17.50);
INSERT INTO Cart VALUES(5, 'johndoe', 4, 19.99);


INSERT INTO Orders VALUES(1,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(2,17.50,'2020-03-10','2020-03-12');
INSERT INTO Orders VALUES(3,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(4,17.50,'2020-03-10','2020-03-12');
INSERT INTO Orders VALUES(5,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(6,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(7,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(8,13.29,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(9,17.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(10,88.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(11,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(12,17.50,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(13,19.99,'2020-01-01,2020-02-01');
INSERT INTO Orders VALUES(14,17.50,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(15,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(16,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(17,19.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(18,13.29,'2020-03-10','2020-03-12');
INSERT INTO Orders VALUES(19,17.99,'2020-01-01','2020-02-01');
INSERT INTO Orders VALUES(20,88.99,'2020-03-10','2020-03-12');

INSERT INTO Reviews VALUES('johndoe',1,'2020-04-04','This is cool!',4.5);
INSERT INTO Reviews VALUES('mikey2',2,'2020-04-04','This is cool!',4.4);
INSERT INTO Reviews VALUES('johndoe',9,'2020-04-04','This is cool!',4.4);
INSERT INTO Reviews VALUES('johndoe',7,'2020-04-04','This is cool!',5.0);
INSERT INTO Reviews VALUES('mikey2',1,'2020-04-04','This is cool!',4.8);
INSERT INTO Reviews VALUES('johndoe',10,'2020-04-04','This is cool!',3.3);
INSERT INTO Reviews VALUES('sarah1',3,'2020-04-04','This is cool!',4.4);
INSERT INTO Reviews VALUES('sarah1',6,'2020-04-04','This is cool!',4.9);
INSERT INTO Reviews VALUES('sarah1',5,'2020-04-04','This is cool!',4.2);
INSERT INTO Reviews VALUES('mikey2',8,'2020-04-04','This is cool!',4.1);


INSERT INTO OrderItems VALUES(1,1,'Media',1);
INSERT INTO OrderItems VALUES(2,2,'Clothing',1);
INSERT INTO OrderItems VALUES(3,3,'Media',1);
INSERT INTO OrderItems VALUES(4,4,'Media',1);
INSERT INTO OrderItems VALUES(5,5,'Media',1);
INSERT INTO OrderItems VALUES(6,6,'Clothing',1);
INSERT INTO OrderItems VALUES(7,7,'Clothing',1);
INSERT INTO OrderItems VALUES(8,8,'Clothing',1);
INSERT INTO OrderItems VALUES(9,9,'Clothing',1);
INSERT INTO OrderItems VALUES(10,10,'Media',1);
INSERT INTO OrderItems VALUES(11,1,'Media',1);
INSERT INTO OrderItems VALUES(12,2,'Clothing',1);
INSERT INTO OrderItems VALUES(13,3,'Media',1);
INSERT INTO OrderItems VALUES(14,4,'Media',1);
INSERT INTO OrderItems VALUES(15,5,'Media',1);
INSERT INTO OrderItems VALUES(16,6,'Clothing',1);
INSERT INTO OrderItems VALUES(17,7,'Clothing',1);
INSERT INTO OrderItems VALUES(18,8,'Clothing',1);
INSERT INTO OrderItems VALUES(19,9,'Clothing',1);
INSERT INTO OrderItems VALUES(20,10,'Media',1);

INSERT INTO SellsItem VALUES('evan7', 1, 'Media', 19.99, 10);
INSERT INTO SellsItem VALUES('evan7', 2, 'Clothing', 17.50, 10);
INSERT INTO SellsItem VALUES('evan7', 3, 'Media', 19.99, 10);
INSERT INTO SellsItem VALUES('evan7', 4, 'Media', 17.50, 10);
INSERT INTO SellsItem VALUES('evan7', 5, 'Media', 19.99, 10);
INSERT INTO SellsItem VALUES('evan7', 6, 'Clothing', 19.99, 10);
INSERT INTO SellsItem VALUES('evan7', 7, 'Clothing', 19.99, 10);
INSERT INTO SellsItem VALUES('evan7', 8, 'Clothing', 13.29, 10);
INSERT INTO SellsItem VALUES('evan7', 9, 'Clothing', 17.99, 10);
INSERT INTO SellsItem VALUES('evan7', 10, 'Media', 88.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 1, 'Media', 19.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 2, 'Clothing', 17.50, 10);
INSERT INTO SellsItem VALUES('janedoe', 3, 'Media', 19.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 4, 'Media', 17.50, 10);
INSERT INTO SellsItem VALUES('janedoe', 5, 'Media', 19.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 6, 'Clothing', 19.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 7, 'Clothing', 19.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 8, 'Clothing', 13.29, 10);
INSERT INTO SellsItem VALUES('janedoe', 9, 'Clothing', 17.99, 10);
INSERT INTO SellsItem VALUES('janedoe', 10, 'Media', 88.99, 10);


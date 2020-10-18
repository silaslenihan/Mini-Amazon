INSERT INTO Category VALUES('Media', 'Television and Movie related media products');
INSERT INTO Category VALUES('Clothing', 'Clothes products');

INSERT INTO Items VALUES(1, 'Media', 'Friends: Season 1', 4.8, 0, 'Season 1 of popular tv show friends.');
INSERT INTO Items VALUES(2, 'Clothing', 'Banana Republic T-Shirt', 4.1, 0, 'grey tshirt from banana republic.');
INSERT INTO Items VALUES(3, 'Media', 'Friends: Season 2', 4.5, 0, 'Season 2 of popular tv show friends.');
INSERT INTO Items VALUES(4, 'Media', 'White Collar: Season 3', 3.9, 0, 'Season 3 of popular tv show white collar.');
INSERT INTO Items VALUES(5, 'Media', 'Prison Break: Season 2', 4.2, 0, 'Season 2 of popular tv show prison break.');
INSERT INTO Items VALUES(6, 'Clothing', 'J-Crew T-Shirt', 4.2, 0, 'white tshirt from j crew.');
INSERT INTO Items VALUES(7, 'Clothing', 'Lucky Brand Jeans', 3.7, 0, 'Soft, light jeans from lucky brand.');
INSERT INTO Items VALUES(8, 'Clothing', 'Nike Running Shoes', 4.3, 0, 'white and yellow, lightweight running sneakers.');
INSERT INTO Items VALUES(9, 'Clothing', 'Nike Ankle Socks', 4.0, 0, 'Soft, white ankle length socks.');
INSERT INTO Items VALUES(10, 'Media', 'Lost: Season 1', 4.4, 0, 'Season 1 of popular tv show lost.');

INSERT INTO Users VALUES('johndoe','pass1234','John Doe', 'jdoe@gmail.com','1 Main St, Durham, NC', 1000, True);
INSERT INTO Users VALUES('janedoe','pass1234','Jane Doe', 'jadoe1@gmail.com','2 Main St, Durham, NC', 10000, True);
INSERT INTO Users VALUES('mikey2','pass1234','Michael', 'mike@gmail.com','3 Main St, Durham, NC', 5000, True);
INSERT INTO Users VALUES('sarah1','pass1234','Sarah', 'sarah@gmail.com','4 Main St, Durham, NC', 2000, True);
INSERT INTO Users VALUES('evan7','pass1234','Evan', 'evan@gmail.com','5 Main St, Durham, NC', 700, True);

INSERT INTO Buyers VALUES('johndoe');
INSERT INTO Buyers VALUES('mikey2');
INSERT INTO Buyers VALUES('sarah1');

INSERT INTO Sellers VALUES('evan7');
INSERT INTO Sellers VALUES('janedoe');

INSERT INTO Orders VALUES(1,19.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(2,17.50,2020-03-10,2020-03-12);
INSERT INTO Orders VALUES(3,19.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(4,17.50,2020-03-10,2020-03-12);
INSERT INTO Orders VALUES(5,19.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(6,19.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(7,19.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(8,13.29,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(9,17.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(10,88.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(11,71.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(12,12.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(13,19.09,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(14,101.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(15,18.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(16,1.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(17,19.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(18,27.50,2020-03-10,2020-03-12);
INSERT INTO Orders VALUES(19,199.99,2020-01-01,2020-02-01);
INSERT INTO Orders VALUES(20,10.50,2020-03-10,2020-03-12);

INSERT INTO Reviews VALUES('johndoe',1,2019-03-04,'This is cool!',4.5);
INSERT INTO Reviews VALUES('mikey2',1,2019-03-04,'This is cool!',4.4);
INSERT INTO Reviews VALUES('johndoe',2,2019-03-04,'This is cool!',4.4);
INSERT INTO Reviews VALUES('johndoe',2,2019-03-04,'This is cool!',5.0);
INSERT INTO Reviews VALUES('mikey2',3,2019-03-04,'This is cool!',4.8);
INSERT INTO Reviews VALUES('johndoe',3,2019-03-04,'This is cool!',3.3);
INSERT INTO Reviews VALUES('johndoe',3,2019-03-04,'This is cool!',4.4);
INSERT INTO Reviews VALUES('sarah1',7,2019-03-04,'This is cool!',4.9);
INSERT INTO Reviews VALUES('sarah1',7,2019-03-04,'This is cool!',4.2);
INSERT INTO Reviews VALUES('mikey2',6,2019-03-04,'This is cool!',4.1);
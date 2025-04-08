-- ENABLE Referential Integrity
PRAGMA foreign_keys = 1;

-- Drops tables so that the code can reset and the tables only have the stated inserted values
DROP TABLE IF EXISTS demo;
DROP TABLE IF EXISTS tbl_cards_people;
DROP TABLE IF EXISTS tbl_users;
DROP TABLE IF EXISTS tbl_purchase_cards;
DROP TABLE IF EXISTS tbl_cards;
DROP TABLE IF EXISTS tbl_purchases;


-- Create Tbl_cards table
CREATE TABLE tbl_cards(
  card_id INTEGER,
  card_name VARCHAR(20),
  card_picture BLOB,
  card_rarity VARCHAR(20),
  card_price INTEGER,
  Primary KEY(card_id)
);

INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (1, 'Squirtle', NULL, 'Common', 3);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (2, 'Charmander', NULL, 'Common', 2);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (3, 'Bulbasaur', NULL, 'Common', 5);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (4, 'Ivysaur', NULL, 'Rare', 2);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (5, 'Venusaur', NULL, 'Rare', 3);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (6, 'Charmeleon', NULL, 'Rare', 4);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (7, 'Charizard', NULL, 'Rare', 9);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (8, 'Wartotle', NULL, 'Rare', 4);
INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (9, 'Blastoise', NULL, 'Rare', 6);




-- Create tbl_users
CREATE TABLE tbl_users(
  person_id INTEGER,
  person_name VARCHAR(20),
  username VARCHAR(30),
  password VARCHAR(30),
  email VARCHAR(30),
  user_access VARCHAR(5),
  Primary KEY (person_id)
);


INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (1, 'James Su', 'JamesDatPro', 'jamesu123', 'j.su2@stpauls.school.nz', 'admin');
INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (2, 'Oscar Walsdorf', 'Pantsoiler28', 'skiba', 'o.walsdorf@stpauls.school.nz', 'user');
INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (3, 'Sean Lester', 'Snowynoob', 'seanlesterer', 's.lester@stpauls.school.nz', 'user');
INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (4, 'Roy Zhu', 'xx_zuzu_dabomb_xx', 'loylu', 'r.zhu@stpauls.school.nz', 'user');
INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (5, 'Eric Joe', 'EJ', 'ericjojo', 'e.joe@stpauls.school.nz', 'user');



-- Create tbl_cards_people table
CREATE TABLE tbl_cards_people(
  person_id INTEGER,
  card_id INTEGER,
  PRIMARY KEY (person_id, card_id),
  FOREIGN KEY (person_id) REFERENCES tbl_users(person_id),
  FOREIGN KEY (card_id) REFERENCES tbl_cards(card_id)
);

INSERT INTO tbl_cards_people (person_id, card_id) VALUES (1, 1);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (1, 2);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (2, 3);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (2, 6);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (3, 5);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (3, 8);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (5, 4);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (5, 7);
INSERT INTO tbl_cards_people (person_id, card_id) VALUES (5, 9);


-- Creates tbl_purchases
CREATE TABLE tbl_purchases(
    purchase_id INT,
  	purchase_date DATETIME,
  	name_of_purchaser VARCHAR(30),
    total FLOAT,
    delivery_address VARCHAR(75),
  	email_address VARCHAR (50),
    PRIMARY KEY(purchase_id)
);


-- Inserts values INTO the columns in tbl_purchases
INSERT INTO tbl_purchases (purchase_id, purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (1, '04-03-2025', 'James Su', 3, 'St Pauls Collegiate', 'j.su2@stpauls.school.nz');
INSERT INTO tbl_purchases (purchase_id, purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (2, '05-03-2025', 'Oscar Walsdorf', 5, 'St Pauls Collegiate', 'o.walsdorf@stpauls.school.nz');
INSERT INTO tbl_purchases (purchase_id, purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (3, '05-03-2025', 'Roy Zhu', 3, 'St Pauls Collegiate', 'r.zhu@stpauls.school.nz');


-- Creates tbl_purchase_cards
CREATE TABLE tbl_purchase_cards(
    purchase_id INT,
    card_id INT,
    PRIMARY KEY (purchase_id, card_id),
    FOREIGN KEY (purchase_id) REFERENCES tbl_purchases(purchase_id),
    FOREIGN KEY (card_id) REFERENCES tbl_cards(card_id)
);

-- Inserts values INTO the columns in tbl_purchase_items	
INSERT INTO tbl_purchase_cards (purchase_id, card_id) VALUES(1,1);
INSERT INTO tbl_purchase_cards (purchase_id, card_id) VALUES(2,3);
INSERT INTO tbl_purchase_cards (purchase_id, card_id) VALUES(3,5);

  
  

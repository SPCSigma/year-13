import sqlite3; 

# create connection to database
with sqlite3.connect("assets/pokemon_database.db") as conn:
    
    c = conn.cursor()
    # Delete tables if they already exist
    c.execute('''DROP TABLE IF EXISTS demo''')
    c.execute('''DROP TABLE IF EXISTS tbl_cards_people''')
    c.execute('''DROP TABLE IF EXISTS tbl_users''')
    c.execute('''DROP TABLE IF EXISTS tbl_purchase_cards''')
    c.execute('''DROP TABLE IF EXISTS tbl_cards''')
    c.execute('''DROP TABLE IF EXISTS tbl_purchases''')
    
    # Create tables
    c.execute('''CREATE TABLE tbl_cards (
				card_id INTEGER PRIMARY KEY AUTOINCREMENT,
				card_name VARCHAR(20),
				card_picture BLOB,
				card_rarity VARCHAR(25),
				card_price FLOAT
        	)''')
    
    c.execute('''CREATE TABLE tbl_users (
				person_id INTEGER PRIMARY KEY AUTOINCREMENT,
				person_name VARCHAR(20),
				username VARCHAR(20),
				password VARCHAR(30),
				email VARCHAR(30),
				user_access VARCHAR(5)
        	)''')
    
    c.execute('''CREATE TABLE tbl_cards_people (
				person_id INTEGER,
				card_id INTEGER,
				PRIMARY KEY (person_id, card_id),
				FOREIGN KEY (person_id) REFERENCES tbl_users(person_id),
				FOREIGN KEY (card_id) REFERENCES tbl_cards(card_id)
        	)''')
    
    c.execute('''CREATE TABLE tbl_purchases (
				purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
				purchase_date DATETIME,
				name_of_purchaser VARCHAR(30),
				total FLOAT,
				delivery_address VARCHAR(75),
				email_address VARCHAR (50)
        	)''')
    
    c.execute('''CREATE TABLE tbl_purchase_cards(
				purchase_id INTEGER,
				card_id INTEGER,
				PRIMARY KEY (purchase_id, card_id),
				FOREIGN KEY (purchase_id) REFERENCES tbl_purchases(purchase_id),
				FOREIGN KEY (card_id) REFERENCES tbl_cards(card_id)
        	)''')
    
    # Insert data into tables
    
    # tbl_cards
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (1, 'Squirtle', NULL, 'Common', 3)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (2, 'Charmander', NULL, 'Common', 2)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (3, 'Bulbasaur', NULL, 'Common', 5)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (4, 'Ivysaur', NULL, 'Rare', 2)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (5, 'Venusaur', NULL, 'Rare', 3)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (6, 'Charmeleon', NULL, 'Rare', 4)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (7, 'Charizard', NULL, 'Rare', 9)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (8, 'Wartotle', NULL, 'Rare', 4)''')
    c.execute('''INSERT INTO tbl_cards (card_id, card_name, card_picture, card_rarity, card_price) VALUES (9, 'Blastoise', NULL, 'Rare', 6)''')
    
    # tbl_users
    c.execute('''INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (1, 'James Su', 'JamesDatPro', 'jamesu123', 'j.su2@stpauls.school.nz', 'admin')''')
    c.execute('''INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (2, 'Oscar Walsdorf', 'Pantsoiler28', 'skiba', 'o.walsdorf@stpauls.school.nz', 'user')''')
    c.execute('''INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (3, 'Sean Lester', 'Snowynoob', 'seanlesterer', 's.lester@stpauls.school.nz', 'user')''')
    c.execute('''INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (4, 'Roy Zhu', 'xx_zuzu_dabomb_xx', 'loylu', 'r.zhu@stpauls.school.nz', 'user')''')
    c.execute('''INSERT INTO tbl_users (person_id, person_name, username, password, email, user_access) VALUES (5, 'Eric Joe', 'EJ', 'ericjojo', 'e.joe@stpauls.school.nz', 'user')''')
    
    # tbl_cards_people
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (1, 1)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (1, 2)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (2, 3)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (2, 6)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (3, 5)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (3, 8)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (5, 4)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (5, 7)''')
    c.execute('''INSERT INTO tbl_cards_people (person_id, card_id) VALUES (5, 9)''')
    
    # tbl_purchases
    c.execute('''INSERT INTO tbl_purchases (purchase_id, purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (1, '04-03-2025', 'James Su', 3, 'St Pauls Collegiate', 'j.su2@stpauls.school.nz')''')
    c.execute('''INSERT INTO tbl_purchases (purchase_id, purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (2, '05-03-2025', 'Oscar Walsdorf', 5, 'St Pauls Collegiate', 'o.walsdorf@stpauls.school.nz')''')
    c.execute('''INSERT INTO tbl_purchases (purchase_id, purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (3, '05-03-2025', 'Roy Zhu', 3, 'St Pauls Collegiate', 'r.zhu@stpauls.school.nz')''')
    
    # tbl_purchase_cards
    c.execute('''INSERT INTO tbl_purchase_cards (purchase_id, card_id) VALUES(1,1)''')
    c.execute('''INSERT INTO tbl_purchase_cards (purchase_id, card_id) VALUES(2,3)''')
    c.execute('''INSERT INTO tbl_purchase_cards (purchase_id, card_id) VALUES(3,5)''')
    
    # run test SQL to see if everything is working
	# all_cards = cur.execute("Select * FROM tbl_cards").fetchall(); 
	#display all stock from the list
	# print(all_cards); 

    
    
	# run our sql to initialise database, using with_resources pattern
	# with open('assets/pokemon_database.sql') as f:
		# conn.executescript(f.read()); 
  
  # Save changes to the database
    conn.commit(); 
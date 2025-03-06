import sqlite3; 

# create connection to database

with sqlite3.connect("assets/pokemon_database.db") as conn:
	# run our sql to initialise database, using with_resources pattern
	with open('assets/pokemon_database.sql') as f:
		conn.executescript(f.read()); 

	# Grab cursor
	cur = conn.cursor(); 

	# run test SQL to see if everything is working
	all_cards = cur.execute("Select * FROM tbl_cards").fetchall(); 
	#display all stock from the list
	print(all_cards); 

	# save changes to database
	conn.commit(); 
import sqlite3; 

# create connection to database

with sqlite3.connect("assets/shop_data.db") as conn:
	# run our sql to initialise database, using with_resources pattern
	with open('setup/shop_items.sql') as f:
		conn.executescript(f.read()); 

	# Grab cursor
	cur = conn.cursor(); 

	# run test SQL to see if everything is working
	all_items = cur.execute("Select * FROM tbl_items").fetchall(); 
	#display all stock from the list
	print(all_items); 

	# save changes to database
	conn.commit(); 

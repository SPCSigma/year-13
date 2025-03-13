from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from sqlite3 import Error
import logging

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])

def get_db_connection():
    """ Create connection to database """
    logging.debug('get_db_connection')
    conn = None
    try:
        # Create connection to database
        conn = sqlite3.connect("assets/pokemon_database.db")
        logging.debug(f"get_db_connection() -> Database connected, version: {sqlite3.version}")
    except sqlite3.Error as er:
        logging.error('get_db_connection() -> Failed to connect to database \'assets/pokemon_database.db\'')
    
    # Enable row factory
    conn.row_factory = sqlite3.Row
    
    # Enforce referential Integrity
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

# Function that gets all data and combines into one execution
def get_data(selected_columns, search_data, sort_column, sort_type):
    conn = get_db_connection()
    cur = conn.cursor()
    
    logging.debug("Getting all table data from the SQL database")
    
    # Convert the list of columns into a string separated by commas
    columns_to_select = ', '.join(selected_columns)
    
    # Adjust numeric columns to ensure proper formatting
    if 'card_price' in selected_columns:
        columns_to_select = columns_to_select.replace('card_price', "printf('%.2f', card_price) AS card_price")
    
    # SQL query
    sql = f"""
    SELECT {columns_to_select} FROM tbl_cards
    WHERE (
        card_id LIKE '%{search_data}%' OR
        card_name LIKE '%{search_data}%' OR
        card_rarity LIKE '%{search_data}%' OR
        card_price LIKE '%{search_data}%'
    )
    ORDER BY {sort_column} {sort_type}
    """
    
    logging.debug(sql)
    
    # Log the action information
    logging.debug(f"Getting table data with [{selected_columns, search_data, sort_column, sort_type}]")
    
    # Execute the sql query and fetch all results
    items = cur.execute(sql).fetchall()
    
    # Close the database connection
    conn.commit()
    conn.close()
    
    return items


@app.route("/", methods=['GET', 'POST'])
def index():
    # Default values
    selected_columns = request.form.getlist('columns')
    if not selected_columns:
        selected_columns = ['card_id', 'card_name', 'card_rarity', 'card_price']
    
    search_data = request.form.get("search_data", "")
    sort_column = request.form.get("sort_column", "card_id")
    sort_type = request.form.get("sort_type", "ASC")
    
    # Default page view load all items for the user.
    data = {}
    data = get_data(selected_columns, search_data, sort_column, sort_type)
    
    # Listen for data returning from the front end.
    if request.method == 'POST':
        action = request.form.get("action")
        
        if action == 'search':
            logging.debug("Processing POST request for search")
            search_data = request.form.get("search_data", "")
            selected_columns = request.form.getlist("columns")
            sort_type = request.form.get("sort_type", "")
            sort_column = request.form.get("sort_column", "")
            
            if selected_columns:
                data = get_data(selected_columns, search_data, sort_column, sort_type)
            if not selected_columns:
                selected_columns = ['card_id', 'card_name', 'card_rarity', 'card_price']
                data = get_data(selected_columns, search_data, sort_column, sort_type)
        
        if action == 'filter':
            logging.debug("Processing POST request for filter")
            search_data = request.form.get("search_data", "")
            selected_columns = request.form.getlist("columns")
            sort_type = request.form.get("sort_type", "ASC")
            sort_column = request.form.get("sort_column", "card_id")
            
            if selected_columns:
                data = get_data(selected_columns, search_data, sort_column, sort_type)
            if not selected_columns:
                selected_columns = ['card_id', 'card_name', 'card_rarity', 'card_price']
                data = get_data(selected_columns, search_data, sort_column, sort_type)
        
        if action == 'sort':
            logging.debug("Processing POST request for sort")
            search_data = request.form.get("search_data", "")
            selected_columns = request.form.getlist("columns")
            sort_type = request.form.get("sort_type", "")
            sort_column = request.form.get("sort_column", "")
            
            if selected_columns:
                data = get_data(selected_columns, search_data, sort_column, sort_type)
            if not selected_columns:
                selected_columns = ['card_id', 'card_name', 'card_rarity', 'card_price']
                data = get_data(selected_columns, search_data, sort_column, sort_type)
    
    return render_template("base.html", items=data, search_data=search_data, selected_columns=selected_columns, sort_type=sort_type, sort_column=sort_column)

# running
if __name__ == "__main__":
    app.run(debug=True)

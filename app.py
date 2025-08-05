from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from sqlite3 import Error
import logging

app = Flask(__name__, static_url_path='/assets', static_folder='assets')
# Add secret key for session encryption
app.config['SECRET_KEY'] = 'T5jicsXX4qC0rZleWafsCsOSzLpKuwt2'

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

# Function that gets all data and combines it into one thing
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

def delete_user(person_id):
    logging.debug(f"Deleting row {person_id} from tbl_users")
    conn = get_db_connection()
    c = conn.cursor()
    sql1 = """DELETE FROM tbl_cards_people WHERE person_id = ?"""
    
    c.execute(sql1, (person_id,))
    cards_affected_rows = c.rowcount
    logging.debug(f"delete_user() -> Deleted {cards_affected_rows} rows from tbl_cards_people")
    
    sql2 = """DELETE FROM tbl_users WHERE person_id = ?"""
    c.execute(sql2, (person_id,))
    users_affected_rows = c.rowcount
    logging.debug(f"Delete_user() -> Deleted user {person_id}. Rows: {users_affected_rows} deleted")
    
    conn.commit()
    conn.close()
    total_affected_rows = cards_affected_rows + users_affected_rows
    
    return total_affected_rows

def update_card(card_id):
    logging.debug(f"Updating data in row {card_id} in tbl_cards")
    conn = get_db_connection()
    sql = """UPDATE tbl_cards SET
            card_name = ?,
            card_rarity = ?,
            card_price = ?
            WHERE card_id = ?
            """
    affected_rows = conn.execute(sql, card_id).rowcount
    logging.debug(f"update_card() -> Number of affected rows for card id: {card_id} is {affected_rows}")
    conn.commit()
    conn.close()

def add_card(add_card_data):
    logging.debug(f"Adding a card with data: {add_card_data}")
    sql = """INSERT INTO tbl_cards (card_name, card_picture, card_rarity, card_price) VALUES (?, NULL, ?, ?)"""
    conn = get_db_connection()
    c = conn.cursor()
    new_item_id = c.execute(sql, add_card_data).lastrowid
    logging.debug(f"add_card() -> New card successfully added with ID: {new_item_id}")
    conn.commit()
    conn.close()

@app.route("/")
def root():
    return redirect(url_for('login'))


@app.route("/index", methods=['GET', 'POST'])
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


@app.route('/login', methods = ['GET', 'POST'])
def login():
    logging.debug('login()')
    error = None
    if request.method == 'POST':
        logging.debug('login() -> POST')
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password')
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists and password is correct
        check_details = cur.execute('SELECT * FROM tbl_users WHERE username = ? AND password = ?', (login_username, login_password)).fetchone()
        
        if check_details:
            logging.debug(f'login() -> User {login_username} has logged in successfully')
            flash(f'Login successful for {login_username}! Redirecting shortly...', 'success')
            return render_template('login.html'), {"Refresh": "1; url=index"}
        else:
            logging.debug(f'login() -> Login attempt failed for user {login_username}')
            flash(f'Login was unsuccessful, please try again', 'danger')
            error = 'Username or password do not match. Please try again'
            
        
    return render_template('login.html', error=error) 


# running
if __name__ == "__main__":
    # deleteusercuzidontlikeyou = delete_user('1')
    # print(f"Total number of affected rows: {deleteusercuzidontlikeyou}")
    app.run(debug=True, port = 5075) 

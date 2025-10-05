from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from sqlite3 import Error
import logging
from datetime import datetime

app = Flask(__name__, static_url_path='/assets', static_folder='assets')
# Add secret key for session encryption
app.config['SECRET_KEY'] = 'T5jicsXX4qC0rZleWafsCsOSzLpKuwt2'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', handlers=[
                    logging.StreamHandler()])
logging.getLogger().setLevel(logging.DEBUG)


def get_db_connection():
    """ Create connection to database """
    logging.debug('get_db_connection')
    conn = None
    try:
        # Create connection to database
        conn = sqlite3.connect("assets/pokemon_database.db")
        logging.debug(
            f"get_db_connection() -> Database connected, version: {sqlite3.version}")
    except sqlite3.Error as er:
        logging.error(
            'get_db_connection() -> Failed to connect to database \'assets/pokemon_database.db\'')

    # Enable row factory
    conn.row_factory = sqlite3.Row

    # Enforce referential Integrity
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

# Function that gets all data and combines it into one thing


def get_data(selected_columns, search_data, sort_column, sort_type):
    conn = get_db_connection()
    c = conn.cursor()

    logging.debug("Getting all table data from the SQL database")

    # Convert the list of columns into a string separated by commas
    columns_to_select = ', '.join(selected_columns)

    # Adjust numeric columns to ensure proper formatting
    if 'card_price' in selected_columns:
        columns_to_select = columns_to_select.replace(
            'card_price', "printf('%.2f', card_price) AS card_price")

    # SQL query
    sql = f"""
    SELECT {columns_to_select} FROM tbl_cards
    WHERE (
        card_id LIKE ? OR
        card_name LIKE ? OR
        card_rarity LIKE ? OR
        card_price LIKE ?
    )
    ORDER BY {sort_column} {sort_type}
    """

    search_querry = f'%{search_data}%'
    search_parameters = (search_querry, search_querry, search_querry, search_querry)

    # Log the action information
    logging.debug(f"Running SQL code {sql} with paramters {search_parameters}")
    # Execute the sql query and fetch all results
    items = c.execute(sql, search_parameters).fetchall()

    # Close the database connection
    conn.close()

    return items

def get_data_purchases(selected_columns, search_data, sort_column, sort_type):
    conn = get_db_connection()
    c = conn.cursor()
    logging.debug("Getting all purchase table data from SQL database")
    
    # Select all columns if none are selected
    if not selected_columns:
        selected_columns = ['purchase_id', 'purchase_date', 'name_of_purchaser', 
                            'total', 'delivery_address', 'email_address']
    
    # Convert the list of columns into a string separated by commas
    columns_to_select = ", ".join(selected_columns)
    
    
    # Adjust numeric columns to ensure proper formatting
    if 'total' in selected_columns:
        columns_to_select = columns_to_select.replace(
            'total', "printf('%.2f', total) AS total")
    
    
    sql = f"""
    SELECT {columns_to_select} 
    FROM tbl_purchases 
    WHERE (
        purchase_id LIKE ? OR
        purchase_date LIKE ? OR
        name_of_purchaser LIKE ? OR
        total LIKE ? OR
        delivery_address LIKE ? OR
        email_address LIKE ?
    )
    ORDER BY {sort_column} {sort_type}
    """
    
    search_querry = f'%{search_data}%'
    search_parameters = (search_querry, search_querry, search_querry, search_querry, search_querry, search_querry)
    # Log the action information
    logging.debug(f"Running SQL code {sql} with paramters {search_parameters}")


    purchase = c.execute(sql, search_parameters).fetchall()
    conn.close()
    
    return purchase


@app.route("/")
def root():
    return redirect(url_for('login'))


@app.route("/index", methods=['GET', 'POST'])
def index():
    # Default values
    selected_columns = request.form.getlist('columns')
    if not selected_columns:
        selected_columns = ['card_id', 'card_name',
                            'card_rarity', 'card_price']

    search_data = request.form.get("search_data", "")
    sort_column = request.form.get("sort_column", "card_id")
    sort_type = request.form.get("sort_type", "ASC")

    # Default page view load all items for the user.
    data = {}
    data = get_data(selected_columns, search_data, sort_column, sort_type)
    
    # For toast flash message
    flash_category = {
        "danger": "danger",
        "success": "success",
        "warning": "warning"
    }


    # Getting the person name from the database
    conn = get_db_connection()
    c = conn.cursor()
    user_id = session.get('user_id')
    user = c.execute('SELECT person_name FROM tbl_users WHERE person_id = ?', (user_id,)).fetchone()
    username = user['person_name'] if user else 'Not logged in'
    conn.close()
    logging.debug(f"User is {username}")
    
    # Admin session
    admin = session.get('admin', False)
    return render_template("base.html", items=data, search_data=search_data, selected_columns=selected_columns, sort_type=sort_type, sort_column=sort_column, admin=admin, flash_category=flash_category, username=username)


@app.route("/edit_card", methods=["POST"])
def edit_card():
    # Retrieve edit_card() information from the frontend
    card_id = request.form.get("card_id")
    card_name = request.form.get("card_name")
    card_rarity = request.form.get("card_rarity")
    card_price = request.form.get("card_price")
    update_card_data = (card_name, card_rarity, card_price, card_id)
    logging.debug(f"edit_card(). Editing card {card_id}")
    
    conn = get_db_connection()
    # Edit the card information in the database
    sql = """UPDATE tbl_cards SET
    card_name = ?,
    card_rarity = ?,
    card_price = ?
    WHERE card_id = ?
    """
    affected_rows = conn.execute(sql, update_card_data).rowcount
    logging.debug(
        f"update_card() -> Number of affected rows for card id: {card_id} is {affected_rows} row(s)")
    conn.commit()
    conn.close()
    
    flash(f"{card_name} has been updated.", "success")
    return redirect(url_for('index'))


@app.route("/delete_card", methods=['POST'])
def delete_card():
    logging.debug("delete_card() called")
    # Retrieve card_id that is being deleted
    card_id = request.form.get("card_id")
    conn = get_db_connection()
    c = conn.cursor()
    # Delete card in database
    card = c.execute("SELECT card_name FROM tbl_cards WHERE card_id = ?", (card_id,)).fetchone()
    card_name = card['card_name']
    
    # Delete card from tables it exists in
    c.execute("DELETE FROM tbl_purchase_cards WHERE card_id = ?", (card_id,))
    c.execute("DELETE FROM tbl_cards_people WHERE card_id = ?", (card_id,))
    c.execute("DELETE FROM tbl_cards WHERE card_id = ?", (card_id,))
    conn.commit()
    conn.close()

    logging.debug(f"{card_id} has been deleted")
    flash(f"'{card_name}' has been deleted.", "warning")
    return redirect(url_for('index'))


@app.route("/add_card", methods=["POST"])
def add_card():
    logging.debug("add_card(). Adding new card")
    # Retrieve add_card() information from the frontend
    card_name = request.form.get("addCardName")
    card_rarity = request.form.get("cardRarity")
    card_price = request.form.get("cardPrice")
    add_card_data = (card_name, card_rarity, card_price)
    conn = get_db_connection()
    c = conn.cursor()
    # Add new card into database
    sql = """INSERT INTO tbl_cards
    card_name = ?,
    card_rarity = ?,
    card_price = ?
    """
    c.execute(sql, add_card_data)
    conn.commit()
    conn.close()
    
    flash(f"New card '{card_name}' has been added.", "success")
    logging.debug(f"Adding a new card: {card_name}, {card_rarity}, {card_price} to database")
    return redirect(url_for('index'))


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():    
    logging.debug('login()')
    error = None
    if request.method == 'POST':
        logging.debug('login() -> POST')
        login_username = request.form.get('login_username')
        login_password = request.form.get('login_password')

        conn = get_db_connection()
        c = conn.cursor()
        
        # For toast flash message
        flash_category = {
            "danger": "danger",
            "success": "success",
            "warning": "warning"
        }

        # Check if user exists and password is correct
        check_details = c.execute(
            'SELECT * FROM tbl_users WHERE username = ? AND password = ?', (login_username, login_password)).fetchone()
        conn.close()
        
        if check_details:
            # Check if the logged in user is an admin
            session['user_id'] = check_details['person_id']
            session['admin'] = check_details['user_access'] == 'admin'
            flash("Login successful", "success")
            return redirect(url_for('index'))
        else:
            logging.debug(f'login() -> Login attempt failed for user {login_username}')
            flash("Login was unsuccessful, please try again", "danger")
            error = 'Username or password do not match. Please try again'
            return render_template('login.html', error=error, flash_category=flash_category)

    return render_template('login.html', error=error)


# Cart page
@app.route("/cart", methods=["GET", "POST"])
def cart():
    user_id = session.get('user_id')
    logging.debug("Loading cart page")
    if not user_id:
        flash("You must be logged in to view your cart.", "warning")
        return redirect(url_for('login'))

    conn = get_db_connection()
    c = conn.cursor()

    # Get each item in the user's cart, joined with card info
    cart_items = c.execute("""
        SELECT tbl_cart.cart_id, tbl_cart.quantity, tbl_cards.card_name, tbl_cards.card_price 
        FROM tbl_cart
        JOIN tbl_cards ON tbl_cart.card_id = tbl_cards.card_id
        WHERE tbl_cart.user_id = ?
    """, (user_id,)).fetchall()

    # Calculate total
    cart_total = sum(item['card_price'] * item['quantity'] for item in cart_items)
    
    # For toast flash message
    flash_category = {
        "danger": "danger",
        "success": "success",
        "warning": "warning"
    }
    
    # Getting the person name from the database
    user = c.execute('SELECT person_name FROM tbl_users WHERE person_id = ?', (user_id,)).fetchone()
    username = user['person_name'] if user else 'Not logged in'
    logging.debug(f"User is {username}")
    conn.close()
    
    # Admin session
    admin = session.get('admin', False)
    return render_template("cart.html", cart_items=cart_items, cart_total=cart_total, flash_category=flash_category, username=username, admin=admin)


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    logging.debug("add_to_cart() called")
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to add items to your cart.", "warning")
        return redirect(url_for('login'))
    # Retrieve add_to_cart() information from the frontend
    card_id = request.form.get("card_id")
    quantity = int(request.form.get("quantity", 1))
    logging.debug(f"User {user_id} is attempting to add card {card_id} with quantity {quantity} to cart")
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get card info
    card_info = c.execute("SELECT card_name FROM tbl_cards WHERE card_id = ?", (card_id,)).fetchone()
    card_name = card_info['card_name']
    
    # Check if item is already in cart
    check_cart = c.execute("SELECT * FROM tbl_cart WHERE user_id = ? AND card_id = ?", (user_id, card_id)).fetchone()
    if check_cart:
        # Update quantity
        previous_quantity = check_cart['quantity']
        new_quantity = previous_quantity + quantity
        logging.debug(f"Card is already in cart. Previous quantity: {previous_quantity}. New quantity after adding: {new_quantity}.")
        c.execute("UPDATE tbl_cart SET quantity = ? WHERE cart_id = ?", (new_quantity, check_cart['cart_id']))
    else:
        # Insert card into cart
        logging.debug(f"Adding card to cart. New quantity after adding: {quantity}.")
        c.execute("INSERT INTO tbl_cart (user_id, card_id, quantity) VALUES (?, ?, ?)", (user_id, card_id, new_quantity))
    conn.commit()
    conn.close()
    flash(f"'{card_name}' was added to your cart.", "success")
    return redirect(url_for('index'))


@app.route("/update_item_cart", methods=["POST"])
def update_item_cart():
    logging.debug("update_item_cart() being called")
    # Retrieve update_item_cart() information from frontend
    cart_id = request.form.get("cart_id")
    quantity = int(request.form.get("quantity", 1))
    conn = get_db_connection()
    c = conn.cursor()
    # Update cart in database
    c.execute("UPDATE tbl_cart SET quantity = ? WHERE cart_id = ?", (quantity, cart_id))
    conn.commit()
    conn.close()
    
    flash("Cart updated.", "success")
    return redirect(url_for("cart"))


@app.route("/remove_item_cart", methods=["POST"])
def remove_item_cart(): 
    logging.debug("remove_item_cart() being called")
    cart_id = request.form.get("cart_id")
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get the name of item that is being removed from cart
    remove_item_info = c.execute("""
        SELECT tbl_cards.card_name FROM tbl_cart
        JOIN tbl_cards ON tbl_cart.card_id = tbl_cards.card_id
        WHERE tbl_cart.cart_id = ?
    """, (cart_id,)).fetchone()
    item_name = remove_item_info['card_name']
    logging.debug(f"{item_name} being removed from Cart ID: {cart_id}")
    
    # Remove the item from the cart
    c.execute("DELETE FROM tbl_cart WHERE cart_id = ?", (cart_id,))
    conn.commit()
    conn.close()
    
    flash(f"{item_name} was removed from your cart", "warning")
    return redirect(url_for("cart"))
    

@app.route("/apply_promo", methods=["POST"])
def apply_promo():
    logging.debug("apply_promo(). User is trying to apply a promo code")
    promocode = request.form.get("promocode")
    # Check if promo code is valid
    if promocode == "supersecretpromocode":
        flash("Promo code applied successfully!", "success")
    else:
        flash("Promo code is invalid", "danger")
    return redirect(url_for("cart"))
        

@app.route("/checkout", methods=["POST"])
def checkout():
    logging.debug("checkout() called")
    user_id = session.get('user_id')
    email = request.form.get('email_address')
    conn = get_db_connection()
    c = conn.cursor()

    # Get the name of the user
    user_row = c.execute("SELECT person_name FROM tbl_users WHERE person_id = ?", (user_id,)).fetchone()
    person_name = user_row['person_name']

    # Get all the info from the cart
    cart_items = c.execute("""
        SELECT tbl_cart.quantity, tbl_cards.card_price
        FROM tbl_cart
        JOIN tbl_cards ON tbl_cart.card_id = tbl_cards.card_id
        WHERE tbl_cart.user_id = ?
    """, (user_id,)).fetchall()
    
    # Check if there are items in the cart
    if not cart_items:
        conn.close()
        flash("Your cart is empty.", "danger")
        return redirect(url_for('cart'))
    
    # Get cart price total
    cart_total = sum(item['card_price'] * item['quantity'] for item in cart_items)

    # Add entry to tbl_purchases
    logging.debug("Adding purchase entry into database")
    date_now = datetime.now().strftime("%d-%m-%Y")
    c.execute("""INSERT INTO tbl_purchases 
        (purchase_date, name_of_purchaser, total, delivery_address, email_address) 
        VALUES (?, ?, ?, ?, ?)""",
        (date_now, person_name, cart_total, "St Pauls Collegiate", email)
    )

    # Clear cart after purchase
    c.execute("DELETE FROM tbl_cart WHERE user_id = ?", (user_id, ))
    conn.commit()
    conn.close()

    flash("Purchase successful! Thank you for your order.", "success")
    return redirect(url_for('index'))


# Logout Route
@app.route("/logout", methods=["GET", "POST"])
def logout():
    logging.debug("User is logging out")
    flash("You have been logged out.", "success")
    # Clear the website session and log out
    session.clear()
    return redirect(url_for("login"))


# Purchases page
@app.route("/purchases", methods=["GET", "POST"])
def purchases():
    if not session.get('admin'):
        flash("You do not have permission to view this page", "danger")
        return redirect(url_for('index'))
    logging.debug("purchases() page called")
    conn = get_db_connection()
    c = conn.cursor()
    
    # Getting the person name from the database
    user_id = session.get('user_id')
    user = c.execute('SELECT person_name FROM tbl_users WHERE person_id = ?', (user_id,)).fetchone()
    username = user['person_name'] if user else 'Not logged in'
    logging.debug(f"User is {username}")
    conn.close()
    
    # For toast flash message
    flash_category = {
        "danger": "danger",
        "success": "success",
        "warning": "warning"
    }

    selected_columns = request.form.getlist("columns")
    search_data = request.form.get("search_data", "")
    sort_column = request.form.get("sort_column", "purchase_id")
    sort_type = request.form.get("sort_type", "ASC")
    
    # Default page view load all items for the user.
    data = {}
    data = get_data_purchases(selected_columns, search_data, sort_column, sort_type)
    
    # Admin session
    admin = session.get('admin', False)
    return render_template("purchases.html", purchase=data, search_data=search_data, selected_columns=selected_columns, sort_type=sort_type, sort_column=sort_column, username=username, admin=admin, flash_category=flash_category)


@app.route('/edit_purchase', methods=['POST'])
def edit_purchase():
    logging.debug("edit_purchase() called")
    # Retrieve edit_purchase() information from front end
    purchase_id = request.form['purchase_id']
    name_of_purchaser = request.form['name_of_purchaser']
    total = request.form['total']
    delivery_address = request.form['delivery_address']
    email_address = request.form['email_address']
    conn = get_db_connection()
    c = conn.cursor()
    # Edit the purchase information in database
    c.execute("""
        UPDATE tbl_purchases
        SET name_of_purchaser = ?, total = ?, delivery_address = ?, email_address = ?
        WHERE purchase_id = ?
    """, (name_of_purchaser, total, delivery_address, email_address, purchase_id))
    conn.commit()
    conn.close()
    logging.debug(f"Editing purchase {purchase_id}")
    flash('Purchase updated.', 'success')
    return redirect(url_for('purchases'))


@app.route('/delete_purchase', methods=['POST'])
def delete_purchase():
    logging.debug("delete_purchase() called")
    # Retrieve the id of the purchase that is being removed
    purchase_id = request.form['purchase_id']
    conn = get_db_connection()
    c = conn.cursor()
    # Delete purchase from database
    c.execute("DELETE FROM tbl_purchase_cards WHERE purchase_id = ?", (purchase_id,))
    c.execute("DELETE FROM tbl_purchases WHERE purchase_id = ?", (purchase_id,))
    conn.commit()
    conn.close()
    logging.debug(f"Deleting purchase {purchase_id}")
    flash(f'Purchase #{purchase_id} has been deleted.', 'warning')
    return redirect(url_for('purchases'))


@app.route('/add_purchase', methods=['POST'])
def add_purchase():
    logging.debug("add_purchase() called")
    # Retrieve add_purchase() information from frontend
    name_of_purchaser = request.form['name_of_purchaser']
    total = request.form['total']
    delivery_address = request.form['delivery_address']
    email_address = request.form['email_address']
    purchase_date = request.form["purchase_date"]
    conn = get_db_connection()
    c = conn.cursor()
    # Add purchase into database
    c.execute(
        "INSERT INTO tbl_purchases (purchase_date, name_of_purchaser, total, delivery_address, email_address) VALUES (?, ?, ?, ?, ?)",
        (purchase_date, name_of_purchaser, total, delivery_address, email_address)
    )
    conn.commit()
    conn.close()
    logging.debug("New purchase added")
    flash("New purchase has been added.", "success")
    return redirect(url_for('purchases'))


# running
if __name__ == "__main__":
    # deleteusercuzidontlikeyou = delete_user('1')
    # print(f"Total number of affected rows: {deleteusercuzidontlikeyou}")
    app.run(debug=True, port=5075)

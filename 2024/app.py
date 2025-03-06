from flask import Flask, render_template, request, redirect
import sqlite3
from sqlite3 import Error

def get_db_connection():
    """ Create conection to database """
    conn = None; 

    try:
        # Create connection to database
        conn = sqlite3.connect("assets/shop_data.db"); 
        print("[LOG] Connected"); 
        print("[LOG]", sqlite3.version); 
    except Error as er:
        print(er);

    # Enable row factory
    conn.row_factory = sqlite3.Row; 
    
    # Enforce referential Integrity
    sql = """
            PRAGMA foreign_keys = ON
            """
    conn.execute(sql);

    return conn;

# Function that gets all data and combines into one execution
def get_data(selected_columns, search_data, sort_column, sort_type):
    conn = get_db_connection();
    cur = conn.cursor();
    print("[LOG] - Getting [ALL ACTION] table data");

    # Convert the list of columns into a string separated by commas
    columns_to_select = ', '.join(selected_columns);

    # Adjust item_price to ensure it is returned with two decimal points
    if 'item_price' in selected_columns:
        columns_to_select = columns_to_select.replace('item_price', "printf('%.2f', item_price) AS item_price");

    # SQL query
    sql = f"""
    SELECT {columns_to_select} FROM tbl_items
    WHERE (
        item_id LIKE '%{search_data}%' OR
        sku LIKE '%{search_data}%' OR
        item_name LIKE '%{search_data}%' OR
        item_cat LIKE '%{search_data}%' OR
        item_size LIKE '%{search_data}%' OR
        item_price LIKE '%{search_data}%'
    )
    ORDER BY {sort_column} {sort_type}
    """;
    print(sql)
    
    # Log the action information
    print(f"[LOG] - Getting Table Information [ALL ACTION] with [{selected_columns, search_data, sort_column, sort_type}]");

    # Execute the sql query and fetch all results
    items = cur.execute(sql).fetchall();

    # Close the database connection
    conn.commit();
    conn.close();
    return items

app = Flask(__name__, static_url_path='/assets', static_folder='assets')

@app.route("/", methods=['GET', 'POST'])
def index():
    # Default values
    selected_columns = request.form.getlist('columns')
    if not selected_columns:
        selected_columns = ['item_id', 'sku', 'item_name', 'item_cat', 'item_size', 'item_price'] 
    search_data = request.form.get("search_data", "")
    sort_column = request.form.get("sort_column", "item_id")
    sort_type = request.form.get("sort_type", "ASC")
    # Default page view load all items for the user.
    data = {};
    data = get_data(selected_columns, search_data, sort_column, sort_type);
    

    # Listen for data returning from the front end.
    if request.method == 'POST':
        action = request.form.get("action")
        
        
        if action == 'search':
            print("[LOG] - Processing POST request for search")
            search_data = request.form.get("search_data", "")
            selected_columns = request.form.getlist("columns")
            sort_type = request.form.get("sort_type", "")
            sort_column = request.form.get("sort_column", "")
            if selected_columns:
                data = get_data(selected_columns, search_data, sort_column, sort_type)
            if not selected_columns:
                selected_columns = ['item_id', 'sku', 'item_name', 'item_cat', 'item_size', 'item_price']
                data = get_data(selected_columns, search_data, sort_column, sort_type)
    
        if action == 'filter':
            print("[LOG] - Processing POST request for filter")
            search_data = request.form.get("search_data", "")
            selected_columns = request.form.getlist("columns")
            sort_type = request.form.get("sort_type", "ASC")
            sort_column = request.form.get("sort_column", "item_id")
            if selected_columns:
                data = get_data(selected_columns, search_data, sort_column, sort_type)
            if not selected_columns:
                selected_columns = ['item_id', 'sku', 'item_name', 'item_cat', 'item_size', 'item_price']
                data = get_data(selected_columns, search_data, sort_column, sort_type)

        if action == 'sort':
            print("[LOG] - Processing POST request for sort")
            search_data = request.form.get("search_data", "")
            selected_columns = request.form.getlist("columns")
            sort_type = request.form.get("sort_type", "")
            sort_column = request.form.get("sort_column", "")
            if selected_columns:
                data = get_data(selected_columns, search_data, sort_column, sort_type)
            if not selected_columns:
                selected_columns = ['item_id', 'sku', 'item_name', 'item_cat', 'item_size', 'item_price']
                data = get_data(selected_columns, search_data, sort_column, sort_type)
    
    return render_template("base.html", items=data, search_data=search_data, selected_columns=selected_columns, sort_type=sort_type, sort_column=sort_column)


# names is tags, tags is tbl tags

# running
if __name__ == "__main__":
    app.run(debug=True)

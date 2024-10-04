import duckdb
import tkinter as tk

from config import *
from tkinter import messagebox
from tkinter import ttk

# Global variable to track sorting order
sort_orders = {}

def duckdb_table_columns(file_directory):
    # Connect to the DuckDB database
    con = duckdb.connect(file_directory)

    # Get all table names
    tables_query = "SHOW TABLES;"
    tables = con.execute(tables_query).fetchall()
    
    # Close the connection after retrieving tables
    con.close()
    
    # Convert table tuples to a list of strings
    table_list = [table[0] for table in tables]

    # Create the Tkinter window
    window = tk.Tk()
    window.title("Select a Table")
    window.geometry("350x400")  # Adjusted window size for a wider Listbox

    # Label for instruction
    label = tk.Label(window, text="Select a table:")
    label.pack(pady=10)

    # Create a listbox for tables with increased width (25% more than the original)
    table_listbox = tk.Listbox(window, listvariable=tk.StringVar(value=table_list), height=15, width=45)
    table_listbox.pack(pady=10)

    # Function to display columns and data types of selected table in a Treeview
    def display_columns():
        # Get the selected table
        try:
            selected = table_listbox.get(table_listbox.curselection())
        except:
            messagebox.showerror("Selection Error", "Please select a table")
            return

        # Reconnect to DuckDB to fetch column information
        con = duckdb.connect(file_directory)
        query = f"PRAGMA table_info({selected});"
        result = con.execute(query).fetchall()
        con.close()

        # Create a new window to display the columns in a spreadsheet-like view
        column_window = tk.Toplevel(window)
        
        # Position the pop-up window to the right edge of the main window
        # Get the main window's position and size
        main_window_x = window.winfo_x()
        main_window_y = window.winfo_y()
        main_window_width = window.winfo_width()
        
        # Set the column window to appear to the right of the main window, aligned at the top
        column_window.geometry(f"500x600+{main_window_x + main_window_width}+{main_window_y}")  # 900px for double the current height
        
        column_window.title(f"Columns in table '{selected}'")

        # Create a Treeview widget for displaying the columns
        tree = ttk.Treeview(column_window, columns=("Column Name", "Data Type"), show="headings")
        tree.heading("Column Name", text="Column Name", command=lambda: sort_column(tree, result, 1))
        tree.heading("Data Type", text="Data Type", command=lambda: sort_column(tree, result, 2))

        # Find the longest values in each column to adjust column widths
        col_name_max_width = max(len(str(col[1])) for col in result)
        col_type_max_width = max(len(str(col[2])) for col in result)

        # Set the column widths based on the longest string, but within a reasonable limit
        tree.column("Column Name", width=min((col_name_max_width * 10), 300), anchor='w')
        tree.column("Data Type", width=min((col_type_max_width * 10), 300), anchor='w')

        # Insert columns into the Treeview
        for col in result:
            tree.insert("", "end", values=(col[1], col[2]))  # col[1] is column name, col[2] is data type

        # Add scrollbar to the Treeview
        scrollbar = ttk.Scrollbar(column_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")

        # Add a button to show the first 50 rows of the selected table
        def show_data():
            display_table_data(file_directory, selected)

        show_data_button = tk.Button(column_window, text="Show First 50 Rows", command=show_data)
        show_data_button.pack(pady=10)

    # Button to confirm selection
    select_button = tk.Button(window, text="Show Columns", command=display_columns)
    select_button.pack(pady=20)

    # Bind double-click event to the listbox to trigger "Show Columns"
    table_listbox.bind("<Double-Button-1>", lambda event: display_columns())

    # Run the Tkinter event loop
    window.mainloop()

def sort_column(tree, data, col_idx):
    global sort_orders
    col_name = "Column Name" if col_idx == 1 else "Data Type"
    
    # Toggle sort order
    if col_name in sort_orders:
        sort_orders[col_name] = not sort_orders[col_name]
    else:
        sort_orders[col_name] = True  # True for ascending, False for descending

    # Sort data based on the selected column
    data.sort(key=lambda x: x[col_idx], reverse=not sort_orders[col_name])

    # Clear the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Reinsert sorted data
    for col in data:
        tree.insert("", "end", values=(col[1], col[2]))

def display_table_data(file_directory, table_name):
    # Fetch first 50 rows from the selected table
    con = duckdb.connect(file_directory)
    query = f"SELECT * FROM {table_name} LIMIT 50;"
    data = con.execute(query).fetchall()
    col_names = [desc[0] for desc in con.description]
    con.close()

    # Create a new window to display the table data
    data_window = tk.Toplevel()
    data_window.title(f"First 50 Rows of '{table_name}'")

    # Set the window geometry to the required size (width: 2000px, height: 1300px)
    data_window.geometry("1700x800")

    # Create a Treeview widget for displaying the data
    tree = ttk.Treeview(data_window, columns=col_names, show="headings")

    # Insert column names in the Treeview
    for col_name in col_names:
        tree.heading(col_name, text=col_name)

    # Insert data rows into the Treeview
    for row in data:
        tree.insert("", "end", values=row)

    # Add vertical scrollbar to the Treeview
    scrollbar_y = ttk.Scrollbar(data_window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")

    # Add horizontal scrollbar to the Treeview
    scrollbar_x = ttk.Scrollbar(data_window, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=scrollbar_x.set)
    scrollbar_x.pack(side="bottom", fill="x")

    # Properly pack the Treeview widget with some space on the right
    tree.pack(expand=True, fill="both", padx=(20, 50))

#run
duckdb_table_columns(duckdb_fpath)

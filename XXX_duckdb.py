import duckdb

# Connect to (or create) the DuckDB database file with SQL
conn = duckdb.connect('D:/Python/Leitner/leitner.duckdb')

# Use SQL statements to create the tables directly
conn.execute('''
CREATE TABLE IF NOT EXISTS flashcards (
    id INTEGER PRIMARY KEY,
    question TEXT,
    answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY,
    card_id INTEGER REFERENCES flashcards(id),
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_review_at TIMESTAMP,
    box_level INTEGER,
    retired BOOLEAN,
    FOREIGN KEY(card_id) REFERENCES flashcards(id)
)
''')

conn.execute('''
CREATE TABLE IF NOT EXISTS static_boxlevel (
    id INTEGER PRIMARY KEY,
    box_level INTEGER,
    box_level_name TEXT,
    frequency INTEGER
)
''')


# Close the connection after creation
conn.close()

print("DuckDB database and tables created successfully!")
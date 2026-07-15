import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY,
        content TEXT,
        embedding TEXT
    )
""")

cursor.execute("INSERT INTO documents (content, embedding) VALUES (?, ?)", 
               ("This is a test sentence.", "[0.1, 0.2, 0.3]"))

conn.commit()

cursor.execute("SELECT * FROM documents")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]} | Content: {row[1]}")

conn.close()
print("SQLite is working!")
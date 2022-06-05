import sqlite3 as sql

def generate_db():
    conn = sql.connect('crush.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS crush (id INTEGER PRIMARY KEY AUTOINCREMENT, your_name_hash TEXT, crush_names_hash TEXT, event_id TEXT)")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    generate_db()
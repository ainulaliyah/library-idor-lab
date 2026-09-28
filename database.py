import sqlite3

def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # Create patrons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patrons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            borrowed_book TEXT NOT NULL,
            private_notes TEXT NOT NULL
        )
    ''')
    
    # Seed mock data
    cursor.execute('DELETE FROM patrons') # Clear old data on restart
    sample_patrons = [
        (1, 'alice123', 'Alice Smith', 'alice@library.org', 'Introduction to Algorithms', 'Overdue fine: RM15.00. Restricted book request pending.'),
        (2, 'bob_reader', 'Bob Jones', 'bob@library.org', 'Python Crash Course', 'Preferred branch: Main Branch. No notes.'),
        (3, 'charlie_c', 'Charlie Tan', 'charlie@library.org', 'Computer Networking Top-Down Approach', 'VIP Member. Special borrowing privileges enabled.'),
        (4, 'diana_prince', 'Diana Prince', 'diana@library.org', 'Database System Concepts', 'Staff account. Access level: Assistant Librarian.')
    ]
    
    cursor.executemany('INSERT INTO patrons VALUES (?, ?, ?, ?, ?, ?)', sample_patrons)
    conn.commit()
    conn.close()
    print("[+] Database initialized and seeded with mock library data.")

if __name__ == '__main__':
    init_db()
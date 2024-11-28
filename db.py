import sqlite3

DB_PATH = 'channels.db'

def init_db():
    """Ma'lumotlar bazasini yaratadi yoki mavjudini ochadi."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def add_channel(chat_id):
    """Yangi kanalni ma'lumotlar bazasiga qo'shadi."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO channels (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Kanal ID allaqachon mavjud
    conn.close()

def get_all_channels():
    """Barcha kanal ID-larini ma'lumotlar bazasidan qaytaradi."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM channels")
    channels = [row[0] for row in cursor.fetchall()]
    conn.close()
    return channels

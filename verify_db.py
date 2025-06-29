import sqlite3

def check_indexes():
    conn = sqlite3.connect('book_reviews.db')
    cursor = conn.cursor()
    
    # Get all indexes
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    
    print("\nDatabase Indexes:")
    for idx in indexes:
        print(f"- {idx[0]}: {idx[1]}")
    
    # Specifically check reviews table indexes
    cursor.execute("PRAGMA index_list(reviews)")
    reviews_indexes = cursor.fetchall()
    
    print("\nReviews Table Indexes:")
    for idx in reviews_indexes:
        print(f"- Seq: {idx[0]}, Name: {idx[1]}, Unique: {idx[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_indexes()

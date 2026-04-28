import sqlite3

# 資料庫檔案路徑（根據架構設計，放置在 instance 資料夾下）
DB_PATH = 'instance/database.db'

def get_db_connection():
    """建立並回傳與 SQLite 資料庫的連線"""
    conn = sqlite3.connect(DB_PATH)
    # 將查詢結果轉為類似 dict 的物件，可透過欄位名稱存取資料
    conn.row_factory = sqlite3.Row
    return conn

def create_note(title, author, review, rating):
    """新增一筆小說筆記"""
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO notes (title, author, review, rating) VALUES (?, ?, ?, ?)',
        (title, author, review, rating)
    )
    conn.commit()
    conn.close()

def get_all_notes():
    """取得所有筆記（依建立時間反序排列）"""
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes ORDER BY id DESC').fetchall()
    conn.close()
    return notes

def get_note_by_id(note_id):
    """根據 ID 取得單一筆記"""
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
    conn.close()
    return note

def update_note(note_id, title, author, review, rating):
    """更新現有筆記內容"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE notes SET title = ?, author = ?, review = ?, rating = ? WHERE id = ?',
        (title, author, review, rating, note_id)
    )
    conn.commit()
    conn.close()

def delete_note(note_id):
    """刪除指定筆記"""
    conn = get_db_connection()
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()

def search_notes(keyword):
    """模糊搜尋書名或作者包含關鍵字的筆記"""
    conn = get_db_connection()
    search_term = f'%{keyword}%'
    notes = conn.execute(
        'SELECT * FROM notes WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC',
        (search_term, search_term)
    ).fetchall()
    conn.close()
    return notes

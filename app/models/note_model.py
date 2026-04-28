import sqlite3
import logging

# 設定基礎日誌，方便追蹤錯誤
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    try:
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO notes (title, author, review, rating) VALUES (?, ?, ?, ?)',
            (title, author, review, rating)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"建立筆記時發生資料庫錯誤: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_all_notes():
    """取得所有筆記（依建立時間反序排列）"""
    try:
        conn = get_db_connection()
        notes = conn.execute('SELECT * FROM notes ORDER BY id DESC').fetchall()
        return notes
    except sqlite3.Error as e:
        logger.error(f"取得筆記列表時發生資料庫錯誤: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_note_by_id(note_id):
    """根據 ID 取得單一筆記"""
    try:
        conn = get_db_connection()
        note = conn.execute('SELECT * FROM notes WHERE id = ?', (note_id,)).fetchone()
        return note
    except sqlite3.Error as e:
        logger.error(f"取得單一筆記時發生資料庫錯誤: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def update_note(note_id, title, author, review, rating):
    """更新現有筆記內容"""
    try:
        conn = get_db_connection()
        conn.execute(
            'UPDATE notes SET title = ?, author = ?, review = ?, rating = ? WHERE id = ?',
            (title, author, review, rating, note_id)
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"更新筆記時發生資料庫錯誤: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def delete_note(note_id):
    """刪除指定筆記"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        logger.error(f"刪除筆記時發生資料庫錯誤: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def search_notes(keyword):
    """模糊搜尋書名或作者包含關鍵字的筆記"""
    try:
        conn = get_db_connection()
        search_term = f'%{keyword}%'
        notes = conn.execute(
            'SELECT * FROM notes WHERE title LIKE ? OR author LIKE ? ORDER BY id DESC',
            (search_term, search_term)
        ).fetchall()
        return notes
    except sqlite3.Error as e:
        logger.error(f"搜尋筆記時發生資料庫錯誤: {e}")
        return []
    finally:
        if 'conn' in locals() and conn:
            conn.close()

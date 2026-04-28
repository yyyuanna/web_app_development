import os
import sqlite3
from flask import Flask
from app.routes.note_routes import note_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
# 設定 Secret Key，用於 flash messages 等功能
app.secret_key = os.environ.get('SECRET_KEY', 'dev_secret_key')

# 註冊路由 Blueprint
app.register_blueprint(note_bp)

def init_db():
    """初始化資料庫並執行 schema.sql 建表語法"""
    # 確保 instance 資料夾存在
    os.makedirs('instance', exist_ok=True)
    db_path = 'instance/database.db'
    
    conn = sqlite3.connect(db_path)
    with open('database/schema.sql', 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("資料庫初始化完成！")

# 透過命令列執行初始化 (python -c "from app import init_db; init_db()")

if __name__ == '__main__':
    app.run(debug=True)

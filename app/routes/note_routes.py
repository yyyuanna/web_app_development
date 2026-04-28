from flask import Blueprint, render_template, request, redirect, url_for
# 引用 model (需在實作階段補上)
# from app.models import note_model

# 建立名為 'note' 的 Blueprint
note_bp = Blueprint('note', __name__)

@note_bp.route('/', methods=['GET'])
def index():
    """
    首頁與筆記列表
    - 若 URL 有 search 參數，則進行搜尋過濾
    - 若無，則顯示所有筆記
    - 渲染 templates/index.html
    """
    pass

@note_bp.route('/add', methods=['GET', 'POST'])
def add_note():
    """
    新增筆記
    - GET: 顯示新增表單 (templates/form.html)
    - POST: 接收表單資料，驗證後呼叫 Model 寫入資料庫，並重導向至首頁
    """
    pass

@note_bp.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    """
    編輯筆記
    - GET: 根據 note_id 取得筆記，並預填至表單中顯示 (templates/form.html)
    - POST: 接收更新後的表單資料，驗證後呼叫 Model 更新資料庫，並重導向至首頁
    """
    pass

@note_bp.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    """
    刪除筆記
    - 接收 POST 請求，根據 note_id 從資料庫中刪除該筆記，完成後重導向至首頁
    """
    pass

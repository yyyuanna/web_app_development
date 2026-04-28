from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import note_model

# 建立名為 'note' 的 Blueprint
note_bp = Blueprint('note', __name__)

@note_bp.route('/', methods=['GET'])
def index():
    """首頁與筆記列表"""
    search_keyword = request.args.get('search', '').strip()
    if search_keyword:
        notes = note_model.search_notes(search_keyword)
    else:
        notes = note_model.get_all_notes()
    
    return render_template('index.html', notes=notes, search_keyword=search_keyword)

@note_bp.route('/add', methods=['GET', 'POST'])
def add_note():
    """新增筆記"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        review = request.form.get('review', '').strip()
        rating_str = request.form.get('rating', '1')
        
        # 1. 必填欄位驗證
        if not title or not author:
            flash('書名與作者為必填欄位！', 'danger')
            # 保留使用者剛填寫的資料，避免重新填寫
            return render_template('form.html', note=request.form)
        
        # 2. 評分格式驗證
        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            flash('評分必須是 1 到 5 的數字！', 'danger')
            return render_template('form.html', note=request.form)
        
        # 3. 寫入資料庫
        if note_model.create_note(title, author, review, rating):
            flash('筆記新增成功！', 'success')
            return redirect(url_for('note.index'))
        else:
            flash('新增失敗，請稍後再試。', 'danger')
            return render_template('form.html', note=request.form)

    # 若為 GET 請求，直接回傳空白表單
    return render_template('form.html')

@note_bp.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    """編輯筆記"""
    note = note_model.get_note_by_id(note_id)
    if not note:
        flash('找不到該筆記！', 'danger')
        return redirect(url_for('note.index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        author = request.form.get('author', '').strip()
        review = request.form.get('review', '').strip()
        rating_str = request.form.get('rating', '1')
        
        if not title or not author:
            flash('書名與作者為必填欄位！', 'danger')
            note_data = dict(request.form)
            note_data['id'] = note_id
            return render_template('form.html', note=note_data)
            
        try:
            rating = int(rating_str)
            if rating < 1 or rating > 5:
                raise ValueError
        except ValueError:
            flash('評分必須是 1 到 5 的數字！', 'danger')
            note_data = dict(request.form)
            note_data['id'] = note_id
            return render_template('form.html', note=note_data)
            
        if note_model.update_note(note_id, title, author, review, rating):
            flash('筆記更新成功！', 'success')
            return redirect(url_for('note.index'))
        else:
            flash('更新失敗，請稍後再試。', 'danger')
            note_data = dict(request.form)
            note_data['id'] = note_id
            return render_template('form.html', note=note_data)

    # GET 請求時，將從 DB 撈出來的資料帶入表單預填
    return render_template('form.html', note=note)

@note_bp.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    """刪除筆記"""
    if note_model.delete_note(note_id):
        flash('筆記已成功刪除！', 'success')
    else:
        flash('刪除失敗，請稍後再試。', 'danger')
    return redirect(url_for('note.index'))

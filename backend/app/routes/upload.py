import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app.models import User
from app import db

upload_bp = Blueprint('upload', __name__)


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400

    file = request.files['file']

    # 检查文件名
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'error': '不允许的文件类型'}), 400

    # 确保上传目录存在
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # 生成安全的文件名
    filename = secure_filename(file.filename)
    # 添加时间戳避免重名
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    name, ext = os.path.splitext(filename)
    filename = f"{name}_{timestamp}{ext}"

    # 保存文件
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 返回文件 URL
    return jsonify({
        'message': '文件上传成功',
        'filename': filename,
        'url': f'/uploads/{filename}'
    }), 200


@upload_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传头像"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': '用户不存在'}), 404

    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400

    file = request.files['file']

    # 检查文件名
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400

    # 检查文件类型
    if not allowed_file(file.filename):
        return jsonify({'error': '不允许的文件类型'}), 400

    # 确保上传目录存在
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # 生成安全的文件名
    filename = secure_filename(file.filename)
    # 使用用户 ID 作为文件名的一部分
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    name, ext = os.path.splitext(filename)
    filename = f"avatar_{current_user_id}_{timestamp}{ext}"

    # 保存文件
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    # 返回文件 URL
    avatar_url = f'/uploads/{filename}'

    return jsonify({
        'message': '头像上传成功',
        'url': avatar_url
    }), 200
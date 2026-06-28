import os
from datetime import datetime
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


def save_uploaded_file(file, prefix=''):
    """保存上传的文件"""
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    name, ext = os.path.splitext(filename)
    filename = f"{prefix}{name}_{timestamp}{ext}"

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    return f'/uploads/{filename}'


def validate_upload_request():
    """验证上传请求"""
    if 'file' not in request.files:
        return {'error': '没有上传文件'}, 400

    file = request.files['file']

    if file.filename == '':
        return {'error': '没有选择文件'}, 400

    if not allowed_file(file.filename):
        return {'error': '不允许的文件类型'}, 400

    return {'file': file}, 200


@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    result, status = validate_upload_request()
    if status != 200:
        return jsonify(result), status

    file_url = save_uploaded_file(result['file'])

    return jsonify({
        'message': '文件上传成功',
        'url': file_url
    }), 200


@upload_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传头像"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': '用户不存在'}), 404

    result, status = validate_upload_request()
    if status != 200:
        return jsonify(result), status

    file_url = save_uploaded_file(result['file'], f'avatar_{current_user_id}_')

    return jsonify({
        'message': '头像上传成功',
        'url': file_url
    }), 200
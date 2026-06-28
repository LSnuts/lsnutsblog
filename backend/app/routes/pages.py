from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Page, User

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('', methods=['GET'])
def get_pages():
    """获取页面列表"""
    published_only = request.args.get('published', 'false').lower() == 'true'
    query = Page.query

    if published_only:
        query = query.filter_by(is_published=True)

    pages = query.order_by(Page.created_at.desc()).all()
    return jsonify({'pages': [p.to_dict() for p in pages]}), 200


@pages_bp.route('/<slug>', methods=['GET'])
def get_page(slug):
    """通过slug获取页面"""
    page = Page.query.filter_by(slug=slug).first()
    if not page:
        return jsonify({'error': '页面不存在'}), 404
    return jsonify({'page': page.to_dict()}), 200


@pages_bp.route('/<int:page_id>', methods=['GET'])
def get_page_by_id(page_id):
    """通过ID获取页面"""
    page = Page.query.get(page_id)
    if not page:
        return jsonify({'error': '页面不存在'}), 404
    return jsonify({'page': page.to_dict()}), 200


@pages_bp.route('', methods=['POST'])
@jwt_required()
def create_page():
    """创建页面"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    data = request.get_json()
    if not data or not data.get('title') or not data.get('slug'):
        return jsonify({'error': '标题和slug不能为空'}), 400

    slug = data.get('slug').strip().lower().replace(' ', '-')
    if Page.query.filter_by(slug=slug).first():
        return jsonify({'error': '该slug已被使用'}), 400

    page = Page(
        title=data.get('title'),
        slug=slug,
        content=data.get('content', ''),
        is_published=data.get('is_published', False)
    )
    db.session.add(page)
    db.session.commit()

    return jsonify({'message': '页面创建成功', 'page': page.to_dict()}), 201


@pages_bp.route('/<int:page_id>', methods=['PUT'])
@jwt_required()
def update_page(page_id):
    """更新页面"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    page = Page.query.get(page_id)
    if not page:
        return jsonify({'error': '页面不存在'}), 404

    data = request.get_json()
    if data.get('title'):
        page.title = data.get('title')
    if data.get('slug'):
        new_slug = data.get('slug').strip().lower().replace(' ', '-')
        existing = Page.query.filter_by(slug=new_slug).first()
        if existing and existing.id != page.id:
            return jsonify({'error': '该slug已被使用'}), 400
        page.slug = new_slug
    if 'content' in data:
        page.content = data.get('content')
    if 'is_published' in data:
        page.is_published = data.get('is_published')

    db.session.commit()
    return jsonify({'message': '页面更新成功', 'page': page.to_dict()}), 200


@pages_bp.route('/<int:page_id>', methods=['DELETE'])
@jwt_required()
def delete_page(page_id):
    """删除页面"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    page = Page.query.get(page_id)
    if not page:
        return jsonify({'error': '页面不存在'}), 404

    db.session.delete(page)
    db.session.commit()
    return jsonify({'message': '页面删除成功'}), 200

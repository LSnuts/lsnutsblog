from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Post, User

posts_bp = Blueprint('posts', __name__)


@posts_bp.route('', methods=['GET'])
def get_posts():
    """获取文章列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    published_only = request.args.get('published', 'true').lower() == 'true'

    query = Post.query

    if published_only:
        query = query.filter_by(is_published=True)

    pagination = query.order_by(Post.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    posts = [post.to_dict() for post in pagination.items]

    return jsonify({
        'posts': posts,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """获取单篇文章"""
    post = Post.query.get(post_id)

    if not post:
        return jsonify({'error': '文章不存在'}), 404

    # 增加浏览次数
    post.views += 1
    db.session.commit()

    return jsonify({
        'post': post.to_dict()
    }), 200


@posts_bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    """创建文章"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    data = request.get_json()

    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': '标题和内容不能为空'}), 400

    post = Post(
        title=data.get('title'),
        content=data.get('content'),
        summary=data.get('summary', ''),
        cover_image=data.get('cover_image'),
        is_published=data.get('is_published', False),
        author_id=current_user_id
    )

    db.session.add(post)
    db.session.commit()

    return jsonify({
        'message': '文章创建成功',
        'post': post.to_dict()
    }), 201


@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """更新文章"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    post = Post.query.get(post_id)

    if not post:
        return jsonify({'error': '文章不存在'}), 404

    data = request.get_json()

    if not data:
        return jsonify({'error': '无数据'}), 400

    if data.get('title'):
        post.title = data.get('title')
    if data.get('content'):
        post.content = data.get('content')
    if 'summary' in data:
        post.summary = data.get('summary')
    if 'cover_image' in data:
        post.cover_image = data.get('cover_image')
    if 'is_published' in data:
        post.is_published = data.get('is_published')

    db.session.commit()

    return jsonify({
        'message': '文章更新成功',
        'post': post.to_dict()
    }), 200


@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """删除文章"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    post = Post.query.get(post_id)

    if not post:
        return jsonify({'error': '文章不存在'}), 404

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        'message': '文章删除成功'
    }), 200
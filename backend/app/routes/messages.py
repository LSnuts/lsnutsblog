from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Message, User

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('', methods=['GET'])
def get_messages():
    """获取留言列表（公开）"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    approved_only = request.args.get('approved', 'false').lower() == 'true'

    query = Message.query

    if approved_only:
        query = query.filter_by(is_approved=True)

    pagination = query.order_by(Message.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    messages = [msg.to_dict() for msg in pagination.items]

    return jsonify({
        'messages': messages,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@messages_bp.route('/<int:message_id>', methods=['GET'])
def get_message(message_id):
    """获取单条留言"""
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': '留言不存在'}), 404

    return jsonify({'message': message.to_dict()}), 200


@messages_bp.route('', methods=['POST'])
def create_message():
    """提交留言（公开）"""
    data = request.get_json()

    if not data or not data.get('author') or not data.get('content'):
        return jsonify({'error': '昵称和内容不能为空'}), 400

    message = Message(
        author=data.get('author'),
        email=data.get('email', ''),
        content=data.get('content'),
        is_approved=False  # 新留言默认待审核
    )

    db.session.add(message)
    db.session.commit()

    return jsonify({
        'message': '留言提交成功，等待审核',
        'data': message.to_dict()
    }), 201


@messages_bp.route('/<int:message_id>', methods=['PUT'])
@jwt_required()
def update_message(message_id):
    """更新留言（回复/审核）"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': '留言不存在'}), 404

    data = request.get_json()

    if 'content' in data:
        message.content = data.get('content')
    if 'is_approved' in data:
        message.is_approved = data.get('is_approved')
    if 'reply' in data:
        message.reply = data.get('reply')

    db.session.commit()

    return jsonify({
        'message': '留言更新成功',
        'data': message.to_dict()
    }), 200


@messages_bp.route('/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """删除留言"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': '留言不存在'}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': '留言删除成功'}), 200
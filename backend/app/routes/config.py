from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import BlogConfig, User

config_bp = Blueprint('config', __name__)


@config_bp.route('', methods=['GET'])
def get_all_config():
    """获取所有配置"""
    configs = BlogConfig.query.all()
    config_dict = {config.key: config.value for config in configs}

    return jsonify({
        'config': config_dict
    }), 200


@config_bp.route('/<key>', methods=['GET'])
def get_config(key):
    """获取单个配置"""
    config = BlogConfig.query.filter_by(key=key).first()

    if not config:
        return jsonify({'error': '配置不存在'}), 404

    return jsonify({
        'config': config.to_dict()
    }), 200


@config_bp.route('', methods=['POST'])
@jwt_required()
def set_config():
    """设置配置"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    data = request.get_json()

    if not data or 'key' not in data or 'value' not in data:
        return jsonify({'error': '配置键和值不能为空'}), 400

    key = data.get('key')
    value = data.get('value')

    # 查找或创建配置
    config = BlogConfig.query.filter_by(key=key).first()

    if config:
        config.value = value
    else:
        config = BlogConfig(key=key, value=value)
        db.session.add(config)

    db.session.commit()

    return jsonify({
        'message': '配置更新成功',
        'config': config.to_dict()
    }), 200


@config_bp.route('/batch', methods=['POST'])
@jwt_required()
def batch_set_config():
    """批量设置配置"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    data = request.get_json()

    if not data or not isinstance(data, dict):
        return jsonify({'error': '无效的数据格式'}), 400

    # 更新或创建配置
    for key, value in data.items():
        config = BlogConfig.query.filter_by(key=key).first()

        if config:
            config.value = str(value)
        else:
            config = BlogConfig(key=key, value=str(value))
            db.session.add(config)

    db.session.commit()

    return jsonify({
        'message': '配置批量更新成功'
    }), 200


@config_bp.route('/<key>', methods=['DELETE'])
@jwt_required()
def delete_config(key):
    """删除配置"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user or not user.is_admin:
        return jsonify({'error': '无权限'}), 403

    config = BlogConfig.query.filter_by(key=key).first()

    if not config:
        return jsonify({'error': '配置不存在'}), 404

    db.session.delete(config)
    db.session.commit()

    return jsonify({
        'message': '配置删除成功'
    }), 200
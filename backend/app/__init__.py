from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
import os

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])

    # 注册蓝图
    from app.routes.auth import auth_bp
    from app.routes.posts import posts_bp
    from app.routes.config import config_bp
    from app.routes.upload import upload_bp
    from app.routes.messages import messages_bp
    from app.routes.pages import pages_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    app.register_blueprint(config_bp, url_prefix='/api/config')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')
    app.register_blueprint(messages_bp, url_prefix='/api/messages')
    app.register_blueprint(pages_bp, url_prefix='/api/pages')

    # 提供上传文件的静态访问
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(upload_folder, filename)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app
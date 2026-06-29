import os
from datetime import timedelta

class Config:
    # 密钥配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # 文件上传配置
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # CORS 配置
    CORS_ORIGINS = [
        'http://localhost:5173',
        'http://localhost:3000',
        'https://lsblog.118201820.xyz',
        'http://lsblog.118201820.xyz'
    ]

    # API 域名（用于拼接 uploads 完整路径）
    API_BASE_URL = os.environ.get('API_BASE_URL') or 'http://localhost:5000'

    # 分页配置
    POSTS_PER_PAGE = 10
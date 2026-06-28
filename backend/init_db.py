"""
数据库初始化脚本
运行此脚本创建初始管理员账户
"""
from app import create_app, db
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        # 创建所有表
        db.create_all()

        # 检查是否已有用户
        if User.query.count() == 0:
            print("创建初始管理员账户...")
            admin = User(
                username='admin',
                email='admin@example.com',
                is_admin=True
            )
            admin.set_password('admin123')  # 默认密码，请在首次登录后修改

            db.session.add(admin)
            db.session.commit()
            print("管理员账户创建成功！")
            print("用户名: admin")
            print("密码: admin123")
            print("请登录后立即修改密码！")
        else:
            print("数据库已初始化，跳过管理员账户创建")

if __name__ == '__main__':
    init_db()
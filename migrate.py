from app import app
from extensions import db, bcrypt
from models import User, Book, BorrowRecord

# 创建应用上下文
with app.app_context():
    # 创建所有表
    db.create_all()
    
    # 检查是否已有管理员用户
    admin = User.query.filter_by(username='admin').first()
    
    if not admin:
        # 创建管理员用户
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='admin', email='admin@library.com', password=hashed_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()
        print('管理员用户创建成功')
    else:
        print('管理员用户已存在')
    
    print('数据库初始化完成')
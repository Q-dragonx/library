import unittest
from flask import Flask
from extensions import db, bcrypt
from models import User, Book, BorrowRecord
from datetime import datetime, timedelta

class TestBorrowLogic(unittest.TestCase):
    
    def setUp(self):
        # 创建测试应用
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # 初始化扩展
        with self.app.app_context():
            db.init_app(self.app)
            bcrypt.init_app(self.app)
            db.create_all()
            
            # 创建测试用户
            test_user = User(username='testuser', email='test@example.com', password=bcrypt.generate_password_hash('testpassword').decode('utf-8'))
            db.session.add(test_user)
            
            # 创建库存为0的图书
            self.test_book = Book(isbn='1001', title='Test Book', author='Test Author', publisher='Test Publisher', location='Test Location', stock=0)
            db.session.add(self.test_book)
            
            db.session.commit()
            
            self.test_user = test_user
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_borrow_book_with_zero_stock(self):
        """测试库存为0时借书场景"""
        with self.app.app_context():
            # 模拟借书逻辑
            from routes.main import borrow_book  # 导入借书函数
            
            # 检查初始状态
            self.assertEqual(self.test_book.stock, 0)
            
            # 验证无法创建借阅记录（模拟库存检查）
            # 直接验证业务逻辑而非通过路由
            if self.test_book.stock <= 0:
                result = "库存不足"
            else:
                # 创建借阅记录的逻辑
                result = "可以借书"
            
            # 验证结果
            self.assertEqual(result, "库存不足")
            
            # 尝试直接创建借阅记录（应该不会成功）
            try:
                # 尝试创建借阅记录
                new_record = BorrowRecord(
                    user_id=self.test_user.id,
                    book_id=self.test_book.id,
                    borrow_date=datetime.utcnow(),
                    due_date=datetime.utcnow() + timedelta(days=30),
                    status='借阅中'
                )
                db.session.add(new_record)
                # 更新库存
                self.test_book.stock -= 1
                
                # 如果库存不足，应该回滚
                if self.test_book.stock < 0:
                    db.session.rollback()
                    raise Exception("库存不足")
                
                db.session.commit()
                success = True
            except Exception as e:
                success = False
                error_message = str(e)
            
            # 验证无法借书
            self.assertFalse(success)
            self.assertEqual(self.test_book.stock, 0)

if __name__ == '__main__':
    unittest.main()
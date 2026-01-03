import unittest
from flask import Flask
from extensions import db, bcrypt, login_manager
from models import User, Book, BorrowRecord
from datetime import datetime
from routes.main import main
from routes.auth import auth

class TestBorrowFunctionality(unittest.TestCase):
    
    def setUp(self):
        # 创建测试应用
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_library.db'
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        
        # 初始化扩展
        with self.app.app_context():
            db.init_app(self.app)
            bcrypt.init_app(self.app)
            login_manager.init_app(self.app)
            db.create_all()
            
            # 创建测试用户
            test_user = User(username='testuser', email='test@example.com', password=bcrypt.generate_password_hash('testpassword').decode('utf-8'))
            db.session.add(test_user)
            
            # 创建库存为0的图书
            test_book = Book(isbn='1001', title='Test Book', author='Test Author', publisher='Test Publisher', location='Test Location', stock=0)
            db.session.add(test_book)
            
            db.session.commit()
            
        # 注册蓝图
        self.app.register_blueprint(auth, url_prefix='/')
        self.app.register_blueprint(main, url_prefix='/')
        
        self.client = self.app.test_client()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_borrow_book_with_zero_stock(self):
        """测试库存为0时借书场景"""
        with self.app.app_context():
            # 获取测试用户和图书
            user = User.query.filter_by(username='testuser').first()
            book = Book.query.filter_by(isbn='1001').first()
            
            # 模拟登录
            with self.client.session_transaction() as sess:
                sess['user_id'] = user.id
            
            # 尝试借书
            response = self.client.get(f'/books/{book.id}/borrow', follow_redirects=True)
            
            # 检查是否显示"库存不足"消息
            self.assertIn(b'Book is out of stock', response.data)
            
            # 验证库存仍为0
            updated_book = Book.query.get(book.id)
            self.assertEqual(updated_book.stock, 0)
            
            # 验证没有创建借阅记录
            borrow_records = BorrowRecord.query.filter_by(book_id=book.id).all()
            self.assertEqual(len(borrow_records), 0)

if __name__ == '__main__':
    unittest.main()
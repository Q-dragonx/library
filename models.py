from extensions import db
from datetime import datetime, timedelta
from flask_login import UserMixin

# 用户模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# 图书模型
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=1)
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', '{self.isbn}')"

# 借阅记录模型
class BorrowRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=30))
    return_date = db.Column(db.DateTime, nullable=True)

    @property
    def is_overdue(self):
        if not self.return_date and datetime.utcnow() > self.due_date:
            return True
        return False

    def __repr__(self):
        return f"BorrowRecord(User: {self.user_id}, Book: {self.book_id}, Borrow: {self.borrow_date}, Due: {self.due_date})"
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import os

# 导入扩展
from extensions import db, bcrypt, login_manager

# 初始化应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
with app.app_context():
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

# 导入蓝图
from routes.auth import auth
from routes.main import main

# 注册蓝图
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(main, url_prefix='/')

# 导入模型（移到这里避免循环导入）
from models import User, Book, BorrowRecord

# 登录管理器回调
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
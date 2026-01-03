# 图书管理系统

一个基于Flask和SQLite的简单图书管理系统，支持用户注册、登录、借书、还书和借阅记录查询等功能。

## 功能特点

- 用户管理：注册、登录、个人信息查看
- 图书管理：添加图书、查看图书列表、搜索图书
- 借阅管理：借书、还书、查看借阅记录
- 排名功能：查看借阅排行榜

## 技术栈

- Python 3.8+
- Flask 2.0+
- SQLAlchemy 2.0+
- SQLite
- Bootstrap 5

## 安装和运行

### 1. 克隆仓库

```bash
git clone https://github.com/Q-dragonx/library.git
cd library
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 初始化数据库

```bash
python migrate.py
```

### 4. 运行应用

```bash
python app.py
```

### 5. 访问应用

在浏览器中访问：http://localhost:5000

## 项目结构

```
library/
├── app.py              # 应用主入口
├── extensions.py       # 扩展配置（数据库、登录管理等）
├── models.py           # 数据库模型
├── migrate.py          # 数据库迁移脚本
├── requirements.txt    # 依赖列表
├── routes/
│   ├── __init__.py
│   ├── auth.py         # 认证相关路由
│   └── main.py         # 主要功能路由
├── templates/          # HTML模板
└── instance/           # 数据库文件和临时文件
```

## 测试

运行单元测试：

```bash
python -m pytest
```

## 许可证

MIT
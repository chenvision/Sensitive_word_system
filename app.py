from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from sqlalchemy.testing import db

from sensitive_word.SensitiveWordDetector import SensitiveWordDetector
from werkzeug.security import generate_password_hash, check_password_hash
import os

# print(f"Template folder: {os.path.join(os.getcwd(), 'sensitive_word/templates')}")
# print(f"Static folder: {os.path.join(os.getcwd(), 'webapp/static')}")

#SensitiveWordDetector:自定义的敏感词检测器类
# db = SQLAlchemy()
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password_hash = db.Column(db.String(150), nullable=False)
#
#     def set_password(self, password):#对密码进行哈希存储
#         self.password_hash = generate_password_hash(password)
#
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
app = Flask(__name__, template_folder=os.path.abspath('sensitive_word/templates'), static_folder=os.path.abspath('webapp/static'))
app.secret_key='supersecretkey'
#设置应用密钥
#Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
#配置 Celery 使用 Redis 作为消息队列和结果后端。
def make_celery(app):#从 Flask 应用中创建 Celery 实例
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    return celery
celery=make_celery(app)#使用 make_celery 函数实例化 Celery 对象 celery。
detector = SensitiveWordDetector()
#登录机制
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['root']
#         password = request.form['Cbb2004!']
#         if username=='admin' and password=='Cbb2004!':
#             session['user'] = username
#             return redirect(url_for('admin'))
#         else:
#             return 'Invalid credentials',401
#     return render_template('login.html')
#
# @app.route('/logout')
# def logout():
#     session.pop('user', None)
#     return redirect(url_for('index'))
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user' not in session:
#             return redirect(url_for('login'))
#         return f(*args, **kwargs)
#     return decorated_function
#
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if User.query.filter_by(username=username).first():
#             return 'Username already exists', 400
#         new_user = User(username=username)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html')
@app.route('/')  #定义了根路由 '/'，访问这个路由时，返回 index.html 模板。
def index():
    return render_template('index.html')


@app.route('/admin')  #定义了管理员路由 '/admin'，访问这个路由时，返回 admin.html 模板。
def admin():
    return render_template('admin.html')


@app.route('/api/detect', methods=['POST'])  #定义了 POST 请求路由 '/api/detect'
def detect():
    data = request.get_json()  #获取请求的JSON数据
    text = data.get('text', '')  #提取文本text
    detected_words = detector.detect(text)  #检测文本中的敏感词
    return jsonify({'detected_words': detected_words})


@app.route('/api/admin/add', methods=['POST'])
def add_word():
    data = request.get_json()
    word = data.get('word', '')
    detector.add_sensitive_word(word)
    return jsonify({'message': 'Word added'})

@app.route('/api/admin/delete', methods=['POST'])
def delete_word():
    data = request.get_json()
    word = data.get('word', '')
    detector.remove_sensitive_word(word)
    return jsonify({'message': 'Word deleted'})

@app.route('/api/admin/update_regex', methods=['POST'])
def update_regex():
    data = request.get_json()
    word = data.get('word')
    new_regex = data.get('new_regex')

    if not word or not new_regex:
        return jsonify({'message': 'Word and new regex must be provided'}), 400

    # 更新敏感词的正则表达式
    detector.db.update_word(word, word, new_regex, detector.db.get_word_type(word))  # 假设 get_word_type 返回现有的类型

    return jsonify({'message': f'Regex for word "{word}" updated successfully'})


@app.route('/api/admin/delete_regex', methods=['POST'])
def delete_regex():
    data = request.get_json()
    regex = data.get('regex', '')
    detector.remove_sensitive_word(regex)
    return jsonify({'message': 'Regex deleted'})

@app.route('/api/admin/test_regex', methods=['POST'])
def test_regex():
    data = request.get_json()
    text = data.get('text', '')
    detected_words = detector.detect(text)  # 测试文本中是否有匹配的正则表达式
    return jsonify({'matched': len(detected_words) > 0})

@app.route('/api/admin/words', methods=['GET'])
def get_words():
    words = detector.db.get_all_words()
    return jsonify({'words': words})

if __name__ == '__main__':
    app.run(debug=True, port=3389)
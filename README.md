## 敏感词检测系统

这是一个基于 Flask 框架的敏感词检测系统，包含以下功能：

- **敏感词检测：** 使用 `SensitiveWordDetector` 类检测文本中的敏感词。
- **管理员界面：** 提供管理员界面，用于添加、删除敏感词和正则表达式。
- **用户注册和登录：** 提供用户注册和登录功能，并使用密码哈希保护用户密码。
- **异步任务：** 使用 Celery 框架处理异步任务，提高系统效率。

### 项目结构

```
sensitive_word_system  
│  
├── .venv/                  # 虚拟环境目录  
├── sensitive_word/  
│   ├── templates/  
│   │   ├── admin.html  
│   │   ├── index.html  
│   │   ├── login.html  
│   │   └── register.html  
│   ├── __init__.py  
│   ├── database.py  
│   ├── SensitiveWordDetector.py  
│   └── views.py            # 假设所有视图函数都在这里  
├── tests/                  # 测试目录  
├── webapp/  
│   ├── static/  
│   │   ├── css/  
│   │   │   └── styles.css  
│   │   └── js/  
│   │       ├── admin_scripts.js  
│   │       └── scripts.js  
├── .gitignore  
├── app.py  
├── crawler.py  
└── 1.docx  
```

### 使用方法

1. **安装依赖：**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置数据库：**
   - 创建一个数据库（例如 SQLite 或 PostgreSQL）。
   - 在 `app.py` 中配置数据库连接信息，例如：

     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite 数据库
     ```

3. **启动应用：**
   ```bash
   python app.py
   ```

4. **访问应用：**
   - 访问 `http://127.0.0.1:3389/`，进入主页。
   - 访问 `http://127.0.0.1:3389/admin`，进入管理员界面。

### 功能说明

- **敏感词检测：**
   - 使用 `POST` 方法访问 `/api/detect` 接口，传入需要检测的文本，返回检测到的敏感词列表。
   - 例如：
     ```json
     {
       "text": "这是一个敏感词测试"
     }
     ```

- **管理员界面：**
   - 添加敏感词：
     - 使用 `POST` 方法访问 `/api/admin/add` 接口，传入敏感词，添加新的敏感词。
     - 例如：
       ```json
       {
         "word": "敏感词"
       }
       ```

   - 删除敏感词：
     - 使用 `POST` 方法访问 `/api/admin/delete` 接口，传入敏感词，删除现有敏感词。
     - 例如：
       ```json
       {
         "word": "敏感词"
       }
       ```

   - 添加正则表达式：
     - 使用 `POST` 方法访问 `/api/admin/add_regex` 接口，传入正则表达式，添加新的正则表达式。
     - 例如：
       ```json
       {
         "regex": "敏感[\\w\\s]*" 
       }
       ```

   - 删除正则表达式：
     - 使用 `POST` 方法访问 `/api/admin/delete_regex` 接口，传入正则表达式，删除现有正则表达式。
     - 例如：
       ```json
       {
         "regex": "敏感[\\w\\s]*" 
       }
       ```

   - 测试正则表达式：
     - 使用 `POST` 方法访问 `/api/admin/test_regex` 接口，传入文本，测试文本中是否包含匹配的正则表达式。
     - 例如：
       ```json
       {
         "text": "这是一个敏感词测试"
       }
       ```

   - 获取所有敏感词：
     - 使用 `GET` 方法访问 `/api/admin/words` 接口，获取所有敏感词列表。

- **用户注册和登录：**
   - 注册新用户：
     - 访问 `/register` 页面，填写用户名和密码，提交注册。
   - 登录：
     - 访问 `/login` 页面，输入用户名和密码，提交登录。

### 注意事项

-  请根据实际需求修改代码中的数据库配置、敏感词库和正则表达式。
-  建议使用安全的哈希算法（例如 scrypt）对用户密码进行哈希处理。
-  注意代码安全，防止 SQL 注入和跨站脚本攻击。

### 未来改进

-  添加更多敏感词类型，例如表情符号、特殊字符。
-  实现敏感词替换功能，将敏感词替换为其他字符。
-  使用机器学习模型进行敏感词识别，提高识别准确率。
-  使用 Docker 部署应用，方便部署和维护。

希望本 README 能帮助您了解和使用该敏感词检测系统。如有任何疑问，请随时提出。
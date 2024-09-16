import re
import mysql.connector


class Database:
    def __init__(self, host='localhost', user='root', password='Cbb2004!', database='sensitive_word_system'):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              word VARCHAR(255) NOT NULL UNIQUE,
                              regex TEXT NOT NULL,
                              type TINYINT NOT NULL
                              );''')
        cursor.close()
        self.conn.commit()

    def generate_regex(self, word):
        # 生成初始正则表达式，将输入的敏感词转换为一个可以匹配中英文、数字和常见标点的正则表达式
        regex = ''
        prev_char_is_chinese = False
        for char in word:
            if '\u4e00' <= char <= '\u9fa5':  # 中文字符
                if prev_char_is_chinese:
                    regex += f'[\u4e00-\u9fa5]{{0,1}}{char}'
                else:
                    regex += char
                prev_char_is_chinese = True
            elif char.isalpha():  # 英文字符
                regex += r'\b[a-zA-Z]+\b'  # 匹配完整单词
                prev_char_is_chinese = False
            elif char.isdigit():  # 数字
                regex += r'\b\d+\b'  # 匹配完整数字
                prev_char_is_chinese = False
            else:  # 其他字符，如标点符号
                regex += re.escape(char)
                prev_char_is_chinese = False
        return regex

    def validate_regex(self, regex):
        try:
            re.compile(regex)
            return True
        except re.error:
            return False


    def add_word(self, word, regex=None, word_type=0):
        # 确保 word_type 是整数
        if not isinstance(word_type, int):
            print(f"Invalid word_type: '{word_type}'. It must be an integer.")
            return

        # 如果没有提供 regex，生成一个默认的正则表达式
        if regex is None:
            regex = self.generate_regex(word)
        else:
            # 替换 \x{xxxx} 为 \uxxxx
            regex = re.sub(r'\\x\{([0-9A-Fa-f]{4})\}', r'\\u\1', regex)

            # 删除末尾的 /u 修饰符
            regex = re.sub(r'/u$', '', regex)

        if not self.validate_regex(regex):
            print(f"Invalid regex: {regex}")
            return

        # 检查是否已存在该词
        if self.word_exists(word):
            print(f"Word '{word}' already exists.")
            return

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO words (word, regex, type) VALUES (%s, %s, %s)", (word, regex, word_type))
        cursor.close()
        self.conn.commit()
        print(f"Word '{word}' added successfully with type '{word_type}'.")

    def word_exists(self, word):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM words WHERE word = %s", (word,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] > 0

    def remove_word(self, word):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM words WHERE word=%s", (word,))
        cursor.close()
        self.conn.commit()

    def get_all_words(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT word, regex, type FROM words")
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_word_type(self, word):
        cursor = self.conn.cursor()
        cursor.execute("SELECT type FROM words WHERE word = %s", (word,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]

    def update_word(self, old_word, new_word, new_regex, new_type):
        if not isinstance(new_type, int):
            print(f"Invalid new_type: '{new_type}'. It must be an integer.")
            return

        if self.validate_regex(new_regex):
            cursor = self.conn.cursor()
            cursor.execute("UPDATE words SET word=%s, regex=%s, type=%s WHERE word=%s",
                           (new_word, new_regex, new_type, old_word))
            cursor.close()
            self.conn.commit()
        else:
            print(f"Invalid regex: {new_regex}")

    def close(self):
        self.conn.close()

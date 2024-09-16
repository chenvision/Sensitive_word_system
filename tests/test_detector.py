import re

class RegexGenerator:
    @staticmethod
    def generate(word):
        regex = ''
        prev_char_is_chinese = False
        for char in word:
            if '\u4e00' <= char <= '\u9fa5':  # 中文字符
                if prev_char_is_chinese:
                    regex += f'[\u4e00-\u9fa5]{{0,1}}{char}'
                else:
                    regex += f'{char}'
                prev_char_is_chinese = True
            elif char.isalpha():  # 英文字符
                regex += f'[a-zA-Z][\\s\\W]*'
                prev_char_is_chinese = False
            elif char.isdigit():  # 数字
                regex += f'\\d[\\s\\W]*'
                prev_char_is_chinese = False
            else:  # 其他字符，如标点符号
                regex += re.escape(char) + '[\\s\\W]*'
                prev_char_is_chinese = False

        return regex.rstrip('[\\s\\W]*')

# 示例使用
word = "四中全会"
regex = RegexGenerator.generate(word)
print(f"Word: {word}\nGenerated Regex: {regex}")


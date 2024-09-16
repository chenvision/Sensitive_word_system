from .trie import Trie
from .database import Database
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

class RegexDetector:
    def __init__(self, patterns):
        self.patterns = [re.compile(pattern) for pattern in patterns]

    def detect(self, text):
        detected_words = []
        for pattern in self.patterns:
            # 使用 re.finditer
            for match in pattern.finditer(text):
                detected_words.append(match.group())
        return detected_words

class DynamicTrie(Trie):
    def __init__(self):
        super().__init__()


    def delete(self,word):
        def _delete(node,word,depth):
            if not node:
                return False
            if depth == len(word):
                if node.is_end_of_word:
                    node.is_end_of_word = False
                return len(node.childrem)==0
            char = word[depth]
            if char in node.children and _delete(node.children[char],word,depth+1):
                del node.children[char]
                return not node.is_end_of_word and len(node.children)==0
            return False
        _delete(self.root,word,0)
    def insert(self,word):
        def _insert(node,word,depth):
            if not node:
                return False
            char = word[depth]
            if char not in node.children:
                node.children[char] =TrieNode()
            if depth == len(word)-1:
                node.children[char].is_end_of_word = True
            else:
                _insert(node.children[char],word,depth+1)
            _insert(self.root,word,0)


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word=False

class SensitiveWordDetector:
    def __init__(self, sensitive_words=None):
        self.trie = Trie()
        self.db = Database()
        self.regex_detector = None

        if sensitive_words is None:
            sensitive_words = self.db.get_all_words()

        self.patterns = []
        for word, existing_regex, word_type in sensitive_words:
            self.trie.insert(word)

            if existing_regex:
                regex = existing_regex
            else:
                regex = RegexGenerator.generate(word)
                if regex:
                    self.db.update_word(word, regex)

            self.patterns.append(regex)

        self.regex_detector = RegexDetector(self.patterns)

    def detect(self,text):#使用正则表达式和trie树进行检测
        detected_words=self.trie.search(text)
        detected_words+= self.regex_detector.detect(text)
        return detected_words

    def replace(self,text,replacements='*'):
        detected_words=self.detect(text)
        for word in detected_words:
            text = text.replace(word,replacements*len(word))
        return text

    def add_sensitive_word(self,word):
        self.trie.insert(word)
        regex=RegexGenerator.generate(word)
        self.db.add_word(word,regex)
        self.patterns.append(regex)
        self.regex_detector = RegexDetector(self.patterns)#更新正则检测器


    def remove_sensitive_word(self,word):
        self.trie.delete(word)
        self.db.remove_word(word)
        self.patterns=[pattern for pattern in self.patterns if not re.match(pattern,word)]
        self.regex_detector = RegexDetector(self.patterns)

    def update_sensitive_word(self,old_word,new_word):
        self.trie.delete(old_word)
        self.trie.insert(new_word)
        regex=RegexGenerator.generate(new_word)
        self.db.update_word(old_word,new_word,regex)
        #update regex
        self.patterns=[regex if re.match(pattern,old_word) else pattern for pattern in self.patterns]
        self.regex_detector = RegexDetector(self.patterns)

from .trie import Trie

class SensitiveWordDetector:
    def __init__(self,sensitive_words):
        self.trie = Trie()
        for word in sensitive_words:
            self.trie.insert(word)
    #初始化敏感词检测器，构造函数接收一个敏感词列表，将这些敏感词插入Trie中
    def detect(self,word):#检测敏感词
        return self.trie.search(word)

    def replace(self,text,replacement='*'):#替换敏感词
        detected_words=self.detect(text)
        for word in detected_words:
            text=text.replace(word,replacement * len(word))
        return text


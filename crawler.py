from docx import Document
import re
from sensitive_word.database import Database
doc=Document('D:/sensitive_word_system/1.docx')
db = Database()
def parse_data(doc):
    for paragraph in doc.paragraphs:
        text=paragraph.text.strip()
        if not text:
            continue
        match = re.match(r'\[(\d+),\"(.*?)\",\"(.*?)\"\]', text)
        if match:
            word_type=int(match.group(1))
            word=match.group(2)
            regex=match.group(3)
            regex=regex.strip("/")
            db.add_word(word,regex,word_type)
parse_data(doc)
db.close()
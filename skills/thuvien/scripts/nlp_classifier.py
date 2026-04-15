import json
import os
import re
import math
from collections import defaultdict

# TF-IDF Naive Bayes Classifier cực nhẹ, không cần thư viện ngoài
class SimpleTextClassifier:
    def __init__(self, data_file):
        self.data_file = data_file
        self.vocab = set()
        self.word_counts = {'positive': defaultdict(int), 'negative': defaultdict(int)}
        self.doc_counts = {'positive': 0, 'negative': 0}
        self.stop_words = {'và', 'của', 'về', 'các', 'cho', 'trong', 'để', 'có', 'được', 'là', 'những', 'đã', 'với', 'từ', 'do', 'tại'}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.word_counts = data.get('word_counts', {'positive': {}, 'negative': {}})
                    self.doc_counts = data.get('doc_counts', {'positive': 0, 'negative': 0})
                    # Reconstruct vocab
                    for word in self.word_counts['positive']: self.vocab.add(word)
                    for word in self.word_counts['negative']: self.vocab.add(word)
            except Exception:
                pass

    def save_data(self):
        data = {
            'word_counts': self.word_counts,
            'doc_counts': self.doc_counts
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def tokenize(self, text):
        # Chuyển thành chữ thường, bỏ dấu câu và số
        text = text.lower()
        words = re.findall(r'\b[a-zàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+\b', text)
        return [w for w in words if w not in self.stop_words and len(w) > 1]

    def train(self, documents, labels):
        """documents: list of strings, labels: list of 'positive' or 'negative'"""
        for doc, label in zip(documents, labels):
            words = self.tokenize(doc)
            self.doc_counts[label] += 1
            # Dùng set để đếm theo Document Frequency (DF) hoặc count term
            for word in words:
                self.vocab.add(word)
                self.word_counts[label][word] = self.word_counts[label].get(word, 0) + 1
        self.save_data()

    def predict(self, text):
        words = self.tokenize(text)
        if not words or (self.doc_counts['positive'] + self.doc_counts['negative']) == 0:
            return 0.5 # Chưa học đủ

        scores = {'positive': 0.0, 'negative': 0.0}
        
        # Laplacian Smoothing
        vocab_size = len(self.vocab)
        total_docs = sum(self.doc_counts.values())
        
        for label in ['positive', 'negative']:
            # P(Class)
            class_prob = self.doc_counts[label] / total_docs
            scores[label] += math.log(class_prob)
            
            # P(Word|Class)
            total_words_in_class = sum(self.word_counts[label].values())
            for word in words:
                word_count = self.word_counts[label].get(word, 0)
                word_prob = (word_count + 1) / (total_words_in_class + vocab_size) # Smoothing +1
                scores[label] += math.log(word_prob)

        # Trả về điểm tự tin cho 'positive' (dùng softmax-like function)
        try:
            # Prevent overflow
            diff = scores['positive'] - scores['negative']
            if diff > 100: prob_pos = 1.0
            elif diff < -100: prob_pos = 0.0
            else: prob_pos = 1 / (1 + math.exp(-diff))
        except OverflowError:
            prob_pos = 0.5

        return prob_pos

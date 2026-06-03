#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 6: Классификация текстов

Этот модуль демонстрирует различные методы классификации:
- Простая классификация по ключевым словам
- TF-IDF
- Наивный байесовский классификатор
"""

import re
from typing import List, Tuple, Dict
from collections import Counter
import math

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
except ImportError:
    print("Предупреждение: scikit-learn не установлена. Установите: pip install scikit-learn")
    TfidfVectorizer = None


class TextClassifier:
    """
    Класс для классификации текстов.
    """
    
    def __init__(self):
        """Инициализация классификатора."""
        # Ключевые слова для различных категорий
        self.keywords = {
            'спорт': ['футбол', 'хоккей', 'теннис', 'спорт', 'матч', 'команда', 'игрок', 'победа'],
            'политика': ['президент', 'парламент', 'закон', 'политика', 'выборы', 'партия', 'депутат'],
            'технология': ['компьютер', 'программа', 'интернет', 'технология', 'код', 'сервер', 'база данных'],
            'здоровье': ['врач', 'больница', 'болезнь', 'лечение', 'здоровье', 'медицина', 'лекарство'],
            'экономика': ['экономика', 'торговля', 'рынок', 'цена', 'инвестиции', 'банк', 'валюта']
        }
    
    def classify_by_keywords(self, text: str) -> Tuple[str, float]:
        """
        Классификация текста по ключевым словам.
        
        Args:
            text: Текст для классификации
            
        Returns:
            Кортеж (категория, уверенность)
        """
        text_lower = text.lower()
        
        category_scores = {}
        for category, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            category_scores[category] = score
        
        if max(category_scores.values()) == 0:
            return "неизвестная", 0.0
        
        best_category = max(category_scores, key=category_scores.get)
        confidence = category_scores[best_category] / sum(category_scores.values())
        
        return best_category, confidence
    
    def calculate_tf(self, words: List[str]) -> Dict[str, float]:
        """
        Расчет TF (Term Frequency).
        
        Args:
            words: Список слов
            
        Returns:
            Словарь с TF для каждого слова
        """
        total_words = len(words)
        word_counts = Counter(words)
        
        tf = {}
        for word, count in word_counts.items():
            tf[word] = count / total_words
        
        return tf
    
    def calculate_idf(self, documents: List[List[str]]) -> Dict[str, float]:
        """
        Расчет IDF (Inverse Document Frequency).
        
        Args:
            documents: Список документов (каждый - список слов)
            
        Returns:
            Словарь с IDF для каждого слова
        """
        total_docs = len(documents)
        word_doc_count = Counter()
        
        for doc in documents:
            unique_words = set(doc)
            word_doc_count.update(unique_words)
        
        idf = {}
        for word, count in word_doc_count.items():
            idf[word] = math.log(total_docs / (1 + count))
        
        return idf
    
    def calculate_tfidf(self, text: str, all_texts: List[str]) -> Dict[str, float]:
        """
        Расчет TF-IDF для текста.
        
        Args:
            text: Текст для анализа
            all_texts: Список всех текстов (для расчета IDF)
            
        Returns:
            Словарь с TF-IDF для каждого слова
        """
        # Подготовка текстов
        documents = [
            re.findall(r'\b\w+\b', t.lower()) for t in all_texts
        ]
        
        # Расчет TF и IDF
        tf = self.calculate_tf(re.findall(r'\b\w+\b', text.lower()))
        idf = self.calculate_idf(documents)
        
        # Расчет TF-IDF
        tfidf = {}
        for word, tf_value in tf.items():
            idf_value = idf.get(word, 0)
            tfidf[word] = tf_value * idf_value
        
        return tfidf


def main():
    """
    Демонстрация классификации текстов.
    """
    print("="*70)
    print("ПРИМЕР 6: КЛАССИФИКАЦИЯ ТЕКСТОВ")
    print("="*70)
    
    classifier = TextClassifier()
    
    # Примеры текстов
    texts = [
        "Футбольная команда выиграла матч со счетом 3-1. Голы забили три разных игрока.",
        "Правительство приняло новый закон о налогах. Депутаты голосовали единогласно.",
        "Новый алгоритм машинного обучения показал отличные результаты. Код опубликован на GitHub.",
        "Врачи рекомендуют регулярные упражнения для здоровья. Болезнь можно предотвратить профилактикой.",
        "Рынок акций показал рост на 5%. Инвестиции в технологии привлекают больше капитала."
    ]
    
    print("\n" + "-"*70)
    print("КЛАССИФИКАЦИЯ ПО КЛЮЧЕВЫМ СЛОВАМ:")
    print("-"*70)
    
    for i, text in enumerate(texts, 1):
        category, confidence = classifier.classify_by_keywords(text)
        print(f"\nТекст {i}: {text[:60]}...")
        print(f"  Категория: {category}")
        print(f"  Уверенность: {confidence:.2f}")
    
    print("\n" + "-"*70)
    print("TF-IDF АНАЛИЗ:")
    print("-"*70)
    
    test_text = texts[0]
    tfidf = classifier.calculate_tfidf(test_text, texts)
    
    print(f"\nТекст: {test_text}")
    print(f"\nТоп 10 слов по TF-IDF:")
    print(f"{'Слово':<15} {'TF-IDF':<10}")
    print("-"*25)
    
    sorted_tfidf = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:10]
    for word, score in sorted_tfidf:
        print(f"{word:<15} {score:<10.4f}")
    
    print("\n" + "="*70)
    print("\nОбъяснение TF-IDF:")
    print("- TF: Как часто слово встречается в документе")
    print("- IDF: Как редко слово встречается во всех документах")
    print("- TF-IDF: Произведение TF и IDF (важность слова в документе)")
    print("="*70)


if __name__ == "__main__":
    main()

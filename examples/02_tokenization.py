#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 2: Токенизация текста

Этот модуль демонстрирует различные методы токенизации:
- Токенизация по пробелам
- Регулярные выражения
- NLTK токенизация
- spaCy токенизация
"""

import re
import nltk
from typing import List

try:
    import spacy
except ImportError:
    print("Предупреждение: spacy не установлена. Установите: pip install spacy")
    spacy = None


class Tokenizer:
    """
    Класс для токенизации текста различными методами.
    """
    
    @staticmethod
    def whitespace_tokenize(text: str) -> List[str]:
        """
        Токенизация по пробелам (самый простой способ).
        
        Args:
            text: Исходный текст
            
        Returns:
            Список токенов
        """
        return text.split()
    
    @staticmethod
    def regex_tokenize(text: str) -> List[str]:
        """
        Токенизация с использованием регулярных выражений.
        
        Args:
            text: Исходный текст
            
        Returns:
            Список токенов
        """
        # Паттерн для выделения слов и пунктуации отдельно
        pattern = r'\b\w+\b|[^\w\s]'
        return re.findall(pattern, text, re.UNICODE)
    
    @staticmethod
    def sentence_tokenize(text: str) -> List[str]:
        """
        Разделение текста на предложения.
        
        Args:
            text: Исходный текст
            
        Returns:
            Список предложений
        """
        # Простой способ разделения по точке, вопросительному и восклицательному знакам
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    @staticmethod
    def nltk_tokenize(text: str) -> List[str]:
        """
        Токенизация с использованием NLTK.
        
        Args:
            text: Исходный текст
            
        Returns:
            Список токенов
        """
        try:
            return nltk.word_tokenize(text)
        except LookupError:
            # Если данные не загружены, используем простую токенизацию
            print("Загрузка данных NLTK...")
            nltk.download('punkt', quiet=True)
            return nltk.word_tokenize(text)
    
    @staticmethod
    def spacy_tokenize(text: str) -> List[str]:
        """
        Токенизация с использованием spaCy.
        
        Args:
            text: Исходный текст
            
        Returns:
            Список токенов
        """
        if spacy is None:
            return []
        
        try:
            nlp = spacy.load('ru_core_news_sm')
            doc = nlp(text)
            return [token.text for token in doc]
        except OSError:
            print("Модель ru_core_news_sm не найдена.")
            print("Установите: python -m spacy download ru_core_news_sm")
            return []


def compare_tokenizers():
    """
    Сравнение различных методов токенизации.
    """
    text = "Обработка естественного языка (НЛП) — это область искусственного интеллекта."
    
    print("="*70)
    print("ПРИМЕР 2: ТОКЕНИЗАЦИЯ ТЕКСТА")
    print("="*70)
    print(f"\nИсходный текст:\n{text}")
    
    tokenizer = Tokenizer()
    
    print("\n" + "-"*70)
    print("1. ТОКЕНИЗАЦИЯ ПО ПРОБЕЛАМ:")
    print("-"*70)
    tokens = tokenizer.whitespace_tokenize(text)
    print(f"Количество токенов: {len(tokens)}")
    print(f"Токены: {tokens}")
    
    print("\n" + "-"*70)
    print("2. ТОКЕНИЗАЦИЯ С РЕГУЛЯРНЫМИ ВЫРАЖЕНИЯМИ:")
    print("-"*70)
    tokens = tokenizer.regex_tokenize(text)
    print(f"Количество токенов: {len(tokens)}")
    print(f"Токены: {tokens}")
    
    print("\n" + "-"*70)
    print("3. РАЗДЕЛЕНИЕ НА ПРЕДЛОЖЕНИЯ:")
    print("-"*70)
    sentences = tokenizer.sentence_tokenize(text)
    print(f"Количество предложений: {len(sentences)}")
    for i, sent in enumerate(sentences, 1):
        print(f"  {i}. {sent}")
    
    print("\n" + "-"*70)
    print("4. ТОКЕНИЗАЦИЯ С NLTK:")
    print("-"*70)
    tokens = tokenizer.nltk_tokenize(text)
    print(f"Количество токенов: {len(tokens)}")
    print(f"Токены: {tokens}")
    
    print("\n" + "-"*70)
    print("5. ТОКЕНИЗАЦИЯ С SPACY:")
    print("-"*70)
    tokens = tokenizer.spacy_tokenize(text)
    if tokens:
        print(f"Количество токенов: {len(tokens)}")
        print(f"Токены: {tokens}")
    else:
        print("spaCy недоступна или модель не установлена")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    compare_tokenizers()

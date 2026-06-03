#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 3: Лемматизация и стемминг

Этот модуль демонстрирует различные методы нормализации слов:
- Простой стемминг
- pymorphy2 лемматизация
- Сравнение эффективности
"""

import re
from typing import List, Tuple

try:
    import pymorphy2
except ImportError:
    print("Предупреждение: pymorphy2 не установлена. Установите: pip install pymorphy2")
    pymorphy2 = None

try:
    import nltk
except ImportError:
    nltk = None


class Stemmer:
    """
    Простой класс для стемминга русских слов.
    """
    
    @staticmethod
    def simple_stem(word: str) -> str:
        """
        Простой стемминг путем удаления суффиксов.
        
        Args:
            word: Слово для обработки
            
        Returns:
            Основа слова
        """
        # Удаляем окончания
        suffixes = ['ция', 'сия', 'ние', 'ение', 'ость', 'ости', 'ый', 'ая', 'ое', 'ый']
        word_lower = word.lower()
        
        for suffix in suffixes:
            if word_lower.endswith(suffix) and len(word_lower) > len(suffix) + 2:
                return word_lower[:-len(suffix)]
        
        return word_lower


class Lemmatizer:
    """
    Класс для лемматизации текста.
    """
    
    def __init__(self):
        """Инициализация морфологического анализатора."""
        if pymorphy2:
            self.morph = pymorphy2.MorphAnalyzer()
        else:
            self.morph = None
    
    def lemmatize_word(self, word: str) -> str:
        """
        Лемматизация одного слова с использованием pymorphy2.
        
        Args:
            word: Слово для лемматизации
            
        Returns:
            Лемма слова
        """
        if self.morph is None:
            return word
        
        parsed = self.morph.parse(word)[0]
        return parsed.normal_form
    
    def get_pos(self, word: str) -> str:
        """
        Получение части речи слова.
        
        Args:
            word: Слово
            
        Returns:
            Часть речи
        """
        if self.morph is None:
            return "unknown"
        
        parsed = self.morph.parse(word)[0]
        return parsed.tag.POS
    
    def lemmatize_text(self, text: str) -> str:
        """
        Лемматизация текста.
        
        Args:
            text: Исходный текст
            
        Returns:
            Лемматизированный текст
        """
        words = text.split()
        lemmas = [self.lemmatize_word(word) for word in words]
        return ' '.join(lemmas)
    
    def analyze_text(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Подробный анализ текста (слово, лемма, часть речи).
        
        Args:
            text: Исходный текст
            
        Returns:
            Список кортежей (слово, лемма, часть речи)
        """
        words = text.split()
        result = []
        
        for word in words:
            lemma = self.lemmatize_word(word)
            pos = self.get_pos(word)
            result.append((word, lemma, pos))
        
        return result


def main():
    """
    Демонстрация лемматизации и стемминга.
    """
    print("="*70)
    print("ПРИМЕР 3: ЛЕММАТИЗАЦИЯ И СТЕММИНГ")
    print("="*70)
    
    # Примеры слов
    words = [
        "обработка", "обрабатывали", "обработанный",
        "язык", "языков", "языкам",
        "алгоритм", "алгоритмы", "алгоритмов",
        "интеллект", "интеллектуальный", "интеллектуально",
        "машина", "машины", "машинного"
    ]
    
    stemmer = Stemmer()
    lemmatizer = Lemmatizer()
    
    print("\n" + "-"*70)
    print("СРАВНЕНИЕ МЕТОДОВ (Слово -> Стемминг -> Лемматизация):")
    print("-"*70)
    print(f"{'Слово':<20} {'Стемминг':<20} {'Лемма':<20} {'Часть речи':<15}")
    print("-"*70)
    
    for word in words:
        stem = stemmer.simple_stem(word)
        lemma = lemmatizer.lemmatize_word(word)
        pos = lemmatizer.get_pos(word)
        print(f"{word:<20} {stem:<20} {lemma:<20} {pos:<15}")
    
    print("\n" + "-"*70)
    print("АНАЛИЗ ПРЕДЛОЖЕНИЯ:")
    print("-"*70)
    
    sentence = "Обработка естественных языков позволяет компьютерам обрабатывать текстовую информацию"
    print(f"\nИсходное предложение:\n{sentence}")
    
    analysis = lemmatizer.analyze_text(sentence)
    print(f"\n{'Слово':<20} {'Лемма':<20} {'Часть речи':<15}")
    print("-"*70)
    for word, lemma, pos in analysis:
        print(f"{word:<20} {lemma:<20} {pos:<15}")
    
    print("\n" + "-"*70)
    print("ЛЕММАТИЗИРОВАННОЕ ПРЕДЛОЖЕНИЕ:")
    print("-"*70)
    lemmatized = lemmatizer.lemmatize_text(sentence)
    print(f"\n{lemmatized}")
    
    print("\n" + "="*70)
    print("\nЗамечание: Лемматизация более точная, чем стемминг, так как возвращает")
    print("действительные слова (леммы) из словаря, а стемминг просто удаляет суффиксы.")
    print("="*70)


if __name__ == "__main__":
    main()

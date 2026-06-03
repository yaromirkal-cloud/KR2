#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 1: Предварительная обработка текста

Этот модуль демонстрирует основные операции предварительной обработки текста:
- Удаление пунктуации
- Преобразование в нижний регистр
- Удаление лишних пробелов
- Удаление специальных символов
- Удаление стоп-слов
"""

import re
import string
from typing import List, Set


class TextPreprocessor:
    """
    Класс для предварительной обработки текста.
    """
    
    def __init__(self):
        """Инициализация стоп-слов для русского языка."""
        self.russian_stopwords = {
            'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'а', 'то', 'все',
            'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы',
            'по', 'только', 'ее', 'можно', 'при', 'наконец', 'два', 'об', 'другой',
            'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про',
            'всех', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем',
            'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чем', 'чем', 'вдруг',
            'ни', 'вот', 'когда', 'даже', 'ну', 'вдруг', 'ль', 'если', 'уже', 'или',
            'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'го', 'почти', 'мне'
        }
    
    def to_lowercase(self, text: str) -> str:
        """
        Преобразование текста в нижний регистр.
        
        Args:
            text: Исходный текст
            
        Returns:
            Текст в нижнем регистре
        """
        return text.lower()
    
    def remove_punctuation(self, text: str) -> str:
        """
        Удаление пунктуации из текста.
        
        Args:
            text: Исходный текст
            
        Returns:
            Текст без пунктуации
        """
        return text.translate(str.maketrans('', '', string.punctuation))
    
    def remove_special_characters(self, text: str) -> str:
        """
        Удаление специальных символов и цифр.
        
        Args:
            text: Исходный текст
            
        Returns:
            Очищенный текст
        """
        return re.sub(r'[^а-яА-ЯёЁ\s]', '', text)
    
    def remove_extra_spaces(self, text: str) -> str:
        """
        Удаление лишних пробелов.
        
        Args:
            text: Исходный текст
            
        Returns:
            Текст с единичными пробелами
        """
        return ' '.join(text.split())
    
    def remove_stopwords(self, words: List[str]) -> List[str]:
        """
        Удаление стоп-слов.
        
        Args:
            words: Список слов
            
        Returns:
            Список слов без стоп-слов
        """
        return [word for word in words if word not in self.russian_stopwords]
    
    def preprocess(self, text: str, remove_stops: bool = True) -> str:
        """
        Полная предварительная обработка текста.
        
        Args:
            text: Исходный текст
            remove_stops: Удалять ли стоп-слова
            
        Returns:
            Обработанный текст
        """
        # 1. Преобразование в нижний регистр
        text = self.to_lowercase(text)
        
        # 2. Удаление специальных символов
        text = self.remove_special_characters(text)
        
        # 3. Удаление пунктуации
        text = self.remove_punctuation(text)
        
        # 4. Удаление лишних пробелов
        text = self.remove_extra_spaces(text)
        
        # 5. Удаление стоп-слов (опционально)
        if remove_stops:
            words = text.split()
            words = self.remove_stopwords(words)
            text = ' '.join(words)
        
        return text


def main():
    """
    Демонстрация предварительной обработки текста.
    """
    print("="*70)
    print("ПРИМЕР 1: ПРЕДВАРИТЕЛЬНАЯ ОБРАБОТКА ТЕКСТА")
    print("="*70)
    
    preprocessor = TextPreprocessor()
    
    # Примеры текстов
    texts = [
        "Обработка естественного языка — это важная область искусственного интеллекта!",
        "Python 3.9+ — отличный выбор для работы с НЛП. Скорость и удобство!",
        "Машинное обучение позволяет компьютерам учиться на примерах."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\nТекст {i}:")
        print(f"Исходный:    {text}")
        print(f"Обработанный (со стоп-словами): {preprocessor.preprocess(text, remove_stops=False)}")
        print(f"Обработанный (без стоп-слов):   {preprocessor.preprocess(text, remove_stops=True)}")
    
    print("\n" + "="*70)
    print("Количество стоп-слов в русском языке:", len(preprocessor.russian_stopwords))
    print("="*70)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 4: Анализ тональности текста

Этот модуль демонстрирует различные методы анализа тональности:
- Словарный метод
- TextBlob
- Простая классификация
"""

from typing import Tuple, List
import re

try:
    from textblob import TextBlob
except ImportError:
    print("Предупреждение: TextBlob не установлена. Установите: pip install textblob")
    TextBlob = None


class SentimentAnalyzer:
    """
    Класс для анализа тональности текста.
    """
    
    def __init__(self):
        """Инициализация словарей позитивных и негативных слов."""
        # Словари эмоциональных слов для русского языка
        self.positive_words = {
            'хорошо', 'отлично', 'прекрасно', 'великолепно', 'замечательно',
            'лучше', 'красиво', 'интересно', 'нравится', 'люблю', 'спасибо',
            'радость', 'счастье', 'удача', 'успех', 'победа', 'чудо',
            'волшебно', 'потрясающе', 'замечательно', 'восхитительно'
        }
        
        self.negative_words = {
            'плохо', 'ужасно', 'ужас', 'страшно', 'опасно', 'страх',
            'хуже', 'некрасиво', 'скучно', 'ненавижу', 'не нравится',
            'печаль', 'грусть', 'неудача', 'провал', 'беда', 'беде',
            'странно', 'отвратительно', 'мерзко', 'омерзительно'
        }
    
    def analyze_dictionary(self, text: str) -> Tuple[str, float]:
        """
        Анализ тональности словарным методом.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Кортеж (тональность, уверенность)
        """
        words = text.lower().split()
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        total = positive_count + negative_count
        
        if total == 0:
            return "нейтральная", 0.0
        
        if positive_count > negative_count:
            confidence = positive_count / total
            return "позитивная", confidence
        elif negative_count > positive_count:
            confidence = negative_count / total
            return "негативная", confidence
        else:
            return "нейтральная", 0.5
    
    def analyze_textblob(self, text: str) -> Tuple[str, float]:
        """
        Анализ тональности с использованием TextBlob.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Кортеж (тональность, полярность)
        """
        if TextBlob is None:
            return "недоступно", 0.0
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 (негативная) до 1 (позитивная)
            
            if polarity > 0.1:
                sentiment = "позитивная"
            elif polarity < -0.1:
                sentiment = "негативная"
            else:
                sentiment = "нейтральная"
            
            return sentiment, polarity
        except Exception as e:
            return "ошибка", 0.0
    
    def classify_sentiment(self, text: str) -> dict:
        """
        Комплексный анализ тональности.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Словарь с результатами анализа
        """
        dictionary_result, dictionary_conf = self.analyze_dictionary(text)
        textblob_result, textblob_conf = self.analyze_textblob(text)
        
        return {
            'text': text,
            'dictionary_method': {
                'sentiment': dictionary_result,
                'confidence': dictionary_conf
            },
            'textblob_method': {
                'sentiment': textblob_result,
                'polarity': textblob_conf
            }
        }


def main():
    """
    Демонстрация анализа тональности.
    """
    print("="*70)
    print("ПРИМЕР 4: АНАЛИЗ ТОНАЛЬНОСТИ ТЕКСТА")
    print("="*70)
    
    analyzer = SentimentAnalyzer()
    
    texts = [
        "Это был прекрасный и замечательный день! Я очень рад!",
        "Мне это не нравится. Это ужасно и страшно.",
        "Это просто текст без эмоций.",
        "Отлично! Восхитительно! Любимое блюдо!",
        "Ужас! Страшно! Не хочу больше видеть!"
    ]
    
    print("\n" + "-"*70)
    print("АНАЛИЗ ТОНАЛЬНОСТИ ТЕКСТОВ:")
    print("-"*70)
    
    for i, text in enumerate(texts, 1):
        result = analyzer.classify_sentiment(text)
        
        print(f"\nТекст {i}: {text}")
        print(f"  Словарный метод:")
        print(f"    - Тональность: {result['dictionary_method']['sentiment']}")
        print(f"    - Уверенность: {result['dictionary_method']['confidence']:.2f}")
        
        if result['textblob_method']['sentiment'] != 'недоступно':
            print(f"  TextBlob:")
            print(f"    - Тональность: {result['textblob_method']['sentiment']}")
            print(f"    - Полярность: {result['textblob_method']['polarity']:.2f}")
    
    print("\n" + "="*70)
    print("\nОбъяснение результатов:")
    print("- Тональность может быть: позитивная, негативная, нейтральная")
    print("- Уверенность/полярность показывает силу эмоции")
    print("- Диапазон: от -1 (максимально негативная) до 1 (максимально позитивная)")
    print("="*70)


if __name__ == "__main__":
    main()

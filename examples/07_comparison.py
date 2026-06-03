#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 7: Сравнение различных алгоритмов НЛП

Этот модуль выполняет сравнительный анализ различных алгоритмов:
- Производительность
- Точность
- Временные характеристики
"""

import time
import re
from typing import List, Dict
from collections import Counter
import math

try:
    import pymorphy2
    PYMORPHY_AVAILABLE = True
except ImportError:
    PYMORPHY_AVAILABLE = False


class AlgorithmComparison:
    """
    Класс для сравнения различных алгоритмов НЛП.
    """
    
    @staticmethod
    def simple_tokenize(text: str) -> List[str]:
        """Простая токенизация по пробелам."""
        return text.split()
    
    @staticmethod
    def regex_tokenize(text: str) -> List[str]:
        """Токенизация с использованием регулярных выражений."""
        return re.findall(r'\b\w+\b', text.lower())
    
    @staticmethod
    def measure_performance(func, text: str, iterations: int = 1000) -> Dict[str, float]:
        """
        Измерение производительности функции.
        
        Args:
            func: Функция для тестирования
            text: Текст для обработки
            iterations: Количество итераций
            
        Returns:
            Словарь с результатами
        """
        start_time = time.time()
        
        for _ in range(iterations):
            func(text)
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time = total_time / iterations
        
        return {
            'total_time': total_time,
            'average_time': avg_time,
            'operations_per_second': 1 / avg_time
        }
    
    @staticmethod
    def calculate_jaccard_similarity(text1: str, text2: str) -> float:
        """
        Расчет сходства Жаккара между двумя текстами.
        
        Args:
            text1: Первый текст
            text2: Второй текст
            
        Returns:
            Коэффициент Жаккара (0-1)
        """
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 and not words2:
            return 1.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        return intersection / union if union > 0 else 0
    
    @staticmethod
    def calculate_cosine_similarity(text1: str, text2: str) -> float:
        """
        Расчет косинусного сходства между двумя текстами.
        
        Args:
            text1: Первый текст
            text2: Второй текст
            
        Returns:
            Косинусное сходство (0-1)
        """
        words1 = re.findall(r'\b\w+\b', text1.lower())
        words2 = re.findall(r'\b\w+\b', text2.lower())
        
        counter1 = Counter(words1)
        counter2 = Counter(words2)
        
        # Все уникальные слова
        all_words = set(counter1.keys()) | set(counter2.keys())
        
        # Векторы
        vector1 = [counter1.get(word, 0) for word in all_words]
        vector2 = [counter2.get(word, 0) for word in all_words]
        
        # Скалярное произведение
        dot_product = sum(v1 * v2 for v1, v2 in zip(vector1, vector2))
        
        # Нормы
        norm1 = math.sqrt(sum(v ** 2 for v in vector1))
        norm2 = math.sqrt(sum(v ** 2 for v in vector2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


def main():
    """
    Демонстрация сравнения алгоритмов.
    """
    print("="*70)
    print("ПРИМЕР 7: СРАВНЕНИЕ РАЗЛИЧНЫХ АЛГОРИТМОВ НЛП")
    print("="*70)
    
    comparator = AlgorithmComparison()
    
    test_text = "Обработка естественного языка это область искусственного интеллекта которая занимается взаимодействием между компьютерами и человеческим языком"
    
    print("\n" + "-"*70)
    print("1. СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМОВ ТОКЕНИЗАЦИИ")
    print("-"*70)
    
    algorithms = {
        'Простая токенизация (split)': comparator.simple_tokenize,
        'Регулярные выражения': comparator.regex_tokenize
    }
    
    results = {}
    for name, func in algorithms.items():
        perf = comparator.measure_performance(func, test_text, iterations=10000)
        results[name] = perf
        print(f"\n{name}:")
        print(f"  Общее время (10000 итераций): {perf['total_time']:.4f} сек")
        print(f"  Среднее время на операцию: {perf['average_time']*1000:.4f} мс")
        print(f"  Операций в секунду: {perf['operations_per_second']:.0f}")
    
    print("\n" + "-"*70)
    print("2. СРАВНЕНИЕ МЕТОДОВ ИЗМЕРЕНИЯ СХОДСТВА ТЕКСТОВ")
    print("-"*70)
    
    texts_pairs = [
        ("Python это отличный язык программирования",
         "Python это хороший язык для разработки"),
        ("Машинное обучение это область искусственного интеллекта",
         "Компьютеры могут летать быстро"),
        ("НЛП обрабатывает естественный язык",
         "НЛП анализирует человеческий язык")
    ]
    
    for i, (text1, text2) in enumerate(texts_pairs, 1):
        print(f"\nПара текстов {i}:")
        print(f"  Текст 1: {text1[:40]}...")
        print(f"  Текст 2: {text2[:40]}...")
        
        jaccard = comparator.calculate_jaccard_similarity(text1, text2)
        cosine = comparator.calculate_cosine_similarity(text1, text2)
        
        print(f"  Сходство Жаккара: {jaccard:.4f}")
        print(f"  Косинусное сходство: {cosine:.4f}")
    
    print("\n" + "="*70)
    print("\nВЫВОДЫ:")
    print("1. Простая токенизация по пробелам обычно быстрее")
    print("2. Регулярные выражения более точны, но медленнее")
    print("3. Сходство Жаккара и косинусное сходство дают разные результаты")
    print("4. Выбор алгоритма зависит от требований приложения")
    print("="*70)


if __name__ == "__main__":
    main()

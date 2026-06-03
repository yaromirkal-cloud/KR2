#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Примечание 5: Извлечение именованных сущностей (NER)

Этот модуль демонстрирует различные методы извлечения сущностей:
- Простой паттерн-матчинг
- Регулярные выражения
- spaCy NER
"""

import re
from typing import List, Tuple

try:
    import spacy
except ImportError:
    spacy = None


class NamedEntityRecognizer:
    """
    Класс для извлечения именованных сущностей.
    """
    
    def __init__(self):
        """Инициализация данных для распознавания сущностей."""
        self.russian_cities = {
            'москва', 'санкт-петербург', 'казань', 'новосибирск',
            'екатеринбург', 'нижний новгород', 'тверь', 'рязань',
            'самара', 'краснодар', 'сочи', 'волгоград'
        }
        
        self.companies = {
            'яндекс', 'google', 'microsoft', 'apple', 'amazon',
            'facebook', 'twitter', 'alibaba', 'технопарк', 'сбер'
        }
    
    def extract_entities_regex(self, text: str) -> dict:
        """
        Извлечение сущностей с использованием регулярных выражений.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Словарь с найденными сущностями
        """
        entities = {
            'emails': [],
            'urls': [],
            'numbers': [],
            'dates': []
        }
        
        # Email адреса
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        entities['emails'] = emails
        
        # URL
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        entities['urls'] = urls
        
        # Числа
        numbers = re.findall(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', text)
        entities['numbers'] = numbers
        
        # Даты (простой паттерн DD.MM.YYYY)
        dates = re.findall(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', text)
        entities['dates'] = dates
        
        return entities
    
    def extract_entities_dictionary(self, text: str) -> dict:
        """
        Извлечение сущностей словарным методом.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Словарь с найденными сущностями
        """
        entities = {
            'cities': [],
            'companies': [],
            'organizations': []
        }
        
        text_lower = text.lower()
        words = text_lower.split()
        
        # Поиск городов
        for city in self.russian_cities:
            if city in text_lower:
                entities['cities'].append(city.title())
        
        # Поиск компаний
        for company in self.companies:
            if company in text_lower:
                entities['companies'].append(company.title())
        
        # Поиск организаций (слова заканчивающиеся на -ция, -ство)
        org_pattern = r'\b\w+(?:ция|ство)\b'
        organizations = re.findall(org_pattern, text, re.IGNORECASE)
        entities['organizations'] = organizations
        
        return entities
    
    def extract_entities_spacy(self, text: str) -> List[Tuple[str, str]]:
        """
        Извлечение сущностей с использованием spaCy.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Список кортежей (сущность, тип)
        """
        if spacy is None:
            return []
        
        try:
            nlp = spacy.load('ru_core_news_sm')
            doc = nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            return entities
        except OSError:
            print("Модель ru_core_news_sm не найдена")
            return []
    
    def extract_all_entities(self, text: str) -> dict:
        """
        Комплексное извлечение всех типов сущностей.
        
        Args:
            text: Текст для анализа
            
        Returns:
            Словарь со всеми найденными сущностями
        """
        return {
            'regex_entities': self.extract_entities_regex(text),
            'dictionary_entities': self.extract_entities_dictionary(text),
            'spacy_entities': self.extract_entities_spacy(text)
        }


def main():
    """
    Демонстрация извлечения именованных сущностей.
    """
    print("="*70)
    print("ПРИМЕР 5: ИЗВЛЕЧЕНИЕ ИМЕНОВАННЫХ СУЩНОСТЕЙ (NER)")
    print("="*70)
    
    recognizer = NamedEntityRecognizer()
    
    texts = [
        "Компания Google основана в Калифорнии. Напишите на support@google.com",
        "Яндекс - это крупная компания. Обновления на 15.03.2024",
        "В Москве и Санкт-Петербурге расположены офисы Microsoft и Apple",
        "Посетите наш сайт: https://example.com или https://www.company.ru"
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n" + "="*70)
        print(f"Текст {i}: {text}")
        print("="*70)
        
        # Регулярные выражения
        regex_ents = recognizer.extract_entities_regex(text)
        print("\nРегулярные выражения:")
        for key, values in regex_ents.items():
            if values:
                print(f"  {key}: {values}")
        
        # Словарный метод
        dict_ents = recognizer.extract_entities_dictionary(text)
        print("\nСловарный метод:")
        for key, values in dict_ents.items():
            if values:
                print(f"  {key}: {values}")
        
        # spaCy
        spacy_ents = recognizer.extract_entities_spacy(text)
        if spacy_ents:
            print("\nspaCy NER:")
            for entity, entity_type in spacy_ents:
                print(f"  {entity} ({entity_type})")
    
    print("\n" + "="*70)
    print("\nТипы сущностей (spaCy):")
    print("- PER: Люди")
    print("- ORG: Организации")
    print("- LOC: Места")
    print("- MISC: Прочее")
    print("="*70)


if __name__ == "__main__":
    main()

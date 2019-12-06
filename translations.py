import csv

with open('translations.csv', mode='r', encoding='utf-8') as csv_file:
    translations = list(csv.DictReader(csv_file))

def get_content(lang):
    lang = lang.lower()
    assert lang in translations[0]
    return [t[lang] for t in translations]
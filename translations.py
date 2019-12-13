import csv

with open('translations.csv', mode='r', encoding='utf-8') as csv_file:
    translations = list(csv.DictReader(csv_file))


def get_content(lang):
    lang = lang.lower()
    assert lang in translations[0]
    return [t[lang] for t in translations[:47]]


def get_dropdown_content(lang):
    lang = lang.lower()
    assert lang in translations[0]
    return [t[lang] for t in translations[47:49]]


def get_error_msg(lang):
    lang = lang.lower()
    assert lang in translations[0]
    return [t[lang] for t in translations[49:]]

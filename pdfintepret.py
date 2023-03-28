import fitz
from deep_translator import GoogleTranslator

def pdfintepret(text, lang):
    with open('/content/pdftranslate.txt', 'w') as f:
      f.write(text)
      f.close
      
    translated = GoogleTranslator(source='english', target=lang).translate_file('/content/pdftranslate.txt')
    return translated

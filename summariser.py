#Plain text parsers since we are parsing through text
from sumy.parsers.plaintext import PlaintextParser

#for tokenization
from sumy.nlp.tokenizers import Tokenizer

import nltk
nltk.download('punkt')

def summarise(file):
    # file = "/content/mydrive/MyDrive/Krypthon-codes/audio.txt" 
    parser = PlaintextParser.from_file(file, Tokenizer("english"))
    
    from sumy.summarizers.luhn import LuhnSummarizer
    summarizer_1 = LuhnSummarizer()
    summary_1 =summarizer_1(parser.document,2)
    
    return summary_1
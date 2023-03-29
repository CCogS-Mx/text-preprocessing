import nltk
import pickle
import re
import string
import spacy
import subprocess

import pandas as pd

from nltk.corpus import stopwords

from textblob import TextBlob

from bs4 import BeautifulSoup

import textblob.exceptions

subprocess.run(["python", "-m", "spacy", "download", "es_core_news_sm"])

nltk.download('stopwords')

class Preprocessing:
  def __init__(self, language):
    self.language = language
    if self.language == 'english':
      self.lang = 'en'
      self.nlp = spacy.load('en_core_web_sm')
    elif self.language == 'spanish':
      self.lang = 'es'
      self.nlp = spacy.load('es_core_news_sm')

  def stopwords_languaje(self):
    return stopwords.words(self.language)

  def lemmatizer(self, text):
    lemmas = []

    doc = self.nlp(text)

    for token in doc:
      lemmas.append(token.lemma_)
    
    return ' '.join(lemmas)


  def load_emoji_dict(self, path):
    with open(path, 'rb') as fp:
      emojis = pickle.load(fp)
    emojis = {v: k for k, v in emojis.items()}

    return emojis

  def remove_stopwords(self, text):
    stop_words = self.stopwords_languaje()
    clean_text = []
 
    for word in text.split():
      if word not in stop_words:
        clean_text.append(word)

    return ' '.join(clean_text)
  
  def tweet_preprocessing(self, text):
    clean_text = []
    for word in text.split(' '):
      word = '' if word.startswith('@') and len(word) > 1 else word
      word = '' if '@' in word else word
      word = '' if word.startswith('RT') and len(word) > 1  else word
      word = '' if word.startswith('http') else word
      word = '' if word.startswith('_USER_') and len(word) > 1 else word
      word = '' if word.startswith('_URL_') else word
      word = '' if word.startswith('_HASHTAG_') else word
      word = '' if word.startswith('rt') else word

      clean_text.append(word)

    return ' '.join(clean_text)

  def emoji_to_text(self, text, emoji_path):
    emojis = self.load_emoji_dict(emoji_path)
    clean_text = []

    for emot in emojis:
      text = re.sub(r'('+emot+')', 
            ' '.join(emojis[emot].replace(',', '').replace(':', '').split()), 
            text)
    
    tokens = text.split()

    for token in tokens:
      if token.count('_') > 0:
        token = token.split('_')
        token = ' '.join(token)
        token = self.translate(token)
      
      clean_text.append(token)

    final_text = ' '.join(clean_text)

    return final_text
  
  def normalize(slef, text):
    replacements = [
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ñ", "n")
    ]
  
    for original, replacement in replacements:
      text = text.replace(original, replacement)
    
    return text

  def split_hashtags(self, text):
    text = re.sub('#', '', text)
    return re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', text)

  def detect_http(self, text):
    return re.sub(r'(?<!http)(?=http)', ' ', text)

  def change_html_entities(self, text):
    return re.sub(r'<.*?>', '', text)

  def turn_lowercase(self, text):
    return text.lower()

  def remove_apostrophes(self, text):
    return re.sub("'", "", text)

  def remove_slaches(self, text):
    return re.sub("'\'", "", text)

  def remove_alphanumceric_words(self, text):
    return re.sub('\w*\d\w*', ' ', text)

  def remove_line_breaks(self, text):
    return ' '.join(text.splitlines())

  def remove_non_ascii(self, text):
    return re.sub(r'[^\x00-\x7fre]',r' ', text)
  
  def remove_blank_spaces(self, text):
    return ' '.join(text.split())

  def crop_repeated_characters(self, text):
    return re.sub(r'(.)\1+', r'\1\1', text)

  def remove_punctuation(self, text):
    return re.sub('[%s]' % re.escape(string.punctuation), ' ', text)

  def translate(self, text):
    try:
      w = TextBlob(text)
      w = w.translate(from_lang= 'en', to= 'es').raw
    except textblob.exceptions.TranslatorError:
      text = text
    except textblob.exceptions.NotTranslated:
      text = text
    else:
      text = w

    return text
  
  def preprocess_dataframe(self, data, column, tweet, remove_stop_words,
                          lemmatize, emoji_path):
    # Emoji to text
    text_emoji = lambda x: self.emoji_to_text(x, emoji_path)

    # Detect links
    detect_link = lambda x: self.detect_http(x)

    # Split hashtags
    split_hashtag = lambda x: self.split_hashtags(x)

    # Remove Tweeter entities
    remove_tweeter_entities = lambda x: self.tweet_preprocessing(x)

    # Change html entities
    html_entities = lambda x: self.change_html_entities(x)

    # Lower text
    lower_text = lambda x: self.turn_lowercase(x)

    # Remove punctuation
    remove_punct = lambda x: self.remove_punctuation(x)

    # Remove apostrophes
    remove_apostroph = lambda x: self.remove_apostrophes(x)

    # Remove inverted slashes
    remove_inv_slaches = lambda x: self.remove_slaches(x)

    # Remove alphanumeric words
    remove_alphanum_words = lambda x: self.remove_alphanumceric_words(x)

    # Remove non ASCII characters
    remove_non_asci = lambda x: self.remove_non_ascii(x)

    # Normalaize text
    normalize_text = lambda x: self.normalize(x)

    # Lemmatize text
    lemmas = lambda x: self.lemmatizer(x)

    # Remove line breaks
    remove_line_brk = lambda x: self.remove_line_breaks(x)

    # Remove blank spaces
    remove_spaces = lambda x: self.remove_blank_spaces(x)

    # Crop repeating characters
    crop_repeating_chars = lambda x: self.crop_repeated_characters(x)

    # Remove stopwords
    remove_stopword = lambda x: self.remove_stopwords(x)

    # traducir texto de emojis
    translate_emoji = lambda x: self.translate(x)

    # Apply functions
    data[column] = data[column].map(detect_link).map(html_entities).\
                                map(remove_line_brk)

    if tweet:
      data[column] = data[column].map(split_hashtag)
      data[column] = data[column].map(remove_tweeter_entities)
    

    if emoji_path != None:
      data[column] = data[column].map(text_emoji)

    data[column] = data[column].map(lower_text)

    if remove_stop_words == True:
      data[column] = data[column].map(remove_stopword)

    if lemmatize:
      data[column] = data[column].map(lemmas).map(normalize_text)
      if remove_stop_words == True:
        data[column] = data[column].map(remove_stopword)
    

    data[column] = data[column].map(normalize_text).\
                                map(remove_punct).\
                                map(crop_repeating_chars).\
                                map(remove_alphanum_words).\
                                map(remove_apostroph).\
                                map(remove_inv_slaches).\
                                map(remove_non_asci).\
                                map(remove_spaces)

    return data
  
  def preprocess_text(self, texts, tweet, remove_stop_words, 
                      lemmatize, emoji_path):

    clean_texts = []

    for text in texts:

      text = self.detect_http(text)

      text = self.change_html_entities(text)

      text = self.remove_line_breaks(text)

      if tweet:
        text = self.split_hashtags(text)

        text = self.tweet_preprocessing(text)
      

      if emoji_path != None:
        text = self.emoji_to_text(text, emoji_path)

      text = self.turn_lowercase(text)

      if remove_stop_words == True:
        text = self.remove_stopwords(text)

      if lemmatize:
        text = self.lemmatizer(text)
        text = self.normalize(text)
        if remove_stop_words:
          text = self.remove_stopwords(text)

      text = self.normalize(text)

      text = self.remove_punctuation(text)

      text = self.crop_repeated_characters(text)

      text = self.remove_alphanumceric_words(text)

      text = self.remove_apostrophes(text)

      text = self.remove_slaches(text)

      text = self.remove_non_ascii(text)

      text = self.remove_blank_spaces(text)

      clean_texts.append(text)

    return clean_texts

  def main_preprocess(self, data, column= None, tweet = False, 
                      remove_stop_words = False, is_dataframe= False, 
                      lemmatize = False, emoji_path = None):
    data_copy = data.copy()
    if is_dataframe == True:
      data = self.preprocess_dataframe(data_copy, column, tweet, 
                                       remove_stop_words, lemmatize, 
                                       emoji_path)
    
    else:
      data = self.preprocess_text(data_copy, tweet, 
                                  remove_stop_words, 
                                  lemmatize, emoji_path)
    
    return data
# Installing subprocess
import subprocess
subprocess.run(["python3", "-m", "pip", "install", 
                "nltk==3.8.1", "spacy==3.5.2",
                "emoji==2.2.0", "pandas==2.0.0",
                "bs4==0.0.1", "textblob==0.17.1"])

#default python dependencies
import pickle
import re
import string

#installed dependencies
import nltk
import spacy
import emoji
import pandas as pd
from bs4 import BeautifulSoup
from textblob import TextBlob

from nltk.corpus import stopwords
import textblob.exceptions

# Downloading the pipelines for spacy in english and spanish
subprocess.run(["python3", "-m", "spacy", "download", "es_core_news_sm"])
subprocess.run(["python3", "-m", "spacy", "download", "en_core_web_sm"])

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
  
  def tag_twitter_entities(self, text):
    clean_text = []

    for word in text.split(' '):

      word = '' if word.startswith('@') and len(word) > 1 else word
      word = '' if '@' in word else word
      word = '' if word.startswith('_USER_') else word

      word = 'RT' if word.startswith('rt') else word
      word = 'RT' if word.startswith('RT') else word

      word = 'URL' if word.startswith('http') else word
      word = 'URL' if word.startswith('_URL_') else word
      word = 'URL' if word == 'url' else word

      word = 'HASHTAG' if word.startswith('#') and len(word) >1 else word
      word = 'HASHTAG' if word.startswith('_HASHTAG_') else word

      clean_text.append(word)

    return ' '.join(clean_text)

  def emoji_to_text(self, text):
    clean_text = []
    for word in emoji.demojize(text, language=self.lang, delimiters= ("&&&&&", " ")).split(" "):
      if word.startswith("&&&&&"):
        word = re.sub("&&&&&", "", word)
        word = re.sub("_", " ", word)
      
      clean_text.append(word)
    
    return ' '.join(clean_text)
  
  def normalize(slef, text):
    replacements = [
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    ]
  
    for original, replacement in replacements:
      text = text.replace(original, replacement)
    
    return text

  def split_hashtags(self, text):
    clean_text = []
    for word in text.split(' '):
      if word.startswith('#'):
        word = re.sub('#', '', word)
        word = re.sub(r'(?<![A-Z\W])(?=[A-Z])', ' ', word)
      clean_text.append(word)
    return ' '.join(clean_text)

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

  def remove_non_ascii(self, text, whitelist):
    #return re.sub(r'[^\x00-\x7fre]',r' ', text)
    return ''.join([i if ord(i) < 128 or i in whitelist else ' ' for t in text for i in t])
  
  def remove_blank_spaces(self, text):
    return ' '.join(text.split())

  def crop_repeated_characters(self, text):
    return re.sub(r'(.)\1+', r'\1\1', text)

  def remove_punctuation(self, text, whitelist):
    punkt = ''

    for pun in string.punctuation:
      if pun not in whitelist:
        punkt += pun

    return re.sub('[%s]' % re.escape(punkt), ' ', text)

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
  
  def preprocess_dataframe(self, data, column, tweet, 
                           tweet_tags, remove_stop_words,
                           lemmatize, translate_emojis,
                           whitelist):
    # Emoji to text
    text_emoji = lambda x: self.emoji_to_text(x)

    # Detect links
    detect_link = lambda x: self.detect_http(x)

    # Split hashtags
    split_hashtag = lambda x: self.split_hashtags(x)

    # Remove Tweeter entities
    remove_tweeter_entities = lambda x: self.tweet_preprocessing(x)

    # Tag twitter entities
    tag_tweets = lambda x: self.tag_twitter_entities(x)

    # Change html entities
    html_entities = lambda x: self.change_html_entities(x)

    # Lower text
    lower_text = lambda x: self.turn_lowercase(x)

    # Remove punctuation
    remove_punct = lambda x: self.remove_punctuation(x, whitelist)

    # Remove apostrophes
    remove_apostroph = lambda x: self.remove_apostrophes(x)

    # Remove inverted slashes
    remove_inv_slaches = lambda x: self.remove_slaches(x)

    # Remove alphanumeric words
    remove_alphanum_words = lambda x: self.remove_alphanumceric_words(x)

    # Remove non ASCII characters
    remove_non_asci = lambda x: self.remove_non_ascii(x, whitelist)

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

    data[column] = data[column].map(lower_text)

    if tweet:
      if tweet_tags:
        data[column] = data[column].map(tag_tweets)
      else:
        data[column] = data[column].map(split_hashtag)
        data[column] = data[column].map(remove_tweeter_entities)

    if translate_emojis:
      data[column] = data[column].map(text_emoji)


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
  
  def preprocess_text(self, texts, tweet,
                      remove_stop_words, 
                      tweet_tags, lemmatize,
                      translate_emojis, 
                      whitelist):

    clean_texts = []

    for text in texts:

      text = self.detect_http(text)

      text = self.change_html_entities(text)

      text = self.remove_line_breaks(text)

      text = self.turn_lowercase(text)

      if tweet:
        if tweet_tags:
          text = self.tag_twitter_entities(text)
        else:
          text = self.split_hashtags(text)
          text = self.tweet_preprocessing(text)
      
      if translate_emojis:
        text = self.emoji_to_text(text)

      if remove_stop_words:
        text = self.remove_stopwords(text)

      if lemmatize:
        text = self.lemmatizer(text)
        text = self.normalize(text)
        if remove_stop_words:
          text = self.remove_stopwords(text)

      text = self.normalize(text)

      text = self.remove_punctuation(text, whitelist)

      text = self.crop_repeated_characters(text)

      text = self.remove_alphanumceric_words(text)

      text = self.remove_apostrophes(text)

      text = self.remove_slaches(text)

      text = self.remove_non_ascii(text, whitelist)

      text = self.remove_blank_spaces(text)

      clean_texts.append(text)

    return clean_texts

  def main_preprocess(self, data, column= None,
                      tweet = False,
                      tweet_tags = False,
                      remove_stop_words = False,
                      lemmatize = False,
                      translate_emojis = False,
                      whitelist = ""):
    
    data_type = type(data)

    if data_type == str:
      data = [data]
  
    data_copy = data.copy()

    if data_type == pd.core.frame.DataFrame:
      if column != None:
        data = self.preprocess_dataframe(data_copy,
                                         column,
                                         tweet, 
                                         tweet_tags,
                                         remove_stop_words,
                                         lemmatize,
                                         translate_emojis, 
                                         whitelist)
      else:

        print("ERROR: to preprocess string elements in a DataFrame Object\n'column' must have a string value to indicate the column where\texts are located")
    
    else:

      data = self.preprocess_text(data_copy, 
                                  tweet, 
                                  remove_stop_words,
                                  tweet_tags,
                                  lemmatize,
                                  translate_emojis,
                                  whitelist)

      if data_type == str:
        data = data[0]

    
    return data
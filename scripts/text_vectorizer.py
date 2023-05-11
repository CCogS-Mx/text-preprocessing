import subprocess
subprocess.run(["python3", "-m", "pip", "install", "scikit-learn==1.2.2"])
subprocess.run(["python3", "-m", "pip", "install", "gensim==4.3.1"])
subprocess.run(["python3", "-m", "pip", "install", "torch==2.0.0"])
subprocess.run(["python3", "-m", "pip", "install", "transformers==4.27.3"])

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import gensim.downloader
from gensim.models import Word2Vec, Doc2Vec, FastText
from gensim.models.doc2vec import TaggedDocument

import torch
from transformers import BertModel, BertTokenizer

class Vectorizer:
    r"""
    Parameters
    ----------
    data: mapping or iterable
        The data to fit the model
    method: {'bow', 'tfidf'}, default='tfidf'
        - If 'bow' a classic Bag of Words would be implemented to
          vectorize the text.
        - If 'tfidf' the TF-IDF method would be implemented to
          vectorize the text.

    ngram_range: tuple (min_n, max_n), default=(1, 1)
        The lower and upper boundary values for the n-grams to extract.

    max_df: float in range [0.0, 1.0] or int, default=1.0
        When building the vocabulary ignore terms that have a document
        frequency strictly higher than the given threshold. If float,
        the parameter represents a proportion, integer represents
        absolute values

    min_df: float in range [0.0, 1.0] or int, default=1
        When building the vocabulary ignore terms with document
        frequencies strictly below the given threshold. If float,
        the parameter represents a proportion, integer represents
        absolute values

    binary: bool, default=False
        If True, all the terms with frequency different from zero
        are set to 1.

    vocabulary: mapping or iterable, default=None
    """

    def __init__(self, data, method:str = 'tfidf', ngram_range:tuple = (1, 1),
                 max_df = 1.0, min_df = 1, binary:bool = False,
                 vocabulary = None):

        self.data = data
        self.method =  method
        self.ngram_range = ngram_range
        self.max_df = max_df
        self.min_df = min_df
        self.binary = binary
        self.vocabulary = vocabulary
        self.vectorizer = self.load_model()
        self.vectors_ = self.set_vocabulary_vectorize()
        self.vocabulary_ = self.vectorizer.vocabulary_

    def load_model(self):
        model_map = {
            'tfidf' : TfidfVectorizer,
            'bow' : CountVectorizer
        }
        vectorizer = model_map[self.method](ngram_range = self.ngram_range,
                                            max_df= self.max_df,
                                            min_df = self.min_df,
                                            binary = self.binary,
                                            vocabulary = self.vocabulary)
        return vectorizer
    
    def set_vocabulary_vectorize(self):
        return self.vectorizer.fit_transform(self.data)
    
    def vectorize(self, raw_documents):
        return self.vectorizer.transform(raw_documents)
    

class Embeddings:
    r"""
    Parameters
    ----------
    data: iterable of documents to train the model, default=None
        An iterable where all the documents are stored as strings

    model: {word2vec, doc2vec, fastext}, default='word2vec'
        The model you want to train. If the pretrained_vectors parameter
        not None, the default model to generate the embeddings will
        be the selected pretrained model.

    vector_size: int, default=300
        This parameter sets the size of the embedding vector for each term.

    window: int, default=7
        The maximum distance between a word and a predicted one (the context
        the model uses to predict the following word)

    seed: int, default=42
        Sets the random state to a static generation seed.

    min_df: int, dafault=1
        This sets an inferior boundary foer the term frequency. All the terms
        whose frequency is less than this wouldn't be taken into account
        to perform the model training.
    
    pretrained_vectors: {'fasttext-wiki-news-subwords-300', 'conceptnet-numberbatch-17-06-300',
        'word2vec-ruscorpora-300', 'word2vec-google-news-300',
        'glove-wiki-gigaword-50', 'glove-wiki-gigaword-100',
        'glove-wiki-gigaword-200', 'glove-wiki-gigaword-300',
        'glove-twitter-25', 'glove-twitter-50',
        'glove-twitter-100', 'glove-twitter-200',
        '__testing_word2vec-matrix-synopsis'}, default= None
        - If None, a new model will be trained to obtain the embeddings.
        - If not None, a pretrained model from the available ones will be used
          to generate the embedding vectors.
    """
    def __init__(
            self,
            data = None,
            model:str = 'word2vec',
            vector_size:int= 300,
            window = 7,
            seed = 42,
            min_df:int = 1,
            pretrained_vectors:str = None):

        self.data = data
        self.model = model
        self.min_df = min_df
        self.vector_size = vector_size
        self.window = window
        self.seed = seed
        if self.data != None:
            self.trained_model = self.train_model()
            self.training_sentences = self.generate_sentences()

        if pretrained_vectors != None:
            self.pretrained_vectors = self.load_pretrained_vectors(pretrained_vectors)
        else:
            self.pretrained_vectors = self.trained_model.wv

    def load_pretrained_vectors(self, pretrained):
        vectors = gensim.downloader.load(pretrained)
        return vectors
    
    def generate_sentences(self):
        sentences = []
        
        for doc in self.data:
            sentences.append(doc.split(' '))

        return sentences

    def generate_sentences_raw_documents(self, raw_documents):
        sentences = []
        for doc in raw_documents:
            sentences.append(doc.split(' '))

        return sentences
    
    
    def train_model(self):

        model_dict = {
            'word2vec' : Word2Vec,
            'doc2vec' : Doc2Vec,
            'fastext' : FastText
        }
        sentences = self.generate_sentences()

        documents = [TaggedDocument(doc, [i]) for i, doc in enumerate(self.data)]
        
        if self.model != 'doc2vec':
            trained_model = model_dict[self.model](sentences = sentences,
                                       vector_size = self.vector_size,
                                       window = self.window,
                                       min_count= self.min_df,
                                       seed = self.seed)
        else:
            trained_model = model_dict[self.model](documents = documents,
                                                   vector_size = self.vector_size,
                                                   window = self.window,
                                                   min_count = self.min_df)
        
        return trained_model

    def sent_embeddings_from_word_embeddings(self, embeddings):
        sentence_embeddings = []

        for embedding in embeddings:
            sent_embed = [0. for i in range(len(self.pretrained_vectors[0]))]
            for embed in embedding:
                sent_embed = list(map(sum, zip(sent_embed, embed)))

            sentence_embeddings.append(sent_embed)

        return sentence_embeddings

    def vectorize(self, raw_documents):
        sentences = self.generate_sentences_raw_documents(raw_documents)
        embeddings = []
        if self.model != 'doc2vec':
            for sent in sentences:
                word_embeddings = []
                for word in sent:
                    word_embeddings.append(self.pretrained_vectors[word] if word in self.pretrained_vectors else [0 for i in range(len(self.pretrained_vectors[0]))])

                embeddings.append(word_embeddings)
        
            sent_embeddings = self.sent_embeddings_from_word_embeddings(embeddings)
        else:
            for sent in sentences:
                embeddings.append(self.trained_model.infer_vector(sent))
            
            sent_embeddings = embeddings
        
        return sent_embeddings
    

class BertEmbeddings:
    r"""
    Parameters
    ----------
    pretrained_model: str, default='bert-base-uncased'
    """
    
    def __init__(
      self,
      pretrained_model:str = 'bert-base-uncased'
    ):
        self.model_name = pretrained_model
        self.model, self.tokenizer = self.load_model_tokenizer()
        self.vector_size = self.model.embeddings.word_embeddings.embedding_dim

    def load_model_tokenizer(self):
        model = BertModel.from_pretrained(self.model_name, output_hidden_states = True)
        tokenizer = BertTokenizer.from_pretrained(self.model_name)

        return model, tokenizer

    def model_text_preparation(self, text):
        marked_text = "[CLS] " + text + " [SEP]"
        tokenized_text = self.tokenizer.tokenize(marked_text)
        indexed_tokens = self.tokenizer.convert_tokens_to_ids(tokenized_text)
        segments_ids = [1] * len(indexed_tokens)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensor = torch.tensor([segments_ids])

        return tokens_tensor, segments_tensor
    
    def get_model_embeddings(self, text):

        tokens_tensor, segments_tensor = self.model_text_preparation(text)
        with torch.no_grad():
            outputs = self.model(tokens_tensor, segments_tensor)
            hidden_states = outputs[2][1:]

        token_embeddings = hidden_states[-1]
        token_embeddings = torch.squeeze(token_embeddings, dim = 0)
        list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]

        return list_token_embeddings
    
    def sent_embeddings_from_word_embeddings(self, embeddings):
        sentence_embeddings = []

        for embedding in embeddings:
            sent_embed = [0. for i in range(len(embeddings[0][0]))]
            for embed in embedding:
                sent_embed = list(map(sum, zip(sent_embed, embed)))

            sentence_embeddings.append(sent_embed)

        return sentence_embeddings

 
    def vectorize(self, raw_documents):
        embeddings = []

        for doc in raw_documents:
            if len(doc.split(' ')) > self.vector_size:
                doc = doc[:self.vector_size]
            embeddings.append(self.get_model_embeddings(doc))
        
        sent_embeddings = self.sent_embeddings_from_word_embeddings(embeddings)


        return sent_embeddings
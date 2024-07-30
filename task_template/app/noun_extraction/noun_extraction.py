import stanza
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import pathlib
import nltk
from nltk.corpus import wordnet as wn

class NounNormalizer:
    def __init__(self):
        nltk_data_dir = './nltk_data'
        pathlib.Path(nltk_data_dir).mkdir(parents=True, exist_ok=True)  # 创建 NLTK 数据目录
        nltk.data.path.append(nltk_data_dir)  # 将 NLTK 数据目录添加到路径中
        nltk.download('wordnet', download_dir=nltk_data_dir)  # 下载 WordNet 数据包到指定目录
    
    
    def singularize_and_lowercase(self, word):
        singular_word = wn.morphy(word, wn.NOUN)
        if singular_word is None:
            singular_word = word
        return singular_word.lower()

class GetNoun(object):
    def __init__(self):
        resource_dir = './stanza_resources'
        hf_cache_dir = './hf_cache'
        
        pathlib.Path(resource_dir).mkdir(parents=True, exist_ok=True)
        pathlib.Path(hf_cache_dir).mkdir(parents=True, exist_ok=True)
        
        os.environ['HF_HOME'] = hf_cache_dir

        self.nounsP = stanza.Pipeline(lang='en', processors='tokenize,pos', dir=resource_dir)
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', cache_dir=hf_cache_dir)
        self.model = BertModel.from_pretrained('bert-base-uncased', cache_dir=hf_cache_dir)
        self.nounNormalizer = NounNormalizer()

    def extractNouns(self, sentenceList):
        sentence_entities = dict()
        for sentence in sentenceList:
            doc = self.nounsP(sentence)
            nouns = []
            for sent in doc.sentences:
                for word in sent.words:
                    if word.pos.startswith('N') or word.xpos == 'NNP':  # Checks if the POS tag is for a noun
                        nouns.append(word.text)
            sentence_entities[sentence] = nouns
        return sentence_entities
    
    def get_entity_embedding(self, entity):
        inputs = self.tokenizer(entity, return_tensors='pt', truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)
    
    def getSimilarity(self, topic_word, sentenceList):
        extracted_nouns = self.extractNouns(sentenceList)
        wordList = [word for sublist in extracted_nouns.values() for word in sublist]
        wordList = list(set([self.nounNormalizer.singularize_and_lowercase(word) for word in wordList]))
        word_similarity = dict()
        topic_embedding = self.get_entity_embedding(topic_word)
        
        for word in wordList:
            word_embedding = self.get_entity_embedding(word)
            similarity = cosine_similarity(topic_embedding, word_embedding)
            word_similarity[word] = similarity[0][0]
        
        # Sort words by similarity score in descending order
        sorted_word_similarity = dict(sorted(word_similarity.items(), key=lambda item: item[1], reverse=True))
        
        return sorted_word_similarity
        

noun = GetNoun()
theme = 'summer'
sentence_entities_nouns = noun.getSimilarity(theme, ['spring is a good weather', 'I like dog', 'There\'s a bunch of white dogs'])
print(sentence_entities_nouns)

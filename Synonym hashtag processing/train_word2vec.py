# train_word2vec.py - Train word2vec
# Copyright (c) 2020-2025 TIAN

from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences = word2vec.Text8Corpus('.\\Data in the analysis process\\Word vector training corpus.txt')
model=word2vec.Word2Vec(sentences,size=128,iter=5,workers=3,min_count=1)
model.save('word2vecAll.model')
print(model.similarity('javascript','js'))


# save model
model.wv.save_word2vec_format('.\\Data in the analysis process\\word2vecAll.vector')
model.save('.\\Data in the analysis process\\word2vecAll.model')
print(model["java"])
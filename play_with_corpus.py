# encoding=utf8
__author__ = 'Paul_Song'

import logging, play_crawler.documents as doc, gensim
from gensim import corpora, models, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documents = [doc._360camera_, doc._360security_, doc._dbs_, doc._djfree_, doc._etsy_, doc._facebook_, doc._gokeyboard_,
             doc._lazyswipe_, doc._mangoplayer_, doc._whatsapp_, doc._wechat_, doc._viber_, doc._tango_, doc._grabtaxi_,
             doc._qoo10_, doc._skype_]

stoplist = set('a or is for of the and to in'.split())

texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
         for text in texts]

# step 1: create dictionary
dictionary = corpora.Dictionary(texts)
dictionary.save('tmp/description.dict')

# step 2: grab the corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('tmp/playAppCorpus.mm', corpus)

lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, update_every=1, chunksize=100,
                                      passes=1)

lda.print_topics(10)


class Corpus(object):
	def __iter__(self):
		'''the way we deal with the input data'''
		yield dictionary.doc2bow(None)




import gensim.downloader

print(list(gensim.downloader.info()['models'].keys()))

model = gensim.downloader.load('word2vec-google-news-300')
import _pickle as pickle

f = open('quotes.pickle', 'rb')
info = pickle.load(f)
print(info)

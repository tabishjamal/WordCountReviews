import gensim
from gensim import corpora
from pprint import pprint
from gensim.utils import simple_preprocess
from smart_open import smart_open
import os

#  Create dictionary from list of sentences

documents_1 = ["The Saudis are preparing a report that will acknowledge that",
             "Saudi journalist Jamal Khashoggi's death was the result of an",
             "interrogation that went wrong, one that was intended to lead",
             "to his abduction from Turkey, according to two sources."]

documents_2 = ["One source says the report will likely conclude that",
                "the operation was carried out without clearance and",
                "transparency and that those involved will be held",
                "responsible. One of the sources acknowledged that the",
                "report is still being prepared and cautioned that",
                "things could change."]
print('documents_1:',documents_1)
print(type(documents_1))

# Tokenize
texts_1=[[text for text in doc.split()] for doc in documents_1]
#print(texts)

# Create dictionary
dictionary=corpora.Dictionary(texts_1)
print(dictionary)

# Show word mapped to ID
#entries=[dict_entries for dict_entries in dictionary.items()]
#print(entries)
print(dictionary.token2id)

## Updating dictionary values with new entries
text_2=[[text for text in docs.split()] for docs in documents_2]
dictionary.add_documents(text_2)
print(dictionary)
print(dictionary.token2id)


########  --  Create a dictionary from one or more text files  --  ########

dictionary_1=corpora.Dictionary(simple_preprocess(line, deacc=True) for line in open('C:\\Users\\tabis\\PycharmProjects\\sentiAnalysisGensim\\reviews.txt',encoding='utf-8'))
print(dictionary_1.token2id)
print(dictionary_1)

######## -- Create Bag of Words -- ########
print('\n\n\nCreating bag of words')
tokenized_list=[ simple_preprocess(line) for line in open('C:\\Users\\tabis\\PycharmProjects\\sentiAnalysisGensim\\reviews.txt',encoding='utf-8')]
print('tokenized_list::',tokenized_list)

# Creating dictionary
my_dictionary=corpora.Dictionary()
my_corpus=[my_dictionary.doc2bow(line, allow_update=True) for line in tokenized_list]
print('my_corpus::',my_corpus)
#word_counts = [[(mydict[id], count) for id, count in line] for line in my_corpus]
#pprint(word_counts)

print(documents_1)
tokens=[simple_preprocess(docs) for docs in documents_1]
my_dict=corpora.Dictionary()
my_corpora=[my_dict.doc2bow(doc, allow_update=True)for doc in tokens]
pprint(my_corpora)
word_counts=[ [(my_dict[id],count)for id, count in line]for line in my_corpora]
pprint(word_counts)
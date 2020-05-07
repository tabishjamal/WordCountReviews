from gensim.utils import simple_preprocess
from gensim import corpora
from smart_open import smart_open
import nltk
from nltk import Cistem
import csv
from pprint import pprint
import time
nltk.download('stopwords')  # run once
from nltk.corpus import stopwords
from collections import OrderedDict

stop_words = stopwords.words('german')
print('Start...')


def my_file_writer(filename_write, data_write):
    with open(filename_write, 'w', encoding='utf-8') as f:
        print(data_write, file=f)
    f.close()


def list_to_dict(convert_list):
    converted_dict = {}
    for sub_list in convert_list:
        for sub_sub_list in sub_list:
            key, value = sub_sub_list[0], sub_sub_list[1]
            converted_dict[key] = value
    return converted_dict


def sort_dict(token_count_dict):
    sorted_map = {}
    for var in sorted(token_count_dict, key=token_count_dict.get, reverse=True):
        sorted_map.update({var: token_count_dict[var]})
    return sorted_map


def fetch_tokens(filename_read, combine_reviews_flag, rev_category):
    print('File Read: ', filename_read)
    print('combine_reviews_flag: ', combine_reviews_flag)
    token_list_return = []
    with open(filename_read, encoding='utf-8') as kununu_file:
        csv_data_raw = csv.reader(kununu_file, delimiter='|')
        row_count = 0
        reviews_combined = ''
        for row in csv_data_raw:
            if row_count == 0:
                print(f'Column names are {", ".join(row)}')  # Formatted print statement which includes all the rows
                row_count += 1
            else:
                # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                row_count += 1
                if combine_reviews_flag == True:
                    if rev_category == 'all':
                        reviews_combined = reviews_combined + ' ' + row[9]
                    else:
                        if rev_category == row[7]:
                            reviews_combined = reviews_combined + ' ' + row[9]
                else:
                    if rev_category == 'all':
                        token_list_return.append(simple_preprocess(row[9]))
                    else:
                        if rev_category == row[7]:
                            token_list_return.append(simple_preprocess(row[9]))
#                if row_count > 3:
#                    break
        if combine_reviews_flag == True:
            token_list_return.append(simple_preprocess(reviews_combined))
    print('Total Data Lines Read ::', row_count - 1)  # Subtracted 1 because file has Header row as well
    return token_list_return


def stopword_removal(in_token_list, stem_flag):
    print('stem_flag: ', stem_flag)
    stemmer = Cistem()
    sw_removed_list = []
    sw_removed_list_stemmed = []
    for list in in_token_list:
        sw_removed_inner = []
        sw_removed_inner_stemmed = []
        for word in list:
            if word not in stop_words:
                sw_removed_inner.append(word)
                if stem_flag == True:
                    sw_removed_inner_stemmed.append(stemmer.stem(word))
        sw_removed_list.append(sw_removed_inner)
        sw_removed_list_stemmed.append(sw_removed_inner_stemmed)
    return sw_removed_list, sw_removed_list_stemmed


filename = 'C:\\Users\\tabis\\PycharmProjects\\sentiAnalysisGensim\\Master_Data_Milestone1.csv'
review_category = 'all'
token_list = fetch_tokens(filename, True, review_category)
#print('token_list: ', token_list)

final_tokens, final_tokens_stemmed = stopword_removal(token_list, True)
#print('final_tokens: ', final_tokens)
#print('final_tokens_stemmed: ', final_tokens_stemmed)

# Make dictionary
my_dict = corpora.Dictionary()
my_dict_stemmed = corpora.Dictionary()
# Create bag of words from dictionary
my_bagOW = [my_dict.doc2bow(words, allow_update=True) for words in final_tokens]
my_bagOW_stemmed = [my_dict_stemmed.doc2bow(words, allow_update=True) for words in final_tokens_stemmed]

print('tokens with count:\n')
# pprint(my_bagOW)
# pprint(my_dict.token2id)
print('sleeping for 0.5 sec---------------------------------')
time.sleep(0.5)
# Count no of word occouring in a review
word_with_counts = [[(my_dict[id], count) for id, count in line] for line in my_bagOW]
# pprint(word_with_counts)
total_tokens = [len(word) for word in word_with_counts]
my_file_writer('wordcount_perReview.txt', word_with_counts)

word_with_counts_stemmed = [[(my_dict_stemmed[id], count) for id, count in line] for line in my_bagOW_stemmed]
# pprint(word_with_counts_stemmed)
total_tokens_stemmed = [len(word) for word in word_with_counts_stemmed]
my_file_writer('wordcount_perReview_stemmed.txt', word_with_counts_stemmed)

print('total_tokens: ', total_tokens)
print('total_tokens_stemmed: ', total_tokens_stemmed)

#### ---------- Sorting by decreasing occourance
print('\nNow Sorting...')
dict_with_count = list_to_dict(word_with_counts)
sorted_dict = sort_dict(dict_with_count)
#print('sorted_dict: ', sorted_dict)

dict_with_count_stemmed = list_to_dict(word_with_counts_stemmed)
sorted_dict_stemmed = sort_dict(dict_with_count_stemmed)
#print('sorted_dict_stemmed: ', sorted_dict_stemmed)

#### ---- Writing in file
my_file_writer('sorted_words_count.csv', sorted_dict)
my_file_writer('sorted_words_count_stemmed.csv', sorted_dict_stemmed)

import csv
from gensim.utils import simple_preprocess
from nltk import Cistem
import time

stemmer=Cistem()
print('Hello')
collected_words = []
words_file='C:\\Users\\tabis\\PycharmProjects\\sentiAnalysisGensim\\selected_words.txt'
with open('selected_words.txt','r',encoding='utf-8') as selected_file:
    for line in selected_file:
        collected_words.append(stemmer.stem(line.strip()))
print('collected_words: ', collected_words)


def get_review_file(filename_read, rev_category):
    with open(filename_read, encoding='utf-8') as kununu_file:
        csv_data_raw = csv.reader(kununu_file, delimiter='|')
        row_count = 0
        created_file = 'filtered_file_'+rev_category+'.csv'
        for row in csv_data_raw:
            if row_count == 0:
                with open(created_file, 'w', encoding='utf-8')as header_writer:
                    print(f'{"| ".join(row)}', file=header_writer)
                header_writer.close()
                print(f'{"| ".join(row)}')  # Formatted print statement which includes all the rows
                row_count += 1
            else:
                '''if row_count > 35:
                    break'''
                if rev_category == 'all':
                    row_list=[]
                    fetch_list=simple_preprocess(row[9])
                    for word in fetch_list:
                        row_list.append(stemmer.stem(word))
                    if len([value for value in row_list if value in collected_words]) != 0:
                        with open(created_file, 'a', encoding='utf-8') as file_writer:
                            print(f'{"| ".join(row)}', file=file_writer)
                        file_writer.close()
                    #token_list_return.append(simple_preprocess(row[9]))
                else:
                    if rev_category == row[7]:
                        row_list=simple_preprocess(row[9])
                        if len([value for value in row_list if value in collected_words]) != 0:
                            with open(created_file, 'a', encoding='utf-8') as file_writer:
                                print(f'{"| ".join(row)}', file=file_writer)
                            file_writer.close()
                row_count += 1
        print('Total Data Lines Read ::', row_count - 1)  # Subtracted 1 because file has Header row as well


file_read='C:\\Users\\tabis\\PycharmProjects\\sentiAnalysisGensim\\Master_Data_Milestone1.csv'
review_category='Arbeitsatmosphäre'
get_review_file(file_read, review_category)
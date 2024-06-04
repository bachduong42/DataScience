import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
cleandata = pd.read_csv('../cleandata/cleandata.csv')
cleandatalecturer = pd.read_csv('../cleandata/CleanDataLecturer.csv')

normdata = cleandata.copy()
normdatalecturer = cleandatalecturer.copy()

# chuẩn hóa văn bản về chữ thường
normdata = normdata.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)
normdatalecturer = normdatalecturer.apply(lambda x: x.str.lower() if x.dtype == 'object' else x)

# loại bỏ các kí tự không cần thiết
def process_tweet(tweet):
    words = tweet.split()
    processed_words = []
    for word in words:
        if '.' in word and all(char.isdigit() or char == '.' for char in word):
            processed_words.append(word)
        elif ',' in word and all(char.isdigit() or char == ',' for char in word):
            processed_words.append(word)
        else:
            processed_word = re.sub(r'[^\w\s]', ' ', word)
            processed_words.extend(processed_word.split())

    # Tách các từ sau khi xử lý để đảm bảo chúng không bị nối với nhau
    processed_tweet = ' '.join(processed_words)
    processed_tweet = re.sub(r'\s+', ' ', processed_tweet)  # Loại bỏ khoảng trắng dư thừa
    return processed_tweet.strip()  # Loại bỏ khoảng trắng dư thừa ở đầu và cuối chuỗi


# cleandata.csv
normdata['Course_Title'] = normdata['Course_Title'].str.replace(",", ", ")
normdata['Description'] = normdata['Description'].str.replace(",", ", ")
normdata['Course_Content'] = normdata['Course_Content'].str.replace(",", ", ")

normdata['Course_Title'] = normdata['Course_Title'].apply(process_tweet)
normdata['Description'] = normdata['Description'].apply(process_tweet)
normdata['Course_Content'] = normdata['Course_Content'].apply(process_tweet)


# cleandatalecturer.csv
normdatalecturer['Job_Title'] = normdatalecturer['Job_Title'].str.replace(",", ", ")
normdatalecturer['Job_Title'] = normdatalecturer['Job_Title'].apply(process_tweet)

# loại bỏ từ dừng

stop_words = set(stopwords.words('english')) # Khởi tạo danh sách từ dừng

columns_to_process = ['Course_Title', 'Description', 'Course_Content'] # Danh sách các cột bạn muốn loại bỏ từ dừng
for column in columns_to_process:
    normdata[column] = normdata[column].apply(lambda text: ' '.join(
        term for term in text.split() if term not in stop_words))

columns_to_process_lecturer = ['Job_Title']
for column in columns_to_process_lecturer:
    normdatalecturer[column] = normdatalecturer[column].apply(lambda text: ' '.join(
        term for term in text.split() if term not in stop_words))




# đưa các tè về dạng từ gốc
ps = PorterStemmer()
columns_to_stem = ['Course_Title', 'Description', 'Course_Content']

for column in columns_to_stem:
    normdata[column] = normdata[column].apply(lambda text: ' '.join(
        ps.stem(term) for term in text.split()))

columns_to_stem = ['Job_Title']
for column in columns_to_stem:
    normdatalecturer[column] = normdatalecturer[column].apply(lambda text: ' '.join(
        ps.stem(term) for term in text.split()))

stop_words_by_tfidf_score = set(['learn', 'use', 'understand', 'cours'])
for column in columns_to_process:
    normdata[column] = normdata[column].apply(lambda text: ' '.join(
        term for term in text.split() if term not in stop_words_by_tfidf_score))

normdata.to_csv('normdata.csv', index=False)
normdatalecturer.to_csv('normdatalecturer.csv', index=False)
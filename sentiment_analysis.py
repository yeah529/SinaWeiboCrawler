# -*- coding: utf-8 -*-
import csv
import sys
import io
import math


def sentence_split(text_set):
    sentence = []
    for each_set in text_set:
        temp =[]
        for tk in each_set:
            if tk not in stopwords:#delete stopwords
                temp.append(re.sub(u'[0123456789O！，“”#￥、’（）+——。：；《》？【】……——!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]','',tk[0]))
                if u'' in temp:
                    temp.remove(u'')
        sentence.append(temp)
    return sentence

def classifier(token_set):
    result = [] #format is [each_weibo, sentiment, positive prob, negative prob]
    
    for each_set in token_set:
        p_prob = [positive] 
        n_prob = [negative]
        for each_word in each_set:
            if each_word in word_count.keys():
                p_prob.append(float(word_count[each_word][0]+1)/(p_word_count+all_vocabulary))
                n_prob.append(float(word_count[each_word][1]+1)/(n_word_count+all_vocabulary))
            else:
                p_prob.append(1.0/(p_word_count+all_vocabulary))
                n_prob.append(1.0/(n_word_count+all_vocabulary))
        
        p_final_prob = math.exp(sum(map(math.log,p_prob)))
        n_final_prob = math.exp(sum(map(math.log,n_prob)))
        
        if p_final_prob > n_final_prob:
            sentiment = 'positive'
        elif p_final_prob < n_final_prob:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        result.append(["".join(each_set), sentiment, p_final_prob, n_final_prob])
    
    return result




##Load training set to train the Naive Bayes algorithm 

input_file = io.open('train_set.txt', 'r',encoding='utf-16')
stop_file = io.open('cn_stopwords.txt', 'r',encoding='utf-8')
stopwords = set([re.sub("\n","",word) for word in stop_file])

training_set = []
for row in input_file:
    each_row = row.split("\t")
    training_set.append([each_row[0],re.sub("\n","",each_row[1].encode('utf-8'))])
    
    input_file.close()
stop_file.close()

allset = [jieba.tokenize(i[0].replace(" ","")) for i in training_set]
sentence_token = sentence_split(allset)
unique_words = set([each_word for each_sentence in sentence_token for each_word in each_sentence])
token_set = [[sentence_token[n],training_set[n][1]] for n in range(len(sentence_token))]

word_count = {}
for each_uni_word in unique_words:
    word_count[each_uni_word] = [0,0,0] #format is {word : [pos_count,neg_count,whole_count]}

for each_sentence in token_set:
    for each_word in each_sentence[0]:
        word_count[each_word][2] += 1
        if each_sentence[1] == 'n':
            word_count[each_word][1] += 1
        else:
            word_count[each_word][0] += 1    
            
p_word_count = sum([pos_count[0] for pos_count in word_count.values()])
n_word_count = sum([neg_count[1] for neg_count in word_count.values()])
all_vocabulary = len(unique_words)

#initiate positive and negative probability from training set
positive = 0.5
negative = 0.5

#Load testing set to test
#In my own script, I usually connect to my databse and load test set into "main_content".
#You could replace "main_content" to your own test set.

test_set = [jieba.tokenize(i.decode('UTF-8').replace(" ","")) for i in main_content]
test_token = sentence_split(test_set)

test = classifier(test_token)

#simply output result to see the sentiment for each weibo
for i in test:
    print(i[0])
    print(i[1])
    print('--------')

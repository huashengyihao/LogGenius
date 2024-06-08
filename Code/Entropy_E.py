import csv
import re
import math
import nltk
from collections import Counter
import pandas as pd

 
def log_entropy_E(sentences,threshold,dataset,filter):

    sentences = get_united_sentences(sentences,dataset,filter)


    template_df = pd.read_csv('../log_after_group/'+ dataset +'_template.csv', usecols=['模板', '句子标号'], encoding='GBK')
    templates = template_df['模板'].dropna()
    templates = templates.tolist()

    csv.field_size_limit(10 * 1024 * 1024)

    with open('../log_after_group/'+ dataset +'_template.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sentence_numbers = [row['句子标号'].strip('"').split(',') for row in reader]

    template_indices = get_low_entropy_template(templates, sentences, sentence_numbers, threshold)

    sentence_indices = []

    for indice in template_indices:
        sentence_indices.append(sentence_numbers[indice][0])

    with open('../log_after_entropy/'+ dataset +'_expanded_indices_thre_'+str(threshold)+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['待扩充句子'])

        writer.writerow(sentence_indices)

 
def get_low_entropy_template(templates,sentences,sentence_numbers,threshold):
    template_indices = []
    cnt = 0

    for i in range(len(sentence_numbers)):
        template = templates[i]

        if is_english_sentence(template):
            print(templates[i])
            if 'user'not in template:
                words = template.split()

                all_words_have_meaning = all(has_meaning(word) for word in words)

                if all_words_have_meaning:
                    continue


        if len(sentence_numbers[i]) == 1:
            template_indices.append(i)

        elif '*' not in templates[i]:
            template_indices.append(i)

        else:
            indices = [int(idx) for idx in sentence_numbers[i]]
            sentence_list = [sentences[idx] for idx in indices]
            entropy = get_sentences_entropy(template, sentence_list)

            if entropy <= threshold:
                template_indices.append(i)

    return template_indices


  
def get_united_sentences(sentences,dataset,filter):
    replaced_sentences = []

    for s in sentences:

        for rgex in filter:
            s = re.sub(rgex, '<*>', s)

        if dataset=='HealthApp':
            s = re.sub(':', ': ', s)
            s = re.sub('=', '= ', s)
            s = re.sub('\|', '| ', s)
        if dataset=='Android':
            s = re.sub('\(', '( ', s)
            s = re.sub('\)', ') ', s)
        if dataset=='Android':
            s = re.sub(':', ': ', s)
            s = re.sub('=', '= ', s)
        if dataset=='HPC':
            s = re.sub('=', '= ', s)
            s = re.sub('-', '- ', s)
            s = re.sub(':', ': ', s)
        if dataset == 'BGL':
                s = re.sub('=', '= ', s)
                s = re.sub('\.\.', '.. ', s)
                s = re.sub('\(', '( ', s)
                s = re.sub('\)', ') ', s)
        if dataset == 'Hadoop':
                s = re.sub('_', '_ ', s)
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
                s = re.sub('\(', '( ', s)
                s = re.sub('\)', ') ', s)
        if dataset == 'HDFS':
                s = re.sub(':', ': ', s)
        if dataset == 'Linux':
            s = re.sub('=', '= ', s)
            s = re.sub(':', ': ', s)
        if dataset == 'Spark':
            s = re.sub(':', ': ', s)
        if dataset == 'Thunderbird':
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
        if dataset == 'Windows':
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)
                s = re.sub('\[', '[ ', s)
                s = re.sub(']', '] ', s)
        if dataset == 'Zookeeper':
                s = re.sub(':', ': ', s)
                s = re.sub('=', '= ', s)

        s = re.sub(',', ', ', s)

        replaced_sentences.append(s)

    return replaced_sentences

 
def get_sentences_entropy(template,sentences):

    no_need_indices = []

    new_sentences = [split_sentence(s) for s in sentences]

    max_length = len(max(new_sentences, key=len))

    for i in range(len(new_sentences)):
        new_sentences[i] += ['%'] * (max_length - len(new_sentences[i]))

    new_lists = [[sentence[i] for sentence in new_sentences] for i in range(max_length) if i not in no_need_indices]

    entropies = [calculate_entropy(sentence) for sentence in new_lists]

    average_entropy = sum(entropies) / len(entropies)

    return average_entropy

def split_sentence(s):
    s = re.sub(' +', ' ', s).split(' ')
    return s

 
def calculate_entropy(sentence_list):
    total_count = len(sentence_list)
    counter = Counter(sentence_list)
    entropy = 0.0
    for count in counter.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)
    return entropy


 
def is_english_sentence(sentence):
    pattern = r'^[A-Za-z\s]+$'
    return re.match(pattern, sentence) is not None

 
def has_meaning(word):
    dictionary = set(nltk.corpus.words.words())
    if word.lower() in dictionary:
        return True

    if word.islower() or word.isupper():
        return False

    word_parts = []
    current_part = ""
    for char in word:
        if char.isupper():
            if current_part:
                word_parts.append(current_part)
            current_part = char
        else:
            current_part += char
    word_parts.append(current_part)

    for part in word_parts:
        if part.lower() in dictionary:
            return True

    return False
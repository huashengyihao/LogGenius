import csv
import re
import math
from collections import Counter
import jieba
import pandas as pd
import datetime
 
def log_entropy_C(sentences,threshold,dataset):

    sentences = get_united_sentences(sentences)


    template_df = pd.read_csv('../log_after_group/'+dataset+'_template.csv', usecols=['模板', '句子标号'], encoding='GBK')
    templates = template_df['模板'].dropna()
    templates = templates.tolist()

    csv.field_size_limit(10 * 1024 * 1024)

    with open('../log_after_group/'+dataset+'_template.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sentence_numbers = [row['句子标号'].strip('"').split(',') for row in reader]

    template_indices = get_low_entropy_template(templates, sentences, sentence_numbers, threshold)

    sentence_indices = []

    for indice in template_indices:
        sentence_indices.append(sentence_numbers[indice][0])


    with open('../log_after_entropy/'+dataset+'_expanded_indices_thre_'+str(threshold)+'.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['待扩充句子'])

        writer.writerow(sentence_indices)


def get_low_entropy_template(templates,sentences,sentence_numbers,theshold):
    template_indices = []
    cnt = 0

    for i in range(len(sentence_numbers)):

        template = templates[i]

        if "test" in template:
            continue

        temp_template = template.replace('*', '')
        pattern = re.compile(r'[a-zA-Z0-9]+')
        if not pattern.search(temp_template):
            cnt += 1
            continue

        if len(sentence_numbers[i]) == 1:
            template_indices.append(i)

        elif '*' not in templates[i]:
            template_indices.append(i)

        else:
            indices = [int(idx) for idx in sentence_numbers[i]]
            sentence_list = [sentences[idx] for idx in indices]
            entropy = get_sentences_entropy(template, sentence_list)

            if entropy <= theshold:
                template_indices.append(i)

    return template_indices



def get_united_sentences(sentences):
    pattern_comma = r','
    repl_comma = '，'
    pattern_left_bracket = r'[（({｛【[]'
    repl_left_bracket = '<'
    pattern_right_bracket = r'[）)}｝】\]]'
    repl_right_bracket = '>'
    replaced_sentences = []
    for sentence in sentences:
        sentence = re.sub(pattern_comma, repl_comma, sentence)
        sentence = re.sub(pattern_left_bracket, repl_left_bracket, sentence)
        sentence = re.sub(pattern_right_bracket, repl_right_bracket, sentence)

        pattern = r'(\d+\.\d+\.\d+\.\d+)'
        sentence = re.sub(pattern, '*', sentence)

        pattern = r"(虚拟机列表：).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, sentence, flags=re.DOTALL)

        pattern = r"(具体原因如下：).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

        pattern = r"(请尽快按照下列方式进行处理：).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

        pattern = r"(请联系供应商进行技术支持。).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

        pattern = r"(请做以下检查：).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

        pattern = r"(建议：\n).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

        pattern = r"(请检查：\n).*"
        replacement = r"\1*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

        pattern = r"(可能原因\d+：).*"
        replacement = r"*"
        s = re.sub(pattern, replacement, s, flags=re.DOTALL)

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
    parts = []
    current_part = ''
    cnt = 0


    for c in s:
        if c == '<':
            if cnt == 0:
                if current_part:
                    parts.append(current_part)
                    current_part = ''
                cnt += 1
                current_part += c
            else:
                cnt += 1
                current_part += c

        elif c == '>':
            cnt -= 1
            current_part += c
            if cnt == 0:
                parts.append(current_part)
                current_part = ''
        else:
            current_part += c

    if current_part:
        parts.append(current_part)


    new_parts = []
    for part in parts:
        if '<' in part and '>' in part:
            new_parts.append(part)
        else:
            pattern = r'([\u4e00-\u9fff\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65℃]+|[a-zA-Z0-9\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+)'
            temp_parts = re.findall(pattern, part)

            for temp_part in temp_parts:
                if re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65℃]+', temp_part):
                    new_parts.extend(jieba.lcut(temp_part))
                else:
                    temp_parts = re.findall(r'\s|[^\s]+', temp_part)
                    for temp_part in temp_parts:
                        sub_parts = re.findall(r'\*|[^\*]+', temp_part)
                        new_parts.extend(sub_parts)

    return new_parts


def calculate_entropy(sentence_list):
    total_count = len(sentence_list)
    counter = Counter(sentence_list)
    entropy = 0.0
    for count in counter.values():
        probability = count / total_count
        entropy -= probability * math.log2(probability)
    return entropy


def get_unknown_sentences(sentences,templates_numbers):

    templates_dict = {}
    for index, element in enumerate(templates_numbers):
        if element not in templates_dict:
            templates_dict[element] = [index]
        else:
            templates_dict[element].append(index)

    unknown_sentences_indedices = []

    for element in templates_dict:
        indices = templates_dict[element]

        if len(indices) == 1:
            unknown_sentences_indedices.append(indices[0])

        else:
            values = [sentences[index] for index in indices]

            if len(set(values)) == 1:
                unknown_sentences_indedices.extend(indices)

    with open("../unknown_indices/alarm_unknown_sentences_indices.txt", "w") as file:
        file.write(" ".join(map(str, unknown_sentences_indedices)))



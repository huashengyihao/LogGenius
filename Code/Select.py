#规整生成的扩充句子
import jieba

import csv
import re
import pandas as pd


def log_select_E(dataset,num,y1,y2):

    expand_sentences = []

    with open('../log_after_gpt/'+ dataset + '_gpt_data.csv', 'r', encoding='gbk') as file:
        reader = csv.reader(file)

        next(reader)

        for row in reader:
            ori_s = row[1]
            expand_sentence = [cell for cell in row[2:] if cell.strip()]

            distances = []

            ori_s_token = split_sentence_E_dataset(ori_s,dataset)

            for sentence in expand_sentence:

                sentence = filter_head_E(sentence)

                sentence_token = split_sentence_E_dataset(sentence,dataset)

                if len(sentence_token) < y1*len(ori_s_token) or len(sentence_token) > y2*len(ori_s_token):
                    continue


                distance = get_distance_E_dataset(sentence_token, ori_s_token)
                distances.append((sentence, distance))

            distances.sort(key=lambda x: x[1])

            for i in range(num):
                if i >= len(distances):
                    break
                expand_sentences.append(distances[i][0])



    with open('../log_after_select/'+ dataset + '_select_top_'+str(num)+'.csv', 'w', encoding='gbk', newline='') as file:
        writer = csv.writer(file)

        for sentence in expand_sentences:
            writer.writerow([sentence])


    with open('../logs/'+dataset+'_2k.log', 'r') as f:
        original_content = f.read()

    with open('../new_dataset/'+dataset+'_new_dataset.txt', 'w') as f:
        f.write(original_content)
        for sentence in expand_sentences:
            f.write('\n'+sentence)

def get_distance_E_dataset(s1_token_list, s2_token_list):
    distance = 0

    for i in range(min(len(s1_token_list),len(s2_token_list))):
        token1 = s1_token_list[i]
        token2 = s2_token_list[i]
        if token1 != token2:
            distance += 1

    distance += max(len(s1_token_list),len(s2_token_list)) - min(len(s1_token_list),len(s2_token_list))

    return distance

def split_sentence_E_dataset(s,dataset):

    if dataset == 'OpenStack':
        filter = [r'((\d+\.){3}\d+,?)+', r'/.+?\s ', r'\d+']
    elif  dataset == 'OpenSSH':
        filter = [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+']
    elif  dataset == 'Apache':
        filter = [r'(\d+\.){3}\d+']
    elif  dataset == 'Zookeeper':
        filter = [r'(/|)(\d+\.){3}\d+(:\d+)?']

    for rgex in filter:
        s = re.sub(rgex, '<*>', s)

    if dataset == 'HealthApp':
        s = re.sub(':', ': ', s)
        s = re.sub('=', '= ', s)
        s = re.sub('\|', '| ', s)
    if dataset == 'Android':
        s = re.sub('\(', '( ', s)
        s = re.sub('\)', ') ', s)
    if dataset == 'Android':
        s = re.sub(':', ': ', s)
        s = re.sub('=', '= ', s)
    if dataset == 'HPC':
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
    s = re.sub(' +', ' ', s).split(' ')

    return s


def filter_head_E(s):

    patterns = [
        r'^\d+\.\s*',
    ]

    for pattern in patterns:
        s = re.sub(pattern, '', s)

    s = s.strip()

    return s


def log_select_C(dataset,num,y1,y2):

    expand_sentences = []

    with open('../log_after_gpt/' + dataset + '_gpt_data.csv', 'r', encoding='gbk') as file:
        reader = csv.reader(file)


        next(reader)


        for row in reader:
            ori_s = row[1]
            expand_sentence = [cell for cell in row[2:] if cell.strip()]

            distances = []

            ori_s_token = split_sentence_C_dataset(ori_s)
            for sentence in expand_sentence:

                sentence = filter_head_C(sentence)

                sentence_token = split_sentence_C_dataset(sentence)

                if len(sentence_token) < y1 * len(ori_s_token) or len(sentence_token) > y2 * len(ori_s_token):
                    continue

                distance = get_distance_C_dataset(sentence_token, ori_s_token)
                distances.append((sentence, distance))

            distances.sort(key=lambda x: x[1])

            for i in range(num):
                if i >= len(distances):
                    break
                expand_sentences.append(distances[i][0])

    with open('../log_after_select/' + dataset + '_select_top_' + str(num) + '.csv', 'w', encoding='gbk',
              newline='') as file:
        writer = csv.writer(file)

        for sentence in expand_sentences:
            writer.writerow([sentence])

    with open('../logs/' + dataset + '_3k.log', 'r') as f:
        original_content = f.read()

    with open('../new_dataset/' + dataset + '_new_dataset.txt', 'w') as f:
        f.write(original_content)
        for sentence in expand_sentences:
            f.write('\n' + sentence)

def split_sentence_C_dataset(s):
    pattern_comma = r','
    repl_comma = '，'
    pattern_left_bracket = r'[（({｛【[]'
    repl_left_bracket = '<'
    pattern_right_bracket = r'[）)}｝】\]]'
    repl_right_bracket = '>'
    s = re.sub(pattern_comma, repl_comma, s)
    s = re.sub(pattern_left_bracket, repl_left_bracket, s)
    s = re.sub(pattern_right_bracket, repl_right_bracket, s)

    filter = [r'(\d+\.\d+\.\d+\.\d+)', r'\(([^\(\)]+)\)', r'（([^（）]+)）', r'\[([^\[\]]+)\]', r'\<([^\<\>]+)\>',
              r'【([^【】]+)】', r'\{([^\{\}]+)\}', r'｛([^｛｝]+)｝', r'<>']

    s = s.rstrip()

    for rgex in filter:
        while re.search(rgex, s):
            s = re.sub(rgex, '*', s)


    pattern = r"(虚拟机列表：).*"
    replacement = r"\1*"
    s = re.sub(pattern, replacement, s, flags=re.DOTALL)

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

    pattern = r"(建议： ).*"
    replacement = r"\1*"
    s = re.sub(pattern, replacement, s, flags=re.DOTALL)

    pattern = r"(请检查： ).*"
    replacement = r"\1*"
    s = re.sub(pattern, replacement, s, flags=re.DOTALL)

    pattern = r"(可能原因\d+：).*"
    replacement = r"*"
    s = re.sub(pattern, replacement, s, flags=re.DOTALL)

    pattern = r'([\u4e00-\u9fff\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65℃]+|[a-zA-Z0-9\s!"#$%&\'()*+,\-./:;<=>?@\[\\\]^_`{|}~]+)'
    parts = re.findall(pattern, s)
    new_parts = []

    for part in parts:
        if re.match(r'[\u4e00-\u9fff\u3000-\u303f\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff65℃]+', part):
            new_parts.extend(jieba.lcut(part))
        else:
            temp_parts = re.findall(r'\s|[^\s]+', part)
            for temp_part in temp_parts:
                if 'f*' in temp_part:
                    new_parts.append(temp_part)
                elif '_*' in temp_part:
                    new_parts.append(temp_part)
                elif 's*' in temp_part:
                    new_parts.append(temp_part)


                else:
                    sub_parts = re.findall(r'\*|[^\*]+', temp_part)
                    new_parts.extend(sub_parts)

    return new_parts


def get_distance_C_dataset(s1_token_list, s2_token_list):
    distance = 0


    for i in range(min(len(s1_token_list),len(s2_token_list))):
        token1 = s1_token_list[i]
        token2 = s2_token_list[i]
        if token1 != token2:
            distance += 1

    distance += max(len(s1_token_list),len(s2_token_list)) - min(len(s1_token_list),len(s2_token_list))

    return distance

def filter_head_C(s):


    patterns = [
        r'^\d+\.\s*',
        r'^告警:\s*',
        r'^告警：\s*',
        r'^警告:\s*',
        r'^警告：\s*',
        r'^告警\d+\:\s*',
        r'^告警\d+\：\s*',
    ]

    for pattern in patterns:
        s = re.sub(pattern, '', s)

    return s
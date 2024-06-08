import openai
import re
import csv
import time
import datetime

def log_gpt_E(sentences, dataset, thre, api_key, model):

    with open('../log_after_entropy/' + dataset + '_expanded_indices_thre_' + str(thre) + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        sentence_indices = next(reader)


    for i in range(1, len(sentence_indices), 1):

        sentence_index = int(sentence_indices[i])
        sentence = sentences[sentence_index]

        print(sentence)

        if "\n" in sentence:
            words = "构造1条类似的数据，只改变其中的变量或参数就行：" + sentence
            expanded_sentences = []

            for _ in range(4):
                response = use_openai_api(words, api_key, model)
                answer = response['choices'][0]['message']['content']
                expanded_sentences.append(answer)
                time.sleep(16)


        else:
            words = "构造10条类似的数据，只改变其中的变量或参数就行：" + sentence
            response = use_openai_api(words, api_key, model)
            answer = response['choices'][0]['message']['content']
            expanded_sentences = answer.split("\n")

        """
        if i == 1:
            answer = "Sure, here are 10 similar data points with varying variables or parameters:\n1.[client 222.166.160.184] Directory index forbidden by rule: /var/www/html/\n2.[client 222.166.160.185] Directory index forbidden by rule: /var/www/html/\n3.[client 222.166.160.186] Directory index forbidden by rule: /var/www/html/"
        else:
            answer = "Certainly, here are 10 similar data points with varying variables or parameters:\n1.mod_jk child init 1 -2\n2.mod_jk child init 1 -3\n3.mod_jk child init 1 -4"

        expanded_sentences = answer.split("\n")
        """

        filename = "../log_after_gpt/" + dataset + "_gpt_data.csv"
        with open(filename, "a", newline="", encoding="gbk") as file:
            writer = csv.writer(file)
            row = [str(i), sentence] + expanded_sentences
            writer.writerow(row)
 
def log_gpt_C(sentences, dataset, thre, api_key, model):

    with open('../log_after_entropy/' + dataset + '_expanded_indices_thre_' + str(thre) + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        sentence_indices = next(reader)


    for i in range(1, len(sentence_indices), 1):


        sentence_index = int(sentence_indices[i])
        sentence = sentences[sentence_index]

        print(sentence)

        if "\n" in sentence:
            words = "构造1条类似的数据，只改变其中的变量或参数就行：" + sentence
            expanded_sentences = []

            for _ in range(4):
                response = use_openai_api(words, api_key, model)
                answer = response['choices'][0]['message']['content']
                expanded_sentences.append(answer)
                time.sleep(16)


        else:
            words = "构造10条类似的数据，只改变其中的变量或参数就行：" + sentence
            response = use_openai_api(words, api_key, model)
            answer = response['choices'][0]['message']['content']
            expanded_sentences = answer.split("\n")


        """
        if i == 1:
            answer = "Sure, here are 10 similar sentences with variable changes:\n1.服务器的可配置内存大小为100GB，已使用95GB，使用率超过95/100，即将无法运行更多的虚拟机，请将虚拟机不必要的内存配置降低或者进行扩容。\n2.服务器的可配置内存大小为120GB，已使用110GB，使用率超过110/120，即将无法运行更多的虚拟机，请将虚拟机不必要的内存配置降低或者进行扩容。\n3.服务器的可配置内存大小为80GB，已使用75GB，使用率超过75/80，即将无法运行更多的虚拟机，请将虚拟机不必要的内存配置降低或者进行扩容。"
        else:
            answer = ""
        expanded_sentences = answer.split("\n")
        """

        filename = "../log_after_gpt/" + dataset + "_gpt_data.csv"
        with open(filename, "a", newline="", encoding="gbk") as file:
            writer = csv.writer(file)
            row = [str(i), sentence] + expanded_sentences
            writer.writerow(row)

 
def use_openai_api(words,api_key,model):

    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model = model,
        messages = [{"role":"user","content":words}]
    )
    return response

 
def write_head(filename):
    with open(filename, "w", newline="", encoding="gbk") as file:
        writer = csv.writer(file)
        writer.writerow(["index","原句子", "扩充句子1", "扩充句子2", "扩充句子3", "扩充句子4"])
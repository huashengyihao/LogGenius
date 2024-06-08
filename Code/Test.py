import csv
import Brain as Ba
import pandas as pd
import random
import re
import jieba
import logging

def main():
    #generate_E()
    print("finish")


#形成英文数据集
def generate_E():
    benchmark_settings = {
        'Apache': {
            'log_file': 'Apache_2k.log',
            'log_format': '\[<Time>\] \[<Level>\] <Content>',
            'regex': [r'(\d+\.){3}\d+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 4
        },
        'Zookeeper': {
            'log_file': 'Zookeeper_2k.log',
            'log_format': '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>',
            'regex': [r'(/|)(\d+\.){3}\d+(:\d+)?'],
            'delimiter': [],
            'tag': 1,
            'theshold': 3
        },
        'OpenSSH': {
            'log_file': 'OpenSSH_2k.log',
            'log_format': '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>',
            'regex': [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 6
        },
        'OpenStack': {
            'log_file': 'OpenStack_2k.log',
            'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>',
            'regex': [r'((\d+\.){3}\d+,?)+', r'/.+?\s ', r'\d+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 5,
        }
    }
    for dataset, setting in benchmark_settings.items():

        if dataset == 'Apache':
            parse = Ba.format_log(
                log_format=setting['log_format'],
                indir='../ori/')
            form = parse.format(setting['log_file'])
            content = form['Content']
            # logID = form['LineId']
            # Date = form['Date']
            # Time = form['Time']
            sentences = content.tolist()

            # 将Content部分写入新文件
            with open('../logs/'+dataset+'_2k.txt', 'w') as new_file:
                for i, sentence in enumerate(sentences):
                    if i == len(sentences) - 1:  # 最后一行不用换行符
                        new_file.write(sentence)
                    else:
                        new_file.write(sentence + '\n')



#

if __name__ == "__main__":
    main()
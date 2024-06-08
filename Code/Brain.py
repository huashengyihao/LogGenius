import datetime
from collections import Counter
import os
import pandas as pd
import re

import csv
import random
import jieba


def get_frequecy_vector(sentences,filter,delimiter,dataset):
    wordlist = {}
    set = {}
    line_id=0
    for s in sentences:

        for rgex in filter:
            s = re.sub(rgex, '<*>', s)
        for de in delimiter:
            s = re.sub(de, '', s)
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
        s = re.sub(' +',' ',s).split(' ')
        s.insert(0,str(line_id))
        lenth = 0
        for token in s:
            set.setdefault(str(lenth), []).append(token)
            lenth += 1
        lena=len(s)
        wordlist.setdefault(lena,[]).append(s)
        line_id+=1
    frequency = {}
    frequency_common={}
    a = max(wordlist.keys())
    i=0
    fre_set={}
    while i < a :

        for word in set[str(i)]:
            word=str(i)+' '+word
            if word in fre_set.keys():
                fre_set[word] = fre_set[word] + 1
            else:
                fre_set[word] = 1
        i += 1
    for key in wordlist.keys():


        for s in wordlist[key]:
            lenth = 0
            fre = []
            fre_common = []
            skip_lineid=1
            for t in s:
                if skip_lineid==1:
                    skip_lineid=0
                    continue
                a=fre_set[str(lenth+1)+' '+t]
                tt = ((a), t, lenth)
                fre.append(tt)
                fre_common.append((a))
                lenth += 1
            frequency.setdefault(key,[]).append(fre)
            frequency_common.setdefault(key,[]).append(fre_common)
    return wordlist,frequency,frequency_common




def parse1(wordlist,frequency):
    index_list = []
    wait_set = {}
    count = 0
    for fre in frequency:
        number = Counter(fre)
        result = number.most_common()
        sorted_result=sorted(result, key=lambda tup: tup[0], reverse=True)
        sorted_result_reverse = sorted(result, key=lambda tup: tup[0])
        if result[0] == sorted_result[0]:
            inde = []
            for index, token in enumerate(fre):
                if token == result[0][0]:
                    inde.append(index)
            index_list.append(inde)
        else:
            index_list.append("placeholder")
            wait_set.setdefault(count,[]).append(sorted_result_reverse)
        count += 1
    return index_list,wait_set

class Tuple_Node():

    def __init__(self,val = None):
        self.val = val
        self.child = set()

    def add_child(self,node):
        if node=='':
            return
        self.child.add(node)




class Tuple_tree:

    def __init__(self, root=None):
        self.root = root

    def child_num(self, node):

        return node.get_child()

    def find_node_val(self,node, node_val):
        for c in node.child:
            if c.val==node_val:
                return  c
            else:
                c=self.find_node_val(c,node_val)
                return c





    def split(self, threshold,node):
        flag=0
        if threshold == 0:
            print('threhold cant be 0')
            return
        branch=node.child
        if node.child==None:
            return 0
        if len(branch)>threshold:
            return 0
        else:
            flag+=1
            return flag
    def cut_branch(self,node,child_set):
        for c in child_set:
            if isinstance(c,node):
                child_set.add(c.val)
                child_set.remove(c)
        return child_set

    def generate_template_path(self, threshold,node):
        flag=0
        if threshold == 0:
            print('threhold cant be 0')
            return
        branch=node.child
        if node.child==None:
            return 0
        if len(branch)>threshold:
            new_child=self.cut_branch(node,child_set=node.child)
            return 0
        else:
            flag+=1
            return flag

def tuple_generate(wordlist,frequency,frequency_common):
    sorted_frequency = {}
    sorted_frequency_common = {}
    sorted_frequency_tuple = {}
    for key in wordlist.keys():
        root_set = {''}
        Tree_set = {''}
        for fre in frequency[key]:
            sorted_fre_reverse = sorted(fre, key=lambda tup: tup[0], reverse=True)
            root_set.add(sorted_fre_reverse[0])
            sorted_frequency.setdefault(key,[]).append(sorted_fre_reverse)
        for fc in frequency_common[key]:
            number = Counter(fc)
            result = number.most_common()
            sorted_result = sorted(result, key=lambda tup: tup[1], reverse=True)
            sorted_fre = sorted(result, key=lambda tup: tup[0], reverse=True)
            sorted_frequency_common.setdefault(key,[]).append(sorted_result)
            sorted_frequency_tuple.setdefault(key,[]).append(sorted_fre)
    return sorted_frequency, sorted_frequency_common, sorted_frequency_tuple

class tupletree:

    def __init__(self,sorted_frequency,sorted_frequency_common,sorted_frequency_tuple,frequency,wordlist):
        self.sorted_frequency=sorted_frequency
        self.sorted_frequency_common=sorted_frequency_common
        self.sorted_frequency_tuple = sorted_frequency_tuple
        self.frequency = frequency
        self.wordlist = wordlist

    def find_root(self, threshold_per):
        root_set_detail={}
        detail_inorder={}
        root_set = {}
        i=0
        for fc in self.sorted_frequency_common:
            count=self.wordlist[i]
            threshold=(max(fc, key=lambda tup: tup[0])[0])*threshold_per
            m=0
            for fc_w in fc:
                if fc_w[0]>=threshold:
                    a = self.sorted_frequency[i].append((int(count[0]), -1, -1))
                    root_set_detail.setdefault(fc_w,[]).append(self.sorted_frequency[i])
                    root_set.setdefault(fc_w,[]).append(self.sorted_frequency_tuple[i])
                    detail_inorder.setdefault(fc_w, []).append(self.frequency[i])
                    break
                if fc_w[0]>=m:
                    candidate=fc_w
                    m=fc_w[0]
                if fc_w == fc[len(fc)-1]:
                    a = self.sorted_frequency[i].append((int(count[0]), -1, -1))
                    root_set_detail.setdefault(candidate, []).append(self.sorted_frequency[i])
                    root_set.setdefault(candidate, []).append(self.sorted_frequency_tuple[i])
                    detail_inorder.setdefault(fc_w, []).append(self.frequency[i])
            i+=1
        return root_set_detail,root_set,detail_inorder

    def up_split(self,root_set_detail,root_set):
        new_root_set_detail={}
        for key in root_set.keys():
            tree_node=root_set[key]
            father_count = []
            for node in tree_node:
                pos = node.index(key)
                for i in range(pos):
                    father_count.append(node[i])
            father_set=set(father_count)
            for father in father_set:
                if father_count.count(father)==key[0]:
                    continue
                else:
                    for i in range(len(root_set_detail[key])):
                        for k in range(len(root_set_detail[key][i])):
                                if father[0] == root_set_detail[key][i][k]:
                                    root_set_detail[key][i][k]=(root_set_detail[key][i][k][0],'<*>',root_set_detail[key][i][k][2])
                    break
        return root_set_detail

    def down_split(self,root_set_detail,root_set,threshold, fr_inorder):

        father_template_set = {}
        over2 = 0
        over = 0
        for key in root_set.keys():
            thre = threshold
            tree_node = root_set[key]
            detail=root_set_detail[key]
            detail_order=fr_inorder[key]
            m=[]
            child={}
            variable={''}
            variable.remove('')
            variable_set={''}
            variable_set.remove('')
            m_count=0
            fist_sentence=detail_order[0]
            for det in fist_sentence:
                if det[0] != key[0]:
                    m.append(m_count)
                m_count+=1
            for i in m:
                for node in detail_order:
                    if i <len(node):
                        #child.setdefault(i, []).append(tuple([n for n in node[:i+1]]))
                        child.setdefault(i, []).append(node[i][1])
            v_flag = 0


            for i in m:
                next={''}
                next.remove('')
                result = set(child[i])
                freq = len(result)
                if freq>=thre:
                        variable=variable.union(result)

                v_flag+=1
            i=0
            while i < len(root_set_detail[key]):
                j=0
                while j < len(root_set_detail[key][i]):
                    if isinstance(root_set_detail[key][i][j],tuple):
                        if root_set_detail[key][i][j][1] in variable:
                            root_set_detail[key][i][j] = (
                            root_set_detail[key][i][j][0], '<*>', root_set_detail[key][i][j][2])
                    j += 1
                i+=1
        return root_set_detail

def output_result(wordlist,parse_result,tag):
    template_set={}
    for key in parse_result.keys():

        for pr in parse_result[key]:

            sort = sorted(pr, key=lambda tup: tup[2])
            i=1
            template=[]

            while i < len(sort):
                this=sort[i][1]
                if bool(re.search(r"/", this)):
                    template.append('<*>')
                    i += 1
                    continue
                if this.isdigit():
                    template.append('<*>')
                    i+=1
                    continue
                if bool('<*>' in this):
                    template.append('<*>')
                    i+=1
                    continue
                if tag ==1:
                    if bool(re.search(r'\d', this)):
                        template.append('<*>')
                        i += 1
                        continue
                template.append(sort[i][1])
                i+=1

            template=tuple(template)
            template_set.setdefault(template,[]).append(pr[len(pr)-1][0])
    return template_set


def parse_E(sentences,filter,dataset,threshold,delimiter,tag,starttime,efficiency):


    origin_sentences = sentences.copy()

    wordlist, frequency, frequency_common = get_frequecy_vector(sentences, filter,delimiter,dataset)
    sorted_frequency, sorted_frequency_common, sorted_frequency_tuple = tuple_generate(wordlist, frequency,
                                                                                          frequency_common)
    group_accuracy_correct = 0
    template_set = {}
    loglines = 0
    correct_choose = 0
    for key in wordlist.keys():
        sf = sorted_frequency[key]
        sfc = sorted_frequency_common[key]
        sft = sorted_frequency_tuple[key]
        fr = frequency[key]
        wl=wordlist[key]
        Tree = tupletree(sf, sfc, sft, fr,wl)
        root_set_detail, root_set, fr_inorder = Tree.find_root(0)
        '''
        ### code for root node choose evaluation.
        for k in root_set_detail:
            choose_flag=1
            for log in root_set_detail[k]:
                c=0
                loglines+=1
                while c <len(log)-1:
                    if log[c][0]==k[0]:
                        if "<*>" in log[c][1] and log[c][1] not in template[log[len(log)-1][0]]:
                            choose_flag=0
                    if choose_flag==0:
                        break
                    c+=1
                if choose_flag == 0:
                    break
                correct_choose+=1
        '''

        root_set_detail = Tree.up_split(root_set_detail, root_set)
        parse_result = Tree.down_split(root_set_detail, root_set, threshold, fr_inorder)
        template_set.update(output_result(wordlist, parse_result,tag))
    '''
    ### code for root node choose evaluation.
    print(
        "correct choose root noed ratio ==" + str(correct_choose / loglines) + "===detail===correct_choose:" + str(
            correct_choose) + " logline:" + str(loglines))
    '''
    endtime=datetime.datetime.now()
    print("### Time cost4 ###" + str(endtime-starttime))
    if efficiency==True:
        return endtime
    '''
    output parsing result
    '''

    if dataset in ['HDFS', 'Hadoop', 'Spark', 'Zookeeper', 'BGL', 'HPC', 'Thunderbird', 'Windows', 'Linux',
                   'Android', 'HealthApp', 'Apache', 'OpenSSH', 'OpenStack', 'Mac']:
        with open('../log_after_group/' + dataset + '_template.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['模板', '句子标号'])

            for k1 in template_set.keys():
                template = ' '.join(list(k1))
                sentence_numbers = ','.join(str(x) for x in template_set[k1])
                writer.writerow([template, sentence_numbers])



    Groupaccuracy=group_accuracy_correct/2000
    return Groupaccuracy





class format_log:    # this part of code is from LogPai https://github.com/LogPai

    def __init__(self, log_format, indir='./'):
        self.path = indir
        self.logName = None
        self.df_log = None
        self.log_format = log_format

    def format(self, logName):


        self.logName=logName

        self.load_data()

        return self.df_log





    def generate_logformat_regex(self, logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\\\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex
    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """ Function to transform log file to dataframe
        """
        log_messages = []
        linecount = 0
        with open(log_file, 'r', encoding='UTF-8') as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
                if linecount==2000000:
                    break
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf


    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.log_format)
        self.df_log = self.log_to_dataframe(os.path.join(self.path, self.logName), regex, headers, self.log_format)


def parse_C(sentences,filter,dataset,threshold,delimiter,tag,starttime,efficiency):

    sentences = get_united_sentences(sentences)

    wordlist, frequency, frequency_common = get_frequecy_vector_alarm(sentences, filter, delimiter, dataset)

    sorted_frequency, sorted_frequency_common, sorted_frequency_tuple = tuple_generate(wordlist, frequency,
                                                                                       frequency_common)

    group_accuracy_correct = 0
    template_set = {}
    loglines = 0
    correct_choose = 0

    for key in wordlist.keys():
        sf = sorted_frequency[key]
        sfc = sorted_frequency_common[key]
        sft = sorted_frequency_tuple[key]
        fr = frequency[key]
        wl = wordlist[key]
        Tree = tupletree(sf, sfc, sft, fr, wl)
        root_set_detail, root_set, fr_inorder = Tree.find_root(0)
        '''
        ### code for root node choose evaluation.
        for k in root_set_detail:
            choose_flag=1
            for log in root_set_detail[k]:
                c=0
                loglines+=1
                while c <len(log)-1:
                    if log[c][0]==k[0]:
                        if "<*>" in log[c][1] and log[c][1] not in template[log[len(log)-1][0]]:
                            choose_flag=0
                    if choose_flag==0:
                        break
                    c+=1
                if choose_flag == 0:
                    break
                correct_choose+=1
        '''

        root_set_detail = Tree.up_split(root_set_detail, root_set)
        parse_result = Tree.down_split(root_set_detail, root_set, threshold, fr_inorder)
        template_set.update(output_result_alarm(wordlist, parse_result, tag))

    '''
    ### code for root node choose evaluation.
    print(
        "correct choose root noed ratio ==" + str(correct_choose / loglines) + "===detail===correct_choose:" + str(
            correct_choose) + " logline:" + str(loglines))
    '''
    endtime = datetime.datetime.now()
    print("### Time cost4 ###" + str(endtime - starttime))
    if efficiency == True:
        return endtime
    '''
    output parsing result
    '''
    template = sentences
    template_num = 0
    group_accuracy_correct = 0
    """
    for k1 in template_set.keys():
        group_accuracy = {''}
        group_accuracy.remove('')
        for i in template_set[k1]:                    
            group_accuracy.add(structured[i])
            template[i]=k1
            template_num += 1
        if len(group_accuracy) == 1:
            count = a.count(a[i])
            if count == len(template_set[k1]):
                group_accuracy_correct += len(template_set[k1])
    df_example['Template']=template
    df_example.to_csv('../Parseresult/' + dataset + 'result.csv', index=False)
    """


    with open('../log_after_group/'+dataset+'_template.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['模板', '句子标号'])

        for k1 in template_set.keys():
            template = ''.join(list(k1))
            sentence_numbers = ','.join(str(x) for x in template_set[k1])
            writer.writerow([template, sentence_numbers])


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


        replaced_sentences.append(sentence)
    return replaced_sentences

def get_frequecy_vector_alarm(sentences,filter,delimiter,dataset):
    wordlist = {}
    set = {}
    line_id=0
    for s in sentences:

        for rgex in filter:
            while re.search(rgex, s):
                s = re.sub(rgex, '*', s)
        for de in delimiter:
            s = re.sub(de, '', s)


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

        s = split_sentence(s)

        s.insert(0, str(line_id))
        lenth = 0
        for token in s:
            set.setdefault(str(lenth), []).append(token)
            lenth += 1
        lena = len(s)
        wordlist.setdefault(lena, []).append(s)
        line_id += 1

    frequency = {}
    frequency_common = {}
    a = max(wordlist.keys())
    i = 0
    fre_set = {}

    while i < a :

        for word in set[str(i)]:
            word=str(i)+' '+word
            if word in fre_set.keys():
                fre_set[word] = fre_set[word] + 1
            else:
                fre_set[word] = 1
        i += 1

    for key in wordlist.keys():

        for s in wordlist[key]:
            lenth = 0
            fre = []
            fre_common = []
            skip_lineid=1
            for t in s:
                if skip_lineid==1:
                    skip_lineid=0
                    continue
                a=fre_set[str(lenth+1)+' '+t]
                tt = ((a), t, lenth)
                fre.append(tt)
                fre_common.append((a))
                lenth += 1


            frequency.setdefault(key,[]).append(fre)

            frequency_common.setdefault(key,[]).append(fre_common)
    return wordlist,frequency,frequency_common


def split_sentence(s):

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


def output_result_alarm(wordlist,parse_result,tag):
    template_set = {}
    for key in parse_result.keys():

        for pr in parse_result[key]:

            sort = sorted(pr, key=lambda tup: tup[2])
            i = 1
            template = []

            while i < len(sort):
                this = sort[i][1]

                """
                if bool(re.search(r"/", this)):
                    template.append('*')
                    i += 1
                    continue
                """

                if bool('%' in this):
                    template.append('*')
                    i += 1
                    continue

                if this.isdigit():
                    template.append('*')
                    i += 1
                    continue
                if bool('*' in this):
                    template.append('*')
                    i += 1
                    continue
                if tag == 1:
                    if bool(re.search(r'\d', this)):
                        template.append('*')
                        i += 1
                        continue
                template.append(sort[i][1])
                i += 1

            template = tuple(template)
            template_set.setdefault(template, []).append(pr[len(pr) - 1][0])
    return template_set



#SB.get_eval_metric('../SaveFiles&Output/Parseresult/Proxifier/Proxifier88.csv','../SaveFiles&Output/Parseresult/Proxifier/template.csv')
'''

    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'delimiter': ['[,!?=]']
    },
'''



import datetime
import Brain as Ba
import Entropy_E as EE
import Entropy_C as EC
import GPT
import Select as Se

def main():
    E_dataset()
    #C_dataset()


 
def E_dataset():
    input_dir = '../logs/'
    output_dir = '../new_dataset/'
    log_file = 'Apache_2k.log'
    dataset_name = 'Apache'

    """
    日志格式设置
    """
    benchmark_settings = {
        'Apache': {
            'log_file': log_file,
            'log_format': '\[<Time>\] \[<Level>\] <Content>',
            'regex': [r'(\d+\.){3}\d+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 4
        },
        'Zookeeper': {
            'log_file': log_file,
            'log_format': '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>',
            'regex': [r'(/|)(\d+\.){3}\d+(:\d+)?'],
            'delimiter': [],
            'tag': 1,
            'theshold': 3
        },
        'OpenSSH': {
            'log_file': log_file,
            'log_format': '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>',
            'regex': [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 6
        },
        'OpenStack': {
            'log_file': log_file,
            'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>',
            'regex': [r'((\d+\.){3}\d+,?)+', r'/.+?\s ', r'\d+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 5,
        }
    }
    for dataset, setting in benchmark_settings.items():

        if dataset == dataset_name:
            starttime = datetime.datetime.now()
            parse = Ba.format_log(
                log_format=setting['log_format'],
                indir='../logs/')
            form = parse.format(setting['log_file'])
            content = form['Content']
            # logID = form['LineId']
            # Date = form['Date']
            # Time = form['Time']
            start = datetime.datetime.now()
            sentences = content.tolist()

            origin_sentences = sentences.copy()


            GA = Ba.parse_E(sentences, setting['regex'], dataset, setting['theshold'], setting['delimiter'],setting['tag'], starttime, efficiency=False)

            thre = 0
            EE.log_entropy_E(origin_sentences,thre,dataset,setting['regex'])


            filename = "../log_after_gpt/" + dataset + "_gpt_data.csv"
            #GPT.write_head(filename)
            api_key = "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"
            model = "gpt-3.5-turbo"
            #GPT.log_gpt_E(origin_sentences,dataset,0,api_key,model)

            num = 3
            y1 = 0.8
            y2 = 1.2
            Se.log_select_E(dataset,num,y1,y2)

 
def C_dataset():
    input_dir = '../logs/'
    output_dir = '../new_dataset/'
    log_file = "alarm_3k.log";

    filter = [r'(\d+\.\d+\.\d+\.\d+)', r'\(([^\(\)]+)\)', r'（([^（）]+)）', r'\[([^\[\]]+)\]', r'\<([^\<\>]+)\>',
              r'【([^【】]+)】', r'\{([^\{\}]+)\}', r'｛([^｛｝]+)｝', r'<>']
    # filter = [r'(\d+\.\d+\.\d+\.\d+)']
    threshold = 3
    delimiter = []
    tag = 0
    starttime = datetime.datetime.now()
    efficiency = False
    dataset = 'alarm'

    sentences = []
    with open('../logs/'+ log_file, 'r') as f:
        for line in f:
            sentences.append(line.rstrip())

    origin_sentences = sentences.copy()

    GA = Ba.parse_C(sentences, filter, dataset, threshold, delimiter, tag, starttime, efficiency)

    thre = 0
    EC.log_entropy_C(origin_sentences, thre, dataset)

    filename = "../log_after_gpt/" + dataset + "_gpt_data.csv"
    #GPT.write_head(filename)
 
    api_key = "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"
    model = "gpt-3.5-turbo"
    #GPT.log_gpt_C(origin_sentences,dataset,0,api_key,model)

    top_n = 3
    y1 = 0.8
    y2 = 1.2
    Se.log_select_C(dataset,top_n,y1,y2)


if __name__ == "__main__":
    main()
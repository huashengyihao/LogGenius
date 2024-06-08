import datetime
import Brain as Ba


 
def log_group(log_file):

    benchmark_settings = {
        'Apache': {
            'log_file': log_file,
            'log_format': '<Content>',
            'regex': [r'(\d+\.){3}\d+'],
            'delimiter': [],
            'tag': 0,
            'theshold': 4
        }
    }


    for dataset, setting in benchmark_settings.items():

        if dataset == 'Apache':
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

            GA = Ba.parse(sentences, setting['regex'], dataset, setting['theshold'], setting['delimiter'],
                          setting['tag'], starttime, efficiency=False)
            print('=====' + dataset + '======   :' + str(GA))
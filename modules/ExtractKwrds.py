import pandas as pd
import numpy as np
import pickle
from konlpy.tag import Komoran, Hannanum
from sklearn.preprocessing import normalize
import re
from modules.textrank import KeywordSummarizer

class DataProcessUnit(KeywordSummarizer):

    def __init__(self, yt_trending_vd, comments):
        self.data           = yt_trending_vd
        self.comments       = comments
        self.dataLength     = len(yt_trending_vd)
        self.textData       = []
        self.keywords       = []
        self.foreignkeySet  = []
        self.processedData  = []

    def cleansing(self, text):  
        if text == None: return None
        pattern = '(\[a-zA-Z0-9\_.+-\]+@\[a-zA-Z0-9-\]+.\[a-zA-Z0-9-.\]+)' # e-mail 주소 제거  
        text = re.sub(pattern=pattern,repl=' ',string=text)

        pattern = '(http|ftp|https)://(?:[-\w.]|(?:\da-fA-F]{2}))+'  # url 제거
        text = re.sub(pattern=pattern,repl=' ',string=text)

        pattern = '([ㄱ-ㅎㅏ-ㅣ])+'                                  # 한글 자음, 모음 제거
        text = re.sub(pattern=pattern,repl=' ',string=text)

        pattern = '<[^>]*>'                                          # html tag 제거
        text = re.sub(pattern=pattern,repl=' ',string=text)

        pattern = '[\r|\n]'                                          # \r, \n 제거
        text = re.sub(pattern=pattern,repl=' ',string=text)

        pattern = '[^\w\s]'                                          # 특수기호 제거
        text = re.sub(pattern=pattern,repl=' ',string=text)

        pattern = re.compile(r'\s+')                                 # 이중 space 제거
        text = re.sub(pattern=pattern,repl=' ',string=text)
        return(text)

    def preprocessData(self):
        for i in range(self.dataLength):
            self.textData.append([
                self.cleansing(self.data['video_title'][i]),
                self.cleansing(self.data['description'][i]),
                self.data['hashtags'][i]
                                 ])
            
            self.foreignkeySet.append([
                self.data['id'][i]
                # self.data['video_url'][i],
                # self.data['collect_datetime'][i]
            ])

    def komoran_tokenizer(self, sent, nWordSet = 1):
        # words = komoran.pos(sent, join=True)
        # words = [w for w in words if ('/NN' in w or '/XR' in w or '/VA' in w or '/VV' in w)]
        # words = komoran.nouns(sent)
        # words = hannaum.nouns(sent)

        words = sent.split()
        result = []

        if (len(words)-nWordSet+1) <= 0:
            return words
        else:
            for i in range(0, len(words)-nWordSet+1):
                # tmp = words[0:nWordSet]
                # for j in range(i, len(words)+i, nWordSet):
                
                result.append(" ".join(words[i:i+nWordSet]))
                    # print(i, len(words)+i, tmp[-1])
            
        # print(result)
            return result
    
    def extractKeywords(self, nWordSet = 1, topk=5):
        keyword_summarizer = KeywordSummarizer(tokenize=self.komoran_tokenizer, nWordSet=nWordSet, min_count=1, min_cooccurrence=1)

        for i in range(self.dataLength):
        # for i in range):
            lst = self.textData[i]
            tmp = [lst[0], 
                lst[0] if len(lst[1]) == 1 or len(lst[1]) == 0 else lst[1],
                lst[0] if len(lst[2]) == 1 or len(lst[2]) == 0 else lst[2]]
            tmplst = keyword_summarizer.summarize(tmp, topk=topk)
            topRates = [keyword[0] for keyword in tmplst[:topk]]
            self.keywords.append(topRates)
        return self.keywords
    

    def processData(self, nWordSet):
        resultDict = []
        for i in range(self.dataLength):
            resultDict.append([self.foreignkeySet[i][0], 
                            #    self.foreignkeySet[i][1], self.foreignkeySet[i][2],
                                # nWordSet, 
                                ','.join(self.keywords[i])])

        self.processedData = pd.DataFrame(resultDict, 
                                columns=['id', 
                                        #  'video_url', 'collected_date',
                                        #  'n_gram', 
                                         'keywords'])
    
    def getProcessedData(self):
        return self.processedData
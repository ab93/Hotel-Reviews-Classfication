__author__ = 'Avik'

import os
import sys
import json
import math
from decimal import *
import re
from collections import defaultdict

stopWords = ['i','me','my','myself','we','our','ours','ourselves','you','your','yours',
             'yourself','yourselves','he','him','his','himself','she','her','hers','herself',
             'it','its','itself','they','them','their','theirs','themselves','what','which',
             'who','whom','this','that','these','those','am','is','are','was','were','be','been',
             'being','have','has','had','having','do','does','did','doing','a','an','the','and',
             'but','if','or','because','as','until','while','of','at','by','for','with','about',
             'against','between','into','through','during','before','after','above','below','to',
             'from','up','down','in','out','on','off','over','under','again','further','then',
             'once','here','there','when','where','why','how','all','any','both','each','few',
             'more','most','other','some','such','no','nor','not','only','own','same',
             'so','than','too','very','s','t','can','will','just','don','should','now']

punctuationList = ["!",'"',"#","$","%","&","'","(",")","*","+",",","-",".","/",":",";","<","=",">","?","@",
                "[",'\\',']','^','_','`','{','|','}','~']

classes = []


def writeJSON(condProb):
    with open('nbmodel.txt','w+') as f:
        json.dump(condProb, f)

def calculateFeatures(vocabSet,classCount,termFreq,textLen):
    priorProb = [0.0 for i in range(4)]
    condProb = {}

    for i in range(4):
        #print classCount[i],sum(classCount)
        priorProb[i] = classCount[i]/sum(classCount)
        #raw_input()

    for word in termFreq.keys():
        condProb[word] = [0.0 for i in range(4)]
        for c in range(4):
            #condProb[word][c] = math.log((Decimal(termFreq[word][c] + 1))/(textLen[c] + len(vocabSet)))
            condProb[word][c] = (termFreq[word][c] + 1)/(textLen[c] + len(vocabSet))

    condProb['PRIOR'] = priorProb
    writeJSON(condProb)



def preProcess(path):
    punctString = ''
    for item in punctuationList:
        punctString = punctString + str(item)
    remove = punctString

    distinctWords = set()
    termFreq = defaultdict(lambda: [0.0 for i in range(4)])
    textLen = [0.0 for i in range(4)]   ##total words in each class i.e. |B|
    totalFiles = 0
    classCount = [0.0 for i in range(4)]

    for root,dirs,files in os.walk(path,topdown=False):
        #print dirs
        for name in files:
            if name not in ['.DS_Store','LICENSE','README.md','README.txt']:
                totalFiles += 1
                parentDirs = root.split('/')[1:3]

                if re.search(r'(.)*positive(.)*',root):
                    classCount[0] += 1
                    index1 = 0
                    if re.search(r'(.)*truthful(.)*',root):
                        classCount[2] += 1
                        index2 = 2
                    elif re.search(r'(.)*deceptive(.)*',root):
                        classCount[3] += 1                     # 3 is deceptive
                        index2 = 3

                elif re.search(r'(.)*negative(.)*',root):
                    classCount[1] += 1
                    index1 = 1
                    if re.search(r'(.)*truthful(.)*',root):
                        classCount[2] += 1
                        index2 = 2
                    elif re.search(r'(.)*deceptive(.)*',root):
                        classCount[3] += 1                     # 3 is deceptive
                        index2 = 3


                '''
                if parentDirs[0] == 'positive_polarity':   # 0 is positive
                    classCount[0] += 1
                    index1 = 0
                else:                                      # 1 is negative
                    classCount[1] += 1
                    index1 = 1
                if parentDirs[1] in ['truthful_from_TripAdvisor','truthful_from_Web'] :  # 2 is truthful
                    classCount[2] += 1
                    index2 = 2
                else:
                    classCount[3] += 1                     # 3 is deceptive
                    index2 = 3
                '''

                with open(os.path.join(root,name),'r') as f:
                    data = f.read()
                    data = data.lower().translate(None,remove)
                    data = ' '.join([word for word in data.split() if word not in stopWords])

                    for word in data.strip().split(' '):
                        distinctWords.add(word)
                        textLen[index1] += 1
                        termFreq[word][index1] += 1
                        textLen[index2] += 1
                        termFreq[word][index2] += 1


    return distinctWords,classCount, termFreq, textLen
                #raw_input()


def main():
    #print('hello')
    vocabSize,classCount,termFreq,textLen = preProcess(sys.argv[1])
    calculateFeatures(vocabSize,classCount,termFreq,textLen)

if __name__ == '__main__':
    main()
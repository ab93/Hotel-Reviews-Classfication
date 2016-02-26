__author__ = 'Avik'

import os
import sys
import json
import math
import re
from decimal import *
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



def calculateScore():
    precision = [0.0 for i in range(4)]
    recall = [0.0 for i in range(4)]
    f1 = [0.0 for i in range(4)]

    with open('nboutput.txt','r') as outputFile:
        data = outputFile.readlines()

    tp = [0.0 for i in range(4)]
    fp = [0.0 for i in range(4)]
    fn = [0.0 for i in range(4)]

    for line in data:
        line = line.strip('\n').split(' ')
        if (line[1] == 'positive') and ( re.search(r'(.)*positive(.)*',line[2]) ):
            tp[0] += 1
        elif (line[1] == 'positive') and ( re.search(r'(.)*negative(.)*',line[2]) ):
            fp[0] += 1
        elif (line[1] == 'negative') and ( re.search(r'(.)*positive(.)*',line[2]) ):
            fn[0] += 1

        if (line[1] == 'negative') and ( re.search(r'(.)*negative(.)*',line[2]) ):
            tp[1] += 1
        elif (line[1] == 'negative') and ( re.search(r'(.)*positive(.)*',line[2]) ):
            fp[1] += 1
        elif (line[1] == 'positive') and ( re.search(r'(.)*negative(.)*',line[2]) ):
            fn[1] += 1

        if (line[0] == 'truthful') and ( re.search(r'(.)*truthful(.)*',line[2]) ):
            tp[2] += 1
        elif (line[1] == 'truthful') and ( re.search(r'(.)*deceptive(.)*',line[2]) ):
            fp[2] += 1
        elif (line[1] == 'deceptive') and ( re.search(r'(.)*truthful(.)*',line[2]) ):
            fn[2] += 1

        if (line[0] == 'deceptive') and ( re.search(r'(.)*deceptive(.)*',line[2]) ):
            tp[3] += 1
        elif (line[1] == 'deceptive') and ( re.search(r'(.)*truthful(.)*',line[2]) ):
            fp[3] += 1
        elif (line[1] == 'truthful') and ( re.search(r'(.)*deceptive(.)*',line[2]) ):
            fn[3] += 1

    #print tp
    #print fp
    #print fn

    for c in range(4):
        precision[c] = tp[c]/(tp[c] + fp[c])
        recall[c] = tp[c] / (tp[c] + fn[c])
        f1[c] = (2 * precision[c] * recall[c]) / (precision[c] + recall[c])
    #P = tp/(tp + fp)
    #R = tp/(tp + fn)
    print "Precision:", precision
    print "Recall:",recall
    print "F1:",f1
    print "F1 avg:",sum(f1)/4.0

    #print line



def readFeatures():
    with open('nbmodel.txt','r') as jsonFile:
        condProb = json.load(jsonFile)
    priorProb =  condProb['PRIOR']
    del condProb['PRIOR']

    return priorProb,condProb

def writeFile(path,classProb):
    index1 = classProb.index(max(classProb[0:2]))
    index2 = classProb.index(max(classProb[2:4]))
    #print path,index1,index2
    #raw_input()
    with open('nboutput.txt','a+') as outputFile:
        if index2 == 2:
            outputFile.write("truthful" + ' ')
        else:
            outputFile.write("deceptive" + ' ')
        if index1 == 0:
            outputFile.write("positive" + ' ')
        else:
            outputFile.write("negative" + ' ')
        outputFile.write(path + '\n')


def readTestFiles(path,priorProb,condProb):
    punctString = ''
    for item in punctuationList:
        punctString = punctString + str(item)
    remove = punctString

    f = open('nboutput.txt','w+')
    f.close()

    for root,dirs,files in os.walk(path,topdown=False):
        for name in files:
            classProb = [math.log(prob,2) for prob in priorProb]
            #classProb = [prob for prob in priorProb]
            #print classProb
            #raw_input()
            if name not in ['.DS_Store','LICENSE','README.md','README.txt']:
                with open(os.path.join(root,name),'r') as f:
                    data =  f.read()
                    data =  data.lower().translate(None,remove)
                    data = ' '.join([word for word in data.split() if word not in stopWords])
                #print data
                #raw_input()

                    for word in data.strip().split(' '):
                        if word not in condProb:
                            continue

                        #classProb = map(Decimal,classProb)
                        for c in range(len(classProb)):
                            #classProb[c] *= condProb[word][c]
                            #classProb[c] += condProb[word][c]
                            classProb[c] += math.log(condProb[word][c],2)
                        #print classProb

                #print name
                #print classProb
                #raw_input()
                writeFile(os.path.join(root,name),classProb)
            #raw_input()

def main():
    priorProb, condProb = readFeatures()
    readTestFiles(sys.argv[1],priorProb,condProb)
    calculateScore()

if __name__ == '__main__':
    main()
from bs4 import BeautifulSoup
import re
import datetime as dt
from cv2 import getNumberOfCPUs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy

numbers = '0123456789'

def between(s, leader, trailer):
    try:
        end_of_leader = s.index(leader) + len(leader)
        start_of_trailer = s.index(trailer, end_of_leader)        
        return s[end_of_leader:start_of_trailer]
    except:
        print(s)
        return '-1'

def numberIndex(s):
    firstnumberflag = True
    fi = -1
    d = {}
    for i in range(len(s)):
        if s[i] in numbers:
            if firstnumberflag:
                fi = i
                d[i] = s[i]
                firstnumberflag = False
            else:
                d[fi] = d[fi] +s[i]
        else:
            firstnumberflag = True
    return d

def numbersAfter(s, leader):
    try:
        end_of_leader = s.index(leader) + len(leader)
        start_of_trailer = end_of_leader+1
        while(s[start_of_trailer] in numbers):
            start_of_trailer += 1
        return s[end_of_leader:start_of_trailer]
    except:
        print(s)
        return '-1'
def numbersBefore(s:str, trailer):
    try:
        start_of_trailer = s.index(trailer)
        end_of_leader = start_of_trailer-1
        while(s[end_of_leader] in numbers):
            end_of_leader -= 1
        return s[end_of_leader+1:start_of_trailer]
    except:
        print(s)
        return '-1'
    
def getNearestI(l, x):
    min = 2**10
    for i in range(len(l)):
        if abs(l[i]-x) < min:
            res = l[i]
    return res
def getQuData(s:str):
    # s : 2022年4月1日，徐汇区新增37例本土确诊病例，新增602例本土无症状感染者，分别居住于：
    # s : 2022年4月23日，松江区新增本土新冠肺炎确诊病例32例，新增本土无症状感染者741例，分别居住于：
    good = True
    sinput = copy.copy(s)
    s = s[s.index('，')+1:]
    s = s.replace('无症状', 'wu症状')
    s = s.replace('无', '0')
    try:
        d = numberIndex(s)
        name = between(s, '', s[s.index('区')+1])
        name = '浦东新区' if name=='浦东' else name
        if "本土确诊" not in s:
            # '金山区新增44本土wu症状感染者，其中部分病例之前已落实管控，其余居住于：'
            qz = '0'
            wzz = d[list(d.keys())[0]]
        elif "wu症状" not in s:
            wzz = '0'
            qz = d[list(d.keys())[0]]
        elif len(d) == 2:
            qzi, wzzi = sorted(d.keys())
            qz, wzz = d[qzi], d[wzzi]
        else:
            qzStringI = s.index("本土确诊")
            wzzStringI = s.index("wu症状")
            qzi = getNearestI(list(d.keys()), qzStringI)
            wzzi = getNearestI(list(d.keys()), wzzStringI)
            qz, wzz = d[qzi], d[wzzi]
    except:
        print(s)
        print(sinput)
        name, qz, wzz = ['-1']*3
        good = False
    return copy.copy((name, qz, wzz, good))

def getData(fileName):
    """_summary_

    Args:
        fileName (_type_): _description_

    Returns:
        [
            日期(datetime对象), 
            新增本土新冠肺炎确诊病例, 新增无症状感染者, 
            [[区名, 区新增本土确诊病例, 区新增本土无症状感染者],...]
        ]
    """
    with open(fileName, encoding="utf-8") as html:
        bs = BeautifulSoup(html, 'lxml')
        L = []
        dateOKflag = False
        zqz,zwzz = -1,-1
        last = ''
        lastisgood = True
        for span in bs.find_all('span'):
            #print(span.string,end='/')
            if span.string == None:
                continue
            if span.string[-1]=='，':
                last = last + span.string[:]
                continue
            else:
                last = ''
            s = last + span.string
            if s[0] == '市' and '市卫健委' in s:
                #print(s)
                if s.count('（') != 1:
                    zqz, zwzz = numbersAfter(s,'新增本土新冠肺炎确诊病例'), numbersAfter(s,'无症状感染者')
                else:
                    zqz, zwzz = numbersAfter(s,'新增本土新冠肺炎确诊病例'), numbersAfter(s,'无症状感染者')
            elif s[0] == '2' and '，' in s:
                #print(s)
                if not dateOKflag and s[0] != '市':
                    dates = between(s, '', '，')
                    date = dt.date(int(between(dates,'','年')), int(between(dates,'年','月')), int(between(dates,'月','日')))
                    dateOKflag = True
                qu, qz, wzz, lastisgood = getQuData(s)
                L.append([qu, int(qz), int(wzz)][:])
            try:
                int(zqz)
            except:
                zqz = -1
            try:
                int(zwzz)
            except:
                zwzz = -1
        return date, int(zqz), int(zwzz), L

if __name__ == "__main__":
    filepath = 'htmls'
    filenumber = 38
    D = []
    for i in range(filenumber):
        data = getData("{}/{}.html".format(filepath, i))
        D.append(data)
    D.sort(key=lambda x:x[0])
    qus = [D[11][3][i][0] for i in range(len(D[11][3]))]
    print(qus)
    print(D[11])
    quDict = {}
    head = ["新增本土确诊","新增无症状"]
    for i in range(len(qus)):
        quDict[qus[i]] = i
        head.append(qus[i]+"新增本土确诊")
        head.append(qus[i]+"新增无症状")
    print(quDict)
    zqzList = []
    dateList = []
    Frame = np.zeros((len(D), 2*len(qus)+2), dtype=np.int32)
    for i in range(len(D)):
        today = D[i]
        '''today : [
            日期(datetime对象), 
            新增本土新冠肺炎确诊病例, 新增无症状感染者, 
            [[区名, 区新增本土确诊病例, 区新增本土无症状感染者],...]
        ]'''
        dateList.append(today[0])
        Frame[i][0] = today[1]
        Frame[i][1] = today[2]
        for j in range(len(D[i][3])):
            quName, quqz, quwzz = today[3][j][0],today[3][j][1],today[3][j][2]
            if quName in qus:
                quNumber = quDict[quName]
                Frame[i][quNumber*2+2], Frame[i][quNumber*2+3] = quqz, quwzz
        # if D[i][1] != -1 and D[i][2] != -1:
        # zqzList.append(D[i][1]+D[i][2])
        # print(D[i][1]+D[i][2])
        # dateList.append(D[i][0])
    print(Frame)
    print(dateList)
    #np.savetxt("n.csv", Frame, delimiter=',', fmt="%d")
    # np.savetxt("date.csv", dateList, delimiter=',')
    df = pd.DataFrame(Frame, dateList, head)
    df.to_csv("data.csv", encoding="utf-8")
    
   
    
    
    
    
    # plt.plot(dateList, zqzList)
    # plt.show()
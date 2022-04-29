from tracemalloc import start
from bs4 import BeautifulSoup
import re
import datetime as dt
import matplotlib.pyplot as plt

numbers = '0123456789'

def between(s, leader, trailer):
    try:
        end_of_leader = s.index(leader) + len(leader)
        start_of_trailer = s.index(trailer, end_of_leader)        
        return s[end_of_leader:start_of_trailer]
    except:
        return '-1'

def numbersAfter(s, leader):
    try:
        end_of_leader = s.index(leader) + len(leader)
        start_of_trailer = end_of_leader+1
        while(s[start_of_trailer] in numbers):
            start_of_trailer += 1
        return s[end_of_leader:start_of_trailer]
    except:
        return '-1'

def getData(fileName):
    """_summary_

    Args:
        fileName (_type_): _description_

    Returns:
        [
            日期(datetime对象), 
            新增本土新冠肺炎确诊病例, 新增无症状感染者, 
            [区名, 区新增本土确诊病例, 区新增本土无症状感染者],...
        ]
    """
    with open(fileName, encoding="utf-8") as html:
        bs = BeautifulSoup(html, 'lxml')
        L = []
        dateOKflag = False
        zqz,zwzz = -1,-1
        for span in bs.find_all('span'):
            #print(span.string,end='/')
            if span.string != None and span.string[0] == '市' and '市卫健委' in span.string:
                s = span.string
                #print(s)
                if s.count('（') != 1:
                    zqz, zwzz = numbersAfter(s,'新增本土新冠肺炎确诊病例'), numbersAfter(s,'无症状感染者')
                else:
                    zqz, zwzz = numbersAfter(s,'新增本土新冠肺炎确诊病例'), numbersAfter(s,'无症状感染者')
            if span.string != None and span.string[0] == '2' and '，' in span.string:
                s = span.string
                #print(s)
                if not dateOKflag and s[0] != '市':
                    dates = between(s, '', '，')
                    date = dt.date(int(between(dates,'','年')), int(between(dates,'年','月')), int(between(dates,'月','日')))
                    dateOKflag = True
                ls = s.split("，")
                try:
                    qus, qzs, wzzs = ls[1], ls[1], ls[2]
                except IndexError:
                    L.append(["?", -1, -1])
                    continue
                # ?区
                qu ='0' if '无' in qus else between(qus, '','新增')
                # print(qu)
                # 新增确诊
                qz = '0' if '无' in qzs else between(qzs, '新增', '例')
                # print(qz)
                # 新增本土无症状感染者
                if '、' in qzs:
                    wzz = between(qzs, '、', '例')
                else:
                    try:
                        wzz = between(wzzs, '新增', '例')
                    except:
                        wzz = between(wzzs, '', '例')
                # print(wzz)
                try:
                    int(qz)
                except:
                    qz = -1
                try:
                    int(wzz)
                except:
                    wzz = -1
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
    zqzList = []
    dateList = []
    for i in range(len(D)):
        if D[i][1] != -1 and D[i][2] != -1:
            zqzList.append(D[i][1]+D[i][2])
            print(D[i][1]+D[i][2])
            dateList.append(D[i][0])
    plt.plot(dateList, zqzList)
    plt.show()
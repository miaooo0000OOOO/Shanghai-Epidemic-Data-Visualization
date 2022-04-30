import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("data2.xlsx")


qzL,wzzL, dateL = [], [], []
QuName = '徐汇区'
QuName = ''
QuName = input("输入区名：(回车代表全上海)")
for i in  range(len(df[QuName+'新增本土确诊'])):
    qz, wzz, date = df[QuName+'新增本土确诊'][i], df[QuName+'新增无症状'][i], df['日期'][i]
    if qz in [0,-1] or wzz in [0,-1]:
        continue
    else:
        qzL.append(qz)
        wzzL.append(wzz)
        dateL.append(date)
print(qzL, wzzL)
plt.plot(dateL, qzL)
plt.plot(dateL, wzzL)
plt.xticks(rotation=15)
plt.show()

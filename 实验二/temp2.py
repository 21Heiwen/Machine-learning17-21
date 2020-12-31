import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler


#获取实验1数据矩阵
data = pd.read_csv('./Completed.csv')
data = data.drop(['Name', 'City', 'Gender', 'Height', 'Constitution'], axis = 1)

#制作散点图
x = data['C1']
y = data['Constitution_int']
plt.yticks([4, 3, 2, 1], ['$excellent$', '$good$', '$general$', '$bad$'])
plt.scatter(x, y)
plt.show()

#制作直方图
plt.xticks(range(60, 101)[::5])
plt.hist(x, histtype = 'bar', bins = [60, 65, 70, 75, 80, 85, 90, 95, 100])
plt.show()

#归一化的数据矩阵
data_z = pd.DataFrame()
data_z.loc[:, 'C1'] = (data['C1'] - data['C1'].min()) / (data['C1'].max() - data['C1'].min())
data_z.loc[:, 'C2'] = (data['C2'] - data['C2'].min()) / (data['C2'].max() - data['C2'].min())
data_z.loc[:, 'C3'] = (data['C3'] - data['C3'].min()) / (data['C3'].max() - data['C3'].min())
data_z.loc[:, 'C4'] = (data['C4'] - data['C4'].min()) / (data['C4'].max() - data['C4'].min())
data_z.loc[:, 'C5'] = (data['C5'] - data['C5'].min()) / (data['C5'].max() - data['C5'].min())
data_z.loc[:, 'C6'] = (data['C6'] - data['C6'].min()) / (data['C6'].max() - data['C6'].min())
data_z.loc[:, 'C7'] = (data['C7'] - data['C7'].min()) / (data['C7'].max() - data['C7'].min())
data_z.loc[:, 'C8'] = (data['C8'] - data['C8'].min()) / (data['C8'].max() - data['C8'].min())
data_z.loc[:, 'C9'] = (data['C9'] - data['C9'].min()) / (data['C9'].max() - data['C9'].min())
data_z.loc[:, 'Constitution'] = (data['Constitution_int'] - data['Constitution_int'].min()) / (data['Constitution_int'].max() - data['Constitution_int'].min())
data_z

#混淆矩阵
data_corr = pd.DataFrame(np.corrcoef(data_z))
data_corr

x_train, x_test, y_train, y_test = train_test_split(data['C1'], data['Constitution_int'], test_size = 0.2)

#用归一化预处理
tra = MinMaxScaler()
x_train = tra.fit_transform(pd.DataFrame(x_train))
x_test = tra.fit_transform(pd.DataFrame(x_test))
es = KNeighborsClassifier(n_neighbors = 5)
es.fit(x_train, y_train.astype('int'))

#实际与预测结果相比较
print(es.predict(x_test))
print(y_test.astype(int))
print(es.score(x_test, y_test))

#将相关矩阵绝对值化
data_corr_abs = abs(data_corr)
data_corr_abs.loc[:, 'ID'] = data['ID']
data_corr_abs

N_id = []
n = data['ID'].count()
for i in range(0, n) :
    N_id.append(data_corr_abs.sort_values(by = i, ascending = False)['ID'][1:4])

#100x3的矩阵
np.savetxt("./实验数据/Corr_ID.txt", N_id, fmt = '%s', delimiter = '\t')
pd.DataFrame(np.loadtxt("./实验数据/Corr_ID.txt", dtype = str, encoding = 'UTF-8'), columns = ['i1', 'i2', 'i3'])

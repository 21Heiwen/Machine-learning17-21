import pandas as pd
import numpy as np
import linecache
import pymysql

#读TXT
data1 = linecache.getline(r'.F:\data.txt', 1).strip('\n').split(',')
data2 = np.loadtxt(r'.F:\data.txt', dtype = str, delimiter = ',', skiprows = 1, encoding = 'UTF-8')
data_txt = pd.DataFrame(data2, columns = data1).drop(['C10'], axis = 1)
#用前一个数据进行填充
data_txt = data_txt.replace(to_replace = "", value = np.NaN)
data_txt = data_txt.fillna(method = 'pad')

#读表格
data = pd.read_excel(".F:/data.xlsx")
#删去C10列
data = data.drop(['C10'], axis = 1)
#用前一个数据进行填充
data = data.fillna(method = 'pad')

#连接数据库
conn = pymysql.connect(host = 'localhost', user = 'root', password = '10613156', database = 'test', charset = "utf8")
cursor = conn.cursor()

#创建student表
sql = "CREATE TABLE Student(ID   int,Name  varchar(20) ,City   varchar(10),Gender   varchar(10), Height float,C1 float,C2 float,C3 float,C4 float,C5 float,C6 float,C7 float,C8 float,C9 float,Constitution varchar(10));"
cursor.execute(sql)
conn.commit()
n = data['ID'].count()
for i in range(0, n) :
	sql = "insert into student values(%d,'%s','%s','%s',%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,'%s');" % (data.iloc[i][0], data.iloc[i][1], data.iloc[i][2], data.iloc[i][3], data.iloc[i][4], data.iloc[i][5], data.iloc[i][6], data.iloc[i][7], data.iloc[i][8], data.iloc[i][9], data.iloc[i][10], data.iloc[i][11], data.iloc[i][12], data.iloc[i][13], data.iloc[i][14])
	cursor.execute(sql)
conn.commit()
sql_1 = "select * from student"
data_db = pd.read_sql(sql_1, conn)

#类型转换一致
data_txt.loc[:, 'ID'] = data_txt['ID'].astype(int)
data_txt.loc[:, 'C1'] = data_txt['C1'].astype(int)
data_txt.loc[:, 'C2'] = data_txt['C2'].astype(int)
data_txt.loc[:, 'C3'] = data_txt['C3'].astype(int)
data_txt.loc[:, 'C4'] = data_txt['C4'].astype(int)
data_txt.loc[:, 'C5'] = data_txt['C5'].astype(int)
data_txt.loc[:, 'C6'] = data_txt['C6'].astype(int)
data_txt.loc[:, 'C7'] = data_txt['C7'].astype(int)
data_txt.loc[:, 'C8'] = data_txt['C8'].astype(int)
data_txt.loc[:, 'C9'] = data_txt['C9'].astype(int)

data_db.loc[:, 'C1'] = data_db['C1'].astype(int)
data_db.loc[:, 'C2'] = data_db['C2'].astype(int)
data_db.loc[:, 'C3'] = data_db['C3'].astype(int)
data_db.loc[:, 'C4'] = data_db['C4'].astype(int)
data_db.loc[:, 'C5'] = data_db['C5'].astype(int)
data_db.loc[:, 'C6'] = data_db['C6'].astype(int)
data_db.loc[:, 'C7'] = data_db['C7'].astype(int)
data_db.loc[:, 'C8'] = data_db['C8'].astype(int)
data_db.loc[:, 'C9'] = data_db['C9'].astype(int)
data_db.loc[:, 'Height'] = data_db['Height'].astype(float)

#单位转换一致
data_db.loc[:, 'ID'] = data_db['ID'].astype(int) + 202000
data_txt.loc[data_txt.Gender == 'male', 'Gender'] = 'boy'
data_txt.loc[data_txt.Gender == 'female', 'Gender'] = 'girl'
data_txt.loc[:, 'Height'] = data_txt['Height'].astype(float) * 100

#data1删去C10这个元素
data1.remove('C10')
#合并数据
data = pd.DataFrame(np.vstack((data_db, data_txt)), columns = data1)

#去除冗余
data = data.drop_duplicates(subset = ['ID'])

#合并文件
data.to_csv('./Completed.csv', index = False)

#学生中家乡在Beijing的所有课程的平均成绩。
ts = 0
for i in data['C1']:
    ts = ts + i
t = ts / data['C1'].count()

A1 = []
A1 = data[data['City'] == 'Beijing'].mean()
A1[1:12]

#学生中家乡在广州，课程1在80分以上，且课程9在9分以上的男同学的数量
A2 = data[data['City'] == 'Shenzhen'][data['C1'] >= 80][data['C9'] >= 9][data['Gender'] == 'boy']['ID'].count()
A2

#比较广州和上海两地女生的平均体能测试成绩
data.loc[data.Constitution == 'excellent', 'Constitution_int'] = 4
data.loc[data.Constitution == 'good', 'Constitution_int'] = 3
data.loc[data.Constitution == 'general', 'Constitution_int'] = 2
data.loc[data.Constitution == 'bad', 'Constitution_int'] = 1

print("Guangzhou")
A3_Guangzhou = data[data['City'] == 'Guangzhou']['Constitution_int'].mean()
A3_Guangzhou

print("Shanghai")
A3_Shanghai = data[data['City'] == 'Shanghai']['Constitution_int'].mean()
A3_Shanghai

#计算相关系数
vs = 0
for i in data['C1']:
    vs = vs + (i - data['C1'].mean())*(i - data['C1'].mean())
var = vs / (data['C1'].count() - 1)

C1_x = data['C1'].mean()#C1平均值
C1_var = data['C1'].var()#C1方差
C1_std = np.sqrt(C1_var)#C1标准差
Con_x = data['Constitution_int'].mean()
Con_var = data['Constitution_int'].var()
Con_std = np.sqrt(Con_var)

t1 = []
for i in data['C1']:
    t1.append(i)
t2 = []
for i in data['Constitution_int'] :
    t2.append(i)
t3 = np.multiply(t1, t2)

t = pd.DataFrame(t3, columns = ['C1_Constitution'])
cov = t['C1_Constitution'].mean() - C1_x * Con_x

cor = cov / (C1_std*Con_std)
np.abs(cor)




#%%
import pymysql
import pandas as pd
import numpy as np

#连接数据库
conn = pymysql.connect(
    host = "127.0.0.1",
    user = "root",
    password= "Root@123456",
    port = 3306,
    database = "mobilemanager",
    charset='utf8'
)

#创建游标
cur = conn.cursor()


#创建数据表
# sql_2 = "create table android_test3(id char(99) PRIMARY KEY,brand char(99),device_name char(99),model char(99),Android_version char(99),Android_version_c char(99),cpu_brand char(99),cpu_model char(99),cpu_Frequency char(99),cpu_core_num char(99),RAM char(99),resolution char(99),screen_type char(99),size char(99),screen_ratio char(99),ROM char(99),state char(99),wanmei_office char(99),MAC_addr char(99),asset_number char(99),QA_compatible char(99),google_able char(99),oversea_sold char(99),Internal_reference char(99),cpu_architecture char(99),cpu_hardware char(99),cpu_model_num char(99),cpu_architecture_detailed char(99),armeabi char(99),armeabi_v7a char(99),arm64_v8a char(99),mips char(99),mips64 char(99),x86 char(99),x86_64 char(99),GPU_brand char(99),GPU_Renderer char(99),GPU_ver char(99),classify char(99),Photographed char(99),archived char(99))character set utf8;"
# cur.execute(sql_2)


#读取源数据
data = pd.read_excel('D:\\gitcode\\dev\\atuotest\\web_scr\\data.xlsx').values
# for i in range(len(data)):


#写入数据

# cur = conn.cursor()
# for i in range(1,len(data)):
#     if pd.isnull(data[i][0]):
#         # print("a")
#         continue
#     line = "("+'\"'+data[i][0]+'\"'
#     for j in [1,2,3,4,6,7,8,9,10,35,36,11,12,13,15,17,18,19]:
#         if pd.isnull(data[i][j]):
#             line += ","
#             line += "\"\""
#         else:
#             line += ","
#             line += ('\"'+str(data[i][j])+'\"').replace("\n","\\n")
#     line += ",\"可用\",0,0,0)"
#     print(line)
#     sql = "replace into catalog_device(deviceId,brand,name,deviceModel,OSVersion,cpuBrand,cpuModel,cpuFrequency,cpuCoreNum,RAM,gpuBrand,gpuModel,resolution,screenType,size,ROM,wanmeiOffice,MACAddr,assetNumber,status,onlyOne_cn,onlyOne_oversea,onlyOne_iOS) VALUES{line};".format(line=line)
#     # sql = "replace into catalog_device(deviceId,brand,name,deviceModel,OSVersion,cpuBrand,cpuModel,cpuFrequency,cpuCoreNum,RAM,gpuBrand,gpuModel,resolution,screenType,size,ROM,wanmeiOffice,MACAddr,assetNumber,status,onlyOne,onlyOne_oversea,genre_id) VALUES{line};".format(line=line)

#     # print(line)
#     cur.execute(sql)
#     conn.commit()
# conn.close()


cur = conn.cursor()
for i in range(1,len(data)):
    if pd.isnull(data[i][0]):
        # print("a")
        continue
    line = "("+'\"'+data[i][0]+'\"'
    for j in [1,2,3,5,6,7,8,9,23,24,10,11,12,14,16,18,19]:
        if pd.isnull(data[i][j]):
            line += ","
            line += "\"\""
        else:
            line += ","
            line += ('\"'+str(data[i][j])+'\"').replace("\n","\\n")
    line += ",\"可用\",0,0,0)"
    print(line)
    sql = "replace into catalog_device(deviceId,brand,name,OSVersion,cpuBrand,cpuModel,cpuFrequency,cpuCoreNum,RAM,gpuBrand,gpuModel,resolution,screenType,size,ROM,wanmeiOffice,MACAddr,assetNumber,status,onlyOne_cn,onlyOne_oversea,onlyOne_iOS) VALUES{line};".format(line=line)
    # sql = "replace into catalog_device(deviceId,brand,name,deviceModel,OSVersion,cpuBrand,cpuModel,cpuFrequency,cpuCoreNum,RAM,gpuBrand,gpuModel,resolution,screenType,size,ROM,wanmeiOffice,MACAddr,assetNumber,status,onlyOne,onlyOne_oversea,genre_id) VALUES{line};".format(line=line)

    # print(line)
    cur.execute(sql)
    conn.commit()
conn.close()

    


# %%

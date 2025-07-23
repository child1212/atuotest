#%%
import pandas as pd

item_excel = pd.read_excel("D:\\million\\GitPro\\VersionCopy_Branches\\TW_VersionCopy_OB4\\item.xlsx")

item_table = item_excel.values

item_dict = {}

length = len(item_table)

for i in range(4,length):
    if item_table[i][0] in item_dict.keys():
        print(item_table[i][0]+"is 重复了！")
    else:
        item_dict[item_table[i][0]] = item_table[i][2]

while True:
    itemid = int(input("输入itemid："))
    print(item_dict[itemid])





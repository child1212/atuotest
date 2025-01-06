#%%
import pandas as pd
import re


text_t = pd.read_excel("D:\\projectM\\Shared\\ExcelFiles\\text.xlsx")
text = text_t.values

def check_c(word):
    wo = re.sub(r"(<.*?>|boss|Boss|BOSS)","",str(word)).replace("\\n","").replace("\n","")
    res = re.findall(r"[a-zA-Z]+",wo)
    if len(res):
        return wo
    else:
        return 0


result = open("D:\\gitcode\\dev\\atuotest\\text\\result.txt","w")

for i in range(2,len(text_t)-1):
    if pd.isnull(text[i][2]):
        pass
    elif check_c(text[i][2]):
        result.write(str(text[i][1])+";"+check_c(text[i][2])+"\n")
        

result.close()
#%%

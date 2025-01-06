#%%
#删除玩家

uid = "66eb8d1c8f870ed0e21c567b"
url = "http://game003aud.happyhorse.top:37576/gm/removeUser?uid={uid}".format(uid=uid)

print(url)

# %%
#修改玩家等级
uid = "66eb8d1c8f870ed0e21c567b"
level = 20
url = "http://game003aud.happyhorse.top:37576/gm/updateUser?uid={uid}&level={level}".format(uid=uid,level=level)
print(url)



# %%
uid = "66eb8d1c8f870ed0e21c567b"

# 1. items: 1:金币,2:经验,20504:树枝,20601:挂机金币收益双倍,20602:挂机经验收益双倍,20603:锤蛋价格-50%,20604:挂机生产时间-50%
items = ''

ite = {
    1:10000,
    2:10000,
    20504:1,
    20601:1,
    20602:1,
    20603:1,
    20604:1
}

for item in ite.keys():
    if len(items) > 0:
        items +=","
    items += str(item)+":"+str(ite[item])


url = "http://game003aud.happyhorse.top:37576/gm/sendItem?uid={uid}&items={items}".format(uid=uid,items=items)

print(url)
# %%

#%%
import pandas as pd
import pymysql

db= pymysql.connect(
    host = "127.0.0.1",
    user = "root",
    password= "Root@123456",
    port = 3306,
    database = "mobileManager",
    charset='utf8'
)

tableHead = ["设备编号","品牌","终端设备","设备型号","当前版本","子版本","CPU品牌","CPU型号","CPU主频","CPU核心数","RAM","分辨率","全面屏","尺寸","屏占比","ROM","设备状态","wanmeioffice","MAC地址","资产编号","QA兼容","可登录谷歌","海外设备","内参","CPU架构","CPUHardware","CPU型号-详细","CPU架构-详细","armeabi","armeabi-v7a","arm64-v8a","mips","mips64","x86","x86_64","GPU品牌","GPU渲染器","GPU版本","设备分类","已拍照","已归档"]

datile={"设备编号":[],"品牌":[],"终端设备":[],"设备型号":[],"当前版本":[],"子版本":[],"CPU品牌":[],"CPU型号":[],"CPU主频":[],"CPU核心数":[],"RAM":[],"分辨率":[],"全面屏":[],"尺寸":[],"屏占比":[],"ROM":[],"设备状态":[],"wanmeioffice":[],"MAC地址":[],"资产编号":[],"QA兼容":[],"可登录谷歌":[],"海外设备":[],"内参":[],"CPU架构":[],"CPUHardware":[],"CPU型号-详细":[],"CPU架构-详细":[],"armeabi":[],"armeabi-v7a":[],"arm64-v8a":[],"mips":[],"mips64":[],"x86":[],"x86_64":[],"GPU品牌":[],"GPU渲染器":[],"GPU版本":[],"设备分类":[],"已拍照":[],"已归档":[]}

cur = db.cursor()

#展示所有内容
sql = '''select * from android_test3'''

#搜索内容
search = ['小米','红米',"note","借出"]#传参

cur.execute(sql)
#搜索数据，保存在datile中
data = cur.fetchall()
if len(search) == 0:
    for line in data:
        for i in range(len(line)):
            datile[tableHead[i]].append(line[i])
else:
    for line in data:
        run = True
        for se in search:
            if se.lower() not in  ",".join(line).lower():
                run = False
                break
        if run:
            for i in range(len(line)):
                datile[tableHead[i]].append(line[i])
             



#数据转dataframe
df = pd.DataFrame(datile)

#dataframe转html
html_table = df.to_html(index=False)

#html格式化
text_html = "<!DOCTYPE html><html lang=\'en\'><head><meta charset=\'utf-8\'><title>兼容设备管理</title><meta name=\"description\" content=\"国内兼容设备\"><meta name=\"keywords\" content=\"国内兼容设备\"></head><body><div><style>* {box-sizing: border-box;}body {margin: 0;}* {box-sizing: border-box;}body {margin-top: 0px;margin-right: 0px;margin-bottom: 0px;margin-left: 0px;font-family: -apple-system, BlinkMacSystemFont, \"Helvetica Neue\", Helvetica, Roboto, Arial, \"PingFang SC\", \"Hiragino Sans GB\", \"Microsoft Yahei\", \"Microsoft Jhenghei\", sans-serif;}.logo path {pointer-events: none;fill: none;stroke-linecap: round;stroke-width: 7;stroke: rgb(255, 255, 255);}.wechat-group img {max-width: 220px;height: auto;border-top-left-radius: 8px;border-top-right-radius: 8px;border-bottom-right-radius: 8px;border-bottom-left-radius: 8px;margin-top: 0px;margin-right: auto;margin-bottom: 0px;margin-left: auto;width: 100%;}.welcome-img img {width: 100%;}.bg-gradient-primary {border-top-left-radius: 8px;border-top-right-radius: 8px;border-bottom-right-radius: 8px;border-bottom-left-radius: 8px;}.container.py-18.pt-md-14.pb-md-14:active {border: -1px solid #000000;}.display-1.mb-4 {color: #ff0000;}</style><meta charset=\"utf-8\" /><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" /><meta name=\"description\" content=\"a\" /><meta name=\"keywords\" content=\"\" /><meta name=\"author\" content=\"Lapus\" /><title>兼容设备管理</title><link rel=\"preload\" href=\"/static/fonts/Unicons.woff2\" as=\"font\" type=\"font/woff2\" crossorigin=\"\" /><link rel=\"shortcut icon\" href=\"/static/img/favicon.png\" /><link rel=\"stylesheet\" href=\"url_for(static\" ,filename=\"css/plugins.css\" ) /><link rel=\"stylesheet\" href=\"url_for(static\" ,filename=\"css/style.css\" ) /><link rel=\"stylesheet\" href=\"url_for(static\" ,filename=\"css/purple.css\" ) /><link rel=\"preload\" href=\"url_for(static\" ,filename=\"css/thicccboi.css\" ) as=\"style\" /><div class=\"content-wrapper\"><section class=\"wrapper bg-gradient-primary\"><div class=\"row text-center\"><div data-cues=\"zoomIn\" data-group=\"welcome\" data-interval=\"-200\"class=\"col-lg-9 col-xxl-7 mx-auto\"><h2 class=\"display-1 mb-4\">国内兼容设备表</h2><p class=\"lead fs-24 lh-sm px-md-5 px-xl-15 px-xxl-10 mb-7\">测试中心兼容设备查询库</p></div><!-- /column --></div><!-- /.row --><div data-cues=\"slideInDown\" data-group=\"join\" data-delay=\"900\" class=\"d-flex justify-content-center\"><span><a href=\"http://127.0.0.1:5000/cndevices/\"class=\"btn btn-lg btn-primary rounded-pill mx-1\">国内兼容设备</a></span><span><ahref=\"http://127.0.0.1:5000/overseadevices/\"class=\"btn btn-lg btn-outline-primary rounded-pill mx-1\">海外兼容设备</a></span></div><!-- /div --><div data-cue=\"fadeIn\" data-delay=\"1600\" class=\"row mt-12\"><div class=\"col-lg-8 mx-auto\"><figure></figure></div><!-- /column --></div><!-- /.row --></div><!-- /.container --></section><!-- /section --><section class=\"wrapper bg-light\"><div class=\"container\"><!-- /.row --><!--/.row --></div><!-- /.container --><!-- /.overflow-hidden --></section><!-- /section --><!-- /section --></div><!-- /.content-wrapper --><script src=\"js/plugins.js\"></script><script src=\"js/theme.js\"></script></div>"
text_html +=html_table.replace("\\n","<br")+text_html

#保存html文件
with open('templates\\androidtest.html', 'w',encoding="utf8") as f:
    f.write(text_html)
db.close()





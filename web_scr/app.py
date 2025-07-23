from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 处理用户提交的表单数据
        data = request.form['input_data']
        # 将数据存储到本地文件中
        with open('data.txt', 'a') as file:
            file.write(data + '\n')
    return render_template('index_main.html')

@app.route('/cndevices/')
def indexcn():
    return render_template("android.html")

@app.route('/overseadevices/')
def indexoversea():
    return render_template("index1.html")


if __name__ == '__main__':
    app.run()




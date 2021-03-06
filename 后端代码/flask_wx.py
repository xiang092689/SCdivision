
# coding=utf8
import sys
from flask import Flask,render_template,request,json
import pymysql
import time




app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/score',methods=['POST'])
def score():
    upload = str(json.loads(request.values.get("upload")))
    upload_list = upload.split(',')
    print(upload_list)
    conn = pymysql.connect(host='127.0.0.1', user='south_china_division',password='scnu',database='south_china_division',charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    sql = "insert into depot(id,type,price,submission_date) values(%s,%s,%s,%s);"
    # 执行SQL语句
    id1,type1,price,submission_date = upload_list[0],upload_list[1],upload_list[2],time.strftime("%Y%m%d")  # 'AA3002059','C',203.5,time.strftime("%Y%m%d")
    try:
        res=cursor.execute(sql,[id1,type1,price,submission_date])
        # 涉及写操作要注意提交
        conn.commit()
    except pymysql.err.IntegrityError:
        res=2
    finally:
        # 关闭光标对象
        cursor.close()
        # 关闭数据库连接
        conn.close()
    if res==1:
        # print res
        res='数据提交成功'
        return json.dumps(res)
    else:
        if res==2:
            return json.dumps('数据重复')
        # print(res)
        res='数据提交失败'
        return json.dumps(res)
    # return json.dumps(upload)
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80)

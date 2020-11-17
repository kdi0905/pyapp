from flask import Flask,render_template,request,redirect
import pymysql
conn = pymysql.connect(host='kdi0905.kro.kr',port=3306,db='pyapp',user='root',passwd='java1004')
#print(conn)
app = Flask(__name__)

#1. msg목록
@app.route('/',methods=["GET"])
def msg_list():
    cursor = conn.cursor()
    cursor.execute('select msg_id,msg_text From msg')
    msgList=cursor.fetchall()
    print(msgList)
    return render_template('msg_list.html',msgList=msgList)
#2. add_msg.html 폼
@app.route('/add_msg',methods=['GET','POST'])
def add_msg():
    if request.method=='GET':
        return render_template('add_msg.html')
    elif request.method=='POST':
        msg_text= request.form['msg_text']
        # db 입력
        cursor = conn.cursor()
        cursor.execute('INSERT INTO msg(msg_text) VALUES(%s)',[msg_text])
        conn.commit()
        return redirect('/')
#3. 삭제
@app.route('/del_msg',methods=['GET'])
def del_msg():
    msg_id = request.args.get('msg_id')
    #try:
    cursor = conn.cursor()
    cursor.execute('delete from msg where msg_id=%s',[msg_id])
    #except:
    #    conn.rollback()
    #else:
    conn.commit()
    #finally:
    #    conn.close()
    return redirect('/')
#4. 수정
@app.route('/update_msg',methods=['GET','POST'])
def update_msg():
    if request.method == 'GET':
        msg_id = request.args.get('msg_id')
        cursor = conn.cursor()
        cursor.execute('select msg_id, msg_text from msg where msg_id=%s',[msg_id])
        msg = cursor.fetchone()
        print(msg)
        return render_template('update_msg.html',msg=msg)
    
    elif request.method =='POST':
     
        msg_id = request.form['msg_id']
        msg_text = request.form['msg_text']
       
        cursor = conn.cursor()
        cursor.execute('update msg set msg_text=%s where msg_id=%s',[msg_text,msg_id])
        conn.commit()
        return redirect('/')

app.run(host='0.0.0.0',port=8888)
from flask import Flask,render_template,request,session
import mysql.connector as mysql


db = mysql.connect(
    host = 'localhost',
    user = 'root',
    password = 'root',
    database='db'
)

cursor = db.cursor()

app=Flask(__name__)

@app.route('/')
def user_page(): #Handler
    return render_template('index.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')
@app.route('/user')
def result_page(): #Handler
    return render_template('index.html')

@app.route('/collect',methods=['POST']) #Collect the data(Handler)  
def collectData():
    n = request.form['name']
    m = request.form['mobile']
    dt = request.form['time']
    storedata(n,m,dt)
    r = "Data Request Sent"
    return render_template('index.html',res=r)

@app.route('/getdata',methods=['GET','POST'])
def getdatafromdb():
    cursor.execute(" SELECT * FROM SCHEDULE ")
    result = cursor.fetchall()
    data = []
    for i in result:
        data.append(i)
    for i in data:
        print(i)
    return render_template('admin.html',res = data)

@app.route('/collectcheck',methods=['GET','POST'])
def checkstatus():
    mobn = request.form['chknom']
    print(mobn)
    sql = ' SELECT * FROM SCHEDULE WHERE mobile = %s '
    val = (mobn,)
    cursor.execute(sql,val)
    result = cursor.fetchone()
    if result:
        sql = "SELECT * FROM SCHEDULE WHERE mobile = %s"
        val = (mobn,)
        cursor.execute(sql,val)
        r1 = cursor.fetchone()
        mn = r1[3]
        mm = r1[2]
        print(mn)
        if mn == "approved":
            return render_template('index.html',res2 = mn,res3="at",res4=mm)
        else:
            return render_template('index.html',res2 = mn)
    else:
        return render_template('index.html',res2 = "INVALID CREDITIONALS")
    

 
@app.route('/collectmob',methods=['POST']) #Collect the data(Handler)  
def collectData1():
    n = request.form['nom']
    st = request.form['stus']
    if st == 'approve':
        k = 'approved'
        sql = "UPDATE SCHEDULE SET status = %s WHERE mobile = %s"
        val = (k,n)
        cursor.execute(sql,val)
        db.commit()
        return render_template('admin.html',res1=k)
    elif st == 'reject':
        kn = 'rejected'
        sql = "UPDATE SCHEDULE SET status = %s WHERE MOBILE = %s"
        val = (kn,n)
        cursor.execute(sql,val)
        db.commit()
        return render_template('admin.html',res1=kn)
    else:
        dt = request.form['time']
        k = 'approved'
        sql = "UPDATE SCHEDULE SET status = %s WHERE mobile = %s"
        val = (k,n)
        cursor.execute(sql,val)
        db.commit()
        sql = "UPDATE SCHEDULE SET time  = %s WHERE MOBILE = %s"
        val = (dt,n)
        cursor.execute(sql,val)
        db.commit()
        return render_template('admin.html',res2 = k)

        
def storedata(name,mobile,time): #Private function not a handler
    sql = "INSERT INTO SCHEDULE (name,mobile,time) VALUES (%s,%s,%s)"
    val = (name,mobile,time)
    cursor.execute(sql,val)
    db.commit()
    return

if __name__=="__main__":

    app.run(debug=True) 
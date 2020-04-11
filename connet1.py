from flask import Flask, render_template, request
import sqlite3 as sql
import time
from waitress import serve
from flask_compress import Compress
app = Flask(__name__)
#COMPRESS_MIMETYPES=['text/html', 'text/css', 'application/json']
#COMPRESS_LEVEL=6
#COMPRESS_MIN_SIZE=500
#Compress(app)


@app.route('/')
def home():
    return render_template('home.html')
    #return ' <html lang="en"><head><meta charset="UTF-8"><title>Home</title></head><body><a href="/">add new record</a><br><a href="/">Show lists</a></body></html> '


@app.route('/student')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['GET', 'POST'])
def addrec():
    if request.method == 'POST':
        try:
            Id = request.form['Id']
            nm = request.form['nm']


            with sql.connect("student.db") as con:
                cur = con.cursor()
                #cur.execute("CREATE TABLE STUDENT (Id INTEGER, Name TEXT)")
                cur.execute("INSERT INTO STUDENT(Id,Name) VALUES (?,?)", (Id, nm))

            con.commit()
            msg = "Record added successfully"
        except Exception as msg1:
            con.rollback()
            #msg = "error in inserting"
            msg=msg1
        finally:
            return render_template("result.html", msg=msg)

            con.close()


@app.route('/list')
def list():
    con = sql.connect('student.db')
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM STUDENT")

    rows = cur.fetchall()
    return render_template('list.html', rows=rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")

@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    Id = request.form["Id"]
    with sql.connect('student.db') as con:
        try:
            cur = con.cursor()
            #n=cur.execute("SELECT * FROM TABLE WHERE Id - ?",Id)
            #msg=n
            cur.execute("delete from STUDENT where Id = ?",Id)
            msg = "record successfully deleted"
            con.commit()
        except Exception as msg1:
            msg = msg1
        finally:
            return render_template("deleterecord.html",msg = msg)

            #con.close()
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    #app.jinja_env.cache={}
     #serve(app, host = '0.0.0.0', threads=100, port = 8000)
    #time.sleep(1)
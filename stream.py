import cv2
import numpy as np
import os #To handle directories 
from PIL import Image #Pillow lib for handling images 
from flask import Flask, render_template, Response, stream_with_context, request
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
import datetime


app = Flask('__name__')
labels = ["akhil","nikhil"] 

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face-trainner.yml")

cap = cv2.VideoCapture(0) #Get vidoe feed from the Camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)



    
def video_stream():
    cur = "js"
    # schedule the function to run every 2 seconds
    count = 0
    while True:
        count = count + 1
        
        if count > 100:
            cur = "ls"
            count = 0
            
            print("counter reset")
            
        ret, img = cap.read()
        gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert Video frame to Greyscale
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5) #Recog. faces
        current_date = datetime.date.today()
        current_time = datetime.datetime.now().time()
        
        for (x, y, w, h) in faces:
            
            roi_gray = gray[y:y+h, x:x+w] #Convert Face to greyscale 
            id_, conf = recognizer.predict(roi_gray) #recognize the Face
            
            if conf>=20 and conf<= 80:
                font = cv2.FONT_HERSHEY_SIMPLEX #Font style for the name 
                name = labels[id_] #Get the name from the List using ID number 
                cv2.putText(img, str(int(conf)), (x,y), font, 1, (0,0,255), 2)
                cv2.putText(img, name, (x,y+50), font, 1, (0,0,255), 2)
                
                if cur is not name:
                    add_user(name , str(current_time) , str(current_date))
                    cur = name
                
                
            else:
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, "unknon", (x,y+5), font, 1, (0,0,255), 2)
                game = "unknown"
                
                if cur is not game:
                    
                    add_user(game , str(current_time) , str(current_date))
                    cur = "unknown"
          
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            
                
        ret, buffer = cv2.imencode('.jpeg', img)
        frame_with_boxes_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_with_boxes_bytes + b'\r\n')
        
        
@app.route('/')
def camera():
    return render_template('camera.html')   
                    
@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(video_stream()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/dashboard')
def dashboard():
    con=sql.connect("db_web.db")
    con.row_factory=sql.Row
    cur=con.cursor() 
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template("dashboard.html",datas=data)

def add_user(name , date ,time ):
    con=sql.connect("db_web.db")
    cur=con.cursor()
    cur.execute("insert into users(UNAME,UTIME,UDATE) values (?,?,?)",(name,date,time))
    con.commit()
    
@app.route("/delete_user/")
def delete_user():
    con = sql.connect("db_web.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE ROWID IN (SELECT ROWID FROM users LIMIT 2)")
    con.commit()
    flash('First 10 users deleted', 'warning')
    return redirect(url_for("dashboard"))

@app.route("/delete_all/")
def delete_all():
    con = sql.connect("db_web.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users")
    con.commit()
    flash('All users deleted', 'warning')
    return redirect(url_for("dashboard"))
    

if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)

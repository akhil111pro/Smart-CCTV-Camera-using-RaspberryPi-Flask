import cv2
import os

video=cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

facedetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

count=0

nameID=str(input("Enter Your Name: ")).lower()

path='images/'+nameID

isExist = os.path.exists(path)

if isExist:
	print("Name Already Taken")
	nameID=str(input("Enter Your Name Again: "))
else:
	os.makedirs(path)

while True:
	ret,frame=video.read()
	#frame = cv2.flip(frame, 0)
	faces=facedetect.detectMultiScale(frame,1.3, 5)
	for x,y,w,h in faces:
		count=count+1
		name='./images/'+nameID+'/'+ str(count) + '.jpg'
		print("Creating Images........." +name)
		cv2.imwrite(name, frame)
		cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
	cv2.imshow("WindowFrame", frame)
	cv2.waitKey(1)
	if count>500:
		break
video.release()
cv2.destroyAllWindows()
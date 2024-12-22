#seat belt invigilator
import cv2
import numpy as np
import winsound
import time
from datetime import datetime


count=0
imagecount=0
def Slope(a,b,c,d):
   return (d-b)/(c-a)
vid = cv2.VideoCapture(0)
while(True):
    ret, frame = vid.read()
    vidgray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges=cv2.Canny(vidgray,100,200)
    lines = cv2.HoughLinesP(edges, 1, np.pi/270, 30, maxLineGap = 20,minLineLength = 170)
    if lines is not None:
       for line in lines:
          x1,y1,x2,y2=line[0]
          s=Slope(x1,y1,x2,y2)
          if(((s)>0.7)and((s)<2)):
            print("belt detected")
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),6)
            count=0
            time.sleep(1)
            break
                               
          else:
             print("not detected")
             winsound.Beep(2000,100)
             time.sleep(1)
             count=count+1
             now = datetime.now()
             dt_string = now.strftime("%d_%m_%Y %H_%M_%S")
            
             if((count==15)&(imagecount==0)):
                 print("wear belt")
                 print("",dt_string)
                 image_name="TS07GW8668{}.png".format(dt_string)
                 cv2.imwrite(image_name,frame)
                 count=0   
                 imagecount=1  
             break
            
                
    cv2.imshow('frame',frame)     
    if cv2.waitKey(1) & 0xFF == ord('q'):
       break  
vid.release()
cv2.destroyAllWindows()
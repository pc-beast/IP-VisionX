import cv2 
import numpy as np 
import imutils 
from PIL import Image
#import pyfirmata
import serial


port='port name'
#bluetooth=serial.Serial(port, 9600)
#bluetooth.flushInput()


def perspective_bird():
    pts1 = np.float32([[430,320],[590,320],[120,450],[850,450]])

    pts2= np.float32([[0,0],[999,0],[0,666],[999,666]])

    per_trans=cv2.getPerspectiveTransform(pts1,pts2)

    perspective = cv2.warpPerspective(frame,per_trans,(999,666))
    return perspective

def houghc():
    global circles
    flag = 1
    l_b = np.array([30,50,30])
    u_b = np.array([190,200,190])

    mask = cv2.inRange(frame, l_b, u_b)
    kernal=np.ones((1,1),np.uint8)

    mask=cv2.dilate(mask,kernal,iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('mask', mask)
    #cv2.imshow('result',res)

    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 200, param1=100, param2=5, minRadius=56, maxRadius=65)
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Draw outer circle
            cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw inner circle
            cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
    #if len(circles[0,:])==0:
    #    flag = 0

    return frame,flag

def hought():
    global frame
    #global i
    frame = cv2.medianBlur(frame,5)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("check",frame)
    #cv2.waitKey(0)
    global circles
###
#HughCircles Detection TEST  
    circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,50,
                          param1=50,param2=30,minRadius=54,maxRadius=70) 
    circles = np.uint16(np.around(circles))
    ret,thresh = cv2.threshold(gray,127,255,0)
    

 
# calculate moments of binary image
    M = cv2.moments(thresh)
 
# calculate x,y coordinate of center
    if(M["m00"]!=0):
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    if circles.all != None:
        for i in circles[0,:]:
        # draw the outer circle
            cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
            cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
        #print(i[0])
def line_angle(thresh,frame):
    global ar
    ar=[]
    #frame = cv2.medianBlur(frame,5)
    global theta2
    #print(frame.shape)
    y,x,_=frame.shape
    x=int(x/2)
    
    theta2=0
    
    #M = cv2.moments(thresh)
 
# calculate x,y coordinate of center
    
    if circles.all != None:
        for i in circles[0,:]:
        # draw the outer circle
            
            #cv2.line(frame,(i[0],i[1]),(cX,cY),(0,0,0),2)
            ar.append(i[1])
            #ar[0].sort()
            ar.sort()
            
            l=str(len(ar))
            theta1=np.arctan((i[0]-x)/(i[1]-y))*180/np.pi
            #cv2.putText(frame,l,(50,50),cv2.FONT_HERSHEY_PLAIN,1,(255,0,0),4)
            cv2.line(frame,(x,y),(x,int(y/2)),(0,0,0),2)
            #if ar[0]==i[1]:
                 #cv2.line(frame,(i[0],i[1]),(x,y),(0,255,0),2)
        
                 


           

            
            #theta1 = np.arctan((thiselem[1]-cY)/(thiselem[0]-cX))
            #theta1*=180/np.pi

            
            #print(theta1)
            #frame=cv2.putText(frame,str(theta1),(thiselem[0],thiselem[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
            if theta1>0:
                frame=cv2.putText(frame,'Turn Left',(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,50,255),2)
            else:
                
                frame=cv2.putText(frame,'Turn Right',(10,20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,50,255),2)
        print(ar)
        for i in circles[0,:]:
            if i[1]==ar[len(ar)-1]:
                cv2.line(frame,(i[0],i[1]),(x,y),(0,255,0),2)
                
            #if len(circles)>1:
            #    nextelem = circles[circles.index(i)-len(li)+1]
            #    theta2=np.arctan((cY-nextelem[1])/(cX-nextelem[0]))
            #    theta2=theta2*180/np.pi
            #    print(theta2) 
            #    frame=cv2.putText(frame,str(theta2),(nextelem[0],nextelem[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0))
        
        
    
    def barcode():
        img=cv.imread("opencv/barcode/bcode.jpg")
        height,width,_=img.shape
        im=Image.open('opencv/barcode/bcode.jpg')
        ppi=im.info['dpi']
        print(ppi[0])


        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #s=cv.Sobel(gray,cv.CV_64f,1,0)
        #cv.imshow("sobel",s)

        a=0
        d=[]
        #can=cv.Canny(gray,100,200)
        edges = cv2.Canny(gray,50,150,apertureSize = 3)
        minLineLength = 100
        maxLineGap = 70
        lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

        for x1,y1,x2,y2 in lines[:,0]:
            
            d.append(x1)
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

        d.sort()
        l=len(d)
        ba=[]
        for i in range(0,l-1):
            if(i%2==0):
                ba.append(d[i+1]-d[i])
        print(ba)

        #   for i in range(0,len(ba)):
        #      ba[i]=(ba[i]/ppi[0])*25.4
        #  print(ba)
        bav=0
        for i in range(0,len(ba)):
            bav=bav+ba[i]
            bav=bav/4
            print(bav)

        s=""
        for i in range(0,len(ba)):
            if ba[i]<=bav:
                ba[i]=0
            if bav< ba[i]:
                ba[i]=1
            s=s+str(ba[i])
        print(s) 






            


        #cv.imwrite('opencv/barcode/houghlines5.jpg',img)
        #i1=cv.imread('opencv/barcode/houghlines5.jpg')
        cv2.putText(frame,s,(int(width/2),int(height/2)),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
        #cv.imshow("Edges",i1)



        #cv.imshow("canny",can)
def shape():
    def nothing(x):
        pass
    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L-H","Trackbars",57,180,nothing)
    cv2.createTrackbar("L-S","Trackbars",0,255,nothing)
    cv2.createTrackbar("L-V","Trackbars",136,255,nothing)
    cv2.createTrackbar("U-H","Trackbars",156,180,nothing)
    cv2.createTrackbar("U-S","Trackbars",111,255,nothing)
    cv2.createTrackbar("U-V","Trackbars",255,255,nothing)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lh=cv2.getTrackbarPos("L-H","Trackbars")
    ls=cv2.getTrackbarPos("L-S","Trackbars")
    lv=cv2.getTrackbarPos("L-V","Trackbars")
    uh=cv2.getTrackbarPos("U-H","Trackbars")
    us=cv2.getTrackbarPos("U-S","Trackbars")
    uv=cv2.getTrackbarPos("U-V","Trackbars")
    lower_black=np.array([lh,ls,lv])
    upper_black=np.array([uh,us,uv])

    mask=cv2.inRange(hsv,lower_black,upper_black)
    kernel=np.ones((5,5),np.uint8)

    mask=cv2.erode(mask,kernel)




    #contour detection


    contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        area=cv2.contourArea(cnt)
        approx=cv2.approxPolyDP(cnt,0.05*cv2.arcLength(cnt,True),True)
        x=approx.ravel()[0]
        y=approx.ravel()[1]
        if area>0:
            cv2.drawContours(frame,[approx],0,(0,255,0))

            if len(approx) == 3:
                cv2.putText(frame, "Triangle", (4,4), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 0))
                
            elif len(approx) == 4:
                
                cv2.putText(frame, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255))
                
            else : cv2.putText(frame, "Circle", (200,200), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255))
    cv2.imshow("mask",mask)
    cv2.imshow("Kernel",kernel)

def main():
    #cap=cv2.VideoCapture("opencv/visionX/r1_toptrack.mp4")
    cap=cv2.VideoCapture("git_workspace/opencv/visionX/visionX/r1_toptrack.mp4")
    global frame
    #frame=cv2.imread("opencv/visionX/r1_track_p1.png")
    #ret=True
    while(True):
        ret,frame=cap.read()
        frame=cv2.transpose(frame)
        frame=cv2.flip(frame,+1)

        if ret==True:
            #frame=perspective_bird()
            #frame,flag=houghc()
            shape()
            hought()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(gray,127,255,0)
            line_angle(thresh,frame)
            
            cv2.imshow("Video",frame)
            
            key=cv2.waitKey(1)
            if key== 27:
                break

    cap.release()
    cv2.destroyAllWindows()
main()
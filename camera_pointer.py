import cv2 as cv
import numpy as np

def nothing(x):
    pass

cap = cv.VideoCapture(0)
cv.namedWindow('Color Detectors')
cv.createTrackbar('LH','Color Detectors' , 0, 179, nothing)
cv.createTrackbar('LS','Color Detectors' , 0, 255, nothing)
cv.createTrackbar('LV','Color Detectors' , 0, 255, nothing)
cv.createTrackbar('UH','Color Detectors' , 179, 179, nothing)
cv.createTrackbar('US','Color Detectors' , 255, 255, nothing)
cv.createTrackbar('UV','Color Detectors' , 255, 225, nothing)

# colors
white = (255,255,255)
black = (0,0,0)
gray = (122,122,122)

colors = [(255,0,0) , (0,255,0) , (0,0,255) , (0,255,255)]
colorIndex = 0

bPoints= [ ]
gPoints= [ ]
rPoints= [ ]
yPoints= [ ]


paint_window = np.zeros((471 , 636,3) ) + 255
paint_window = cv.rectangle(paint_window, (40,1), (140,65), black,2)
paint_window = cv.rectangle(paint_window, (160,1), (255,65), colors[0],-1)
paint_window = cv.rectangle(paint_window, (275,1), (370,65), colors[1],-1)
paint_window = cv.rectangle(paint_window, (390,1), (485,65), colors[2],-1)
paint_window = cv.rectangle(paint_window, (505,1), (600,65), colors[3],-1)
cv.putText(paint_window, 'Clear all', (49,33), cv.FONT_HERSHEY_SIMPLEX, 0.5, black,2)
cv.putText(paint_window, 'BLUE', (185,33),cv.FONT_HERSHEY_SIMPLEX, 0.5, white,2, cv.LINE_AA)
cv.putText(paint_window, 'GREEN', (298,33), cv.FONT_HERSHEY_SIMPLEX, 0.5,  white,2, cv.LINE_AA)
cv.putText(paint_window, 'RED', (428,33), cv.FONT_HERSHEY_SIMPLEX, 0.5,  white,2, cv.LINE_AA)
cv.putText(paint_window, 'YELLOW', (528,33), cv.FONT_HERSHEY_SIMPLEX, 0.5,  white,2, cv.LINE_AA)






while True :
   ret ,frame  = cap.read()
   if ret == True :
       frame = cv.flip(frame, 1)
       hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
       l_h = cv.getTrackbarPos('LH', 'Color Detectors')
       l_s = cv.getTrackbarPos('LS', 'Color Detectors')
       l_v = cv.getTrackbarPos('LV', 'Color Detectors')
       u_h = cv.getTrackbarPos('UH', 'Color Detectors')
       u_s = cv.getTrackbarPos('US', 'Color Detectors')
       u_v = cv.getTrackbarPos('UV', 'Color Detectors')
       upper_hsv = np.array([u_h ,u_s, u_v])
       lower_hsv = np.array([l_h , l_s, l_v])
       # buttons
       frame = cv.rectangle(frame, (40,1), (140,65), black,-1)
       frame = cv.rectangle(frame, (160,1), (255,65), colors[0],-1)
       frame = cv.rectangle(frame, (275,1), (370,65), colors[1],-1)
       frame = cv.rectangle(frame, (390,1), (485,65), colors[2],-1)
       frame = cv.rectangle(frame, (505,1), (600,65), colors[3],-1)
       cv.putText(frame, 'Clear all', (49,33), cv.FONT_HERSHEY_SIMPLEX, 0.5, white,2)
       cv.putText(frame, 'BLUE', (185,33),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255),2, cv.LINE_AA)
       cv.putText(frame, 'GREEN', (298,33), cv.FONT_HERSHEY_SIMPLEX, 0.5,  (255, 255, 255),2, cv.LINE_AA)
       cv.putText(frame, 'RED', (428,33), cv.FONT_HERSHEY_SIMPLEX, 0.5,  (255, 255, 255),2, cv.LINE_AA)
       cv.putText(frame, 'YELLOW', (528,33), cv.FONT_HERSHEY_SIMPLEX, 0.5,  (150, 150, 150),2, cv.LINE_AA)


       kernel = np.ones((5,5),np.uint8)
       mask = cv.inRange(hsv, lower_hsv, upper_hsv)
       # to remove noise
       mask = cv.erode(mask, kernel,iterations=1)
       mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel) 
       mask = cv.dilate(mask, kernel,iterations=1)

       cnts ,_ = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
       center = None
       if len(cnts) > 0 :
        cnt = sorted(cnts,key= cv.contourArea, reverse=True)[0]
        ((x,y),raduis) = cv.minEnclosingCircle(cnt)
        cv.circle(frame, (int(x),int(y)), int(raduis), colors[3],2)

    
        M= cv.moments(cnt)  
        center = (int(M['m10']/M['m00']),int(M['m01']/M['m00']) )

        if center[1] <= 65 :
            if  40<= center[0] <= 140 :
                bPoints = []
                gPoints= []
                rPoints= []
                yPoints= []
                paint_window [67: , : , :]  = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0 #blue
            elif 275 <= center[0 ]<= 370:
                colorIndex = 1 # green
            elif 390 <= center[0 ]<= 485:
                colorIndex = 2 #red
            elif 505 <= center[0] <= 600:
                colorIndex = 3 #yellow                 
                    
        if colorIndex == 0:
            bPoints.insert(0, center)
        elif colorIndex == 1:
            gPoints.insert(0, center)
        elif colorIndex == 2:
            rPoints.insert(0, center)    
        elif colorIndex == 3:
            yPoints.insert(0, center)    
        
        points = [bPoints ,gPoints ,rPoints,yPoints] 
        for i in range(len(points)):
            for j in range(1, len(points[i])):
                cv.line(frame, points[i][j-1], points[i][j], colors[i] ,2)
                cv.line(paint_window, points[i][j-1], points[i][j], colors[i] ,2)




        


       cv.imshow('Frame', frame)
       cv.imshow('Paint', paint_window)
       cv.imshow('Mask', mask)
       if cv.waitKey(1) == ord('q'):
           break
   else:
      break    

cap.release()
cv.destroyAllWindows()

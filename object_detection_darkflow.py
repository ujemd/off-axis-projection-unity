# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 17:00:09 2020

@author: andrija
"""

from darkflow.net.build import TFNet
import cv2
import subprocess as sp


options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.5, "gpu" : 1.0}

tfnet = TFNet(options)

cap = cv2.VideoCapture(0)

bottle_consec = 0
bottle_found = False
book_consec = 0
book_found = False
clock_consec = 0
clock_found = False

while cap.isOpened():
    _, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = tfnet.return_predict(img)
    print(result)
    labels = []
    for k in range(len(result)):
        labels.append(result[k]['label'])
    if 'bottle' not in labels:
        bottle_consec = 0
    if 'book' not in labels:
        book_consec = 0
    if 'clock' not in labels:
        clock_consec = 0
        
    for k in range(len(result)):
        obj = result[k] 
        x1 = obj['topleft']['x']
        y1 = obj['topleft']['y']
        x2 = obj['bottomright']['x']
        y2 = obj['bottomright']['y']
        label = obj['label']


        if label == 'person':
            cv2.rectangle(img, (x1,y1), (x2, y2), (255, 0 , 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, label, (x1-5,y1-5), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        if label == 'bottle':
            cv2.rectangle(img, (x1,y1), (x2, y2), (0, 0, 255), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, label, (x1-5,y1-5), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            if not bottle_found and bottle_consec!=5:
                bottle_consec += 1
            else:
                if not bottle_found:
                    bottle_found = True
                    bottle_consec = 0
                    programName = "notepad.exe"
                    fileName = "file.txt"
                    f = open(fileName,"w+")
                    sp.Popen([programName, fileName])
        elif label == 'book':
            cv2.rectangle(img, (x1,y1), (x2, y2), (0, 255, 0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, label, (x1-5,y1-5), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
            if not book_found and book_consec!=5:
                book_consec += 1
            else:
                if not book_found:
                    book_found = True
                    book_consec = 0
                    programName = "C:\Program Files (x86)\Microsoft Office\Office14\WINWORD.exe"
                    fileName = "file.txt"
                    f = open(fileName,"w+")
                    sp.Popen([programName, fileName])
        elif label == 'clock':
            cv2.rectangle(img, (x1,y1), (x2, y2), (0, 255, 255), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, label, (x1-5,y1-5), font, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
            if not clock_found and clock_consec!=5:
                clock_consec += 1
            else:
                if not clock_found:
                    clock_found = True
                    clock_consec = 0
                    programName = "C:\Program Files (x86)\Microsoft Office\Office14\POWERPNT.exe"
                    fileName = "file.txt"
                    f = open(fileName,"w+")
                    sp.Popen([programName, fileName])
        
    # Display the output
    cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
#result = tfnet.return_predict(imgcv)

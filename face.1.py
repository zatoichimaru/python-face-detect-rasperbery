import numpy as np
import cv2
import os
import hashlib
import time
import json
from datetime import datetime

#Path
pathRoot = os.getcwd()
pathOpencv = os.path.dirname(cv2.__file__)

#max timer 2 minutes
timerStop = int( 120 )

#load file face
faceCascade = cv2.CascadeClassifier( pathOpencv + '\\data\\haarcascade_frontalface_alt.xml' )
eyeGlassCascade = cv2.CascadeClassifier(pathOpencv + '\\data\\haarcascade_eye_tree_eyeglasses.xml')

def generateRandomHashName():
    hashValue = hashlib.sha1( str( datetime.now() ).encode('utf-8') ).hexdigest()
    return hashValue

def generateFolderDefault():
    folderName = 'files'

    if not os.path.exists( os.path.join( pathRoot, folderName ) ):
        os.makedirs( os.path.join( pathRoot, folderName ) )
    
    return os.path.normpath( os.path.join( pathRoot, folderName ) )

def generateFolderPeople( fileName, pathValue ):
    if( not os.path.exists( os.path.join( pathValue, fileName ) ) ):
        os.makedirs( os.path.join( pathValue, fileName ) )
    
    return  os.path.normpath( os.path.join( pathValue, fileName ) )

def saveFaceDetected( cap, cameraStatus ):
    counterFrames = 0
    minute, second = ( 0, 0 )
    jsonTimer = []

    pathFolder = generateFolderPeople( generateRandomHashName(), generateFolderDefault() )
    
    while counterFrames < 300:
        ret, frame = cap.read()

        if second > 59:
            minute += 1
            second = 0

        time.sleep(1)
        second += 1
    
        if ( ret == False ):
            cap.release()
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale( gray, 1.3, 5 )
       
        #verifica se tem faces
        if not np.any(faces):
            continue

        for ( x, y, w, h ) in faces:
            #funcao para adicionar cor no rosto e olhos
            colorDraw( frame, gray, x, y, w, h )

        #funcao para adicionar cor no rosto e olhos
        showCam( cameraStatus, frame )

        #print( x,y,w,h )
        faceImage = frame[ y:y + h, x:x + w ]

        larg, alt, _ = faceImage.shape

        if ( larg * alt <= 20 * 20 ):
            continue

        faceImage = cv2.resize( faceImage, ( 255, 255 ) )
        fileName = 'people' + "-" + str( counterFrames ) + ".png"
        cv2.imwrite( os.path.join( pathFolder, fileName ), faceImage )
        jsonTimer.append({'datetime' : time.strftime("%Y-%m-%d %H:%M:%S"), 'minute' : minute, 'second': second })

        print('------' + fileName + '------')

        counterFrames += 1

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cap.release()
            cv2.destroyAllWindows()
            break

        ##time.sleep(3)
    print(pathFolder)
    print(jsonTimer)
    #saveFileJson( jsonTimer, pathFolder )

    cap.release()
    cv2.destroyAllWindows()
    return counterFrames


def showCam( status, frame ):
    if not status or status == False:
        return

    cv2.imshow( 'Poc SemParar',frame )

#funcao para adicionar cor no rosto e olhos
def colorDraw( frame, gray, x, y, w, h ):
    colorFace = ( 255, 0, 0 )
    colorEyes = ( 0, 255, 0 )
    stroke = 2
    
    cv2.rectangle( frame, ( x, y ), ( x + w, y + h ), colorFace, stroke )
    roiGray = gray[ y:y + h, x:x + w ]
    roiColor = frame[ y:y + h, x:x + w ]
    eyes = eyeGlassCascade.detectMultiScale( roiGray )

    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle( roiColor, (ex, ey), ( ex + ew, ey + eh ), colorEyes, stroke )


def saveFileJson( objectJson, path ):
    pathDFile = os.path.join( path, 'file.json' )
    fileJson = open( pathDFile, 'w')
    fileJson.write( objectJson )
    fileJson.close()

def start():
    total = 0
    cameraStatus = False
    camera = cv2.VideoCapture(0)
    total = saveFaceDetected( camera, cameraStatus )
    if( total >= 300 ):
        start()

def main():
    start()

if __name__ == "__main__":
    main()
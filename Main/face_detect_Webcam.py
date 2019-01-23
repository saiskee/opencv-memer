import cv2
import sys
import datetime
import numpy
import subprocess

basedir = os.path.dirname(sys.argv[0])

def addItems(frame,faces,mouths,eyes):
    glasses = cv2.imread(basedir+"/glasses.png",-1)
    joint = cv2.imread(basedir+"/joint.png",-1)
    
    t=datetime.datetime.now().time()
    filename=basedir+"/Saved/"+str(t.hour)+str(t.minute)+str(t.second)+".jpg"
    #print(frame[0,0])
    #print(joint)
    for (x, y, w, h) in faces:
        for (x2, y2, w2, h2) in eyes:
            if(x2>x and x2+w2<x+w and y2>y and y2+h2<y+h and y2+h2/2<y+h/2 and x2+w2/2>x+h/3 and x2+w2/2<x+2*h/3):
                glasses=cv2.resize(glasses,(w2,h2))
                for c in range(0,3):
                    frame[y2+h2/5:y2+6*h2/5, x2:x2+w2, c] =  glasses[:,:,c] * (glasses[:,:,3]/255.0) + frame[y2+h2/5:y2+6*h2/5, x2:x2+w2, c] * (1.0 - glasses[:,:,3]/255.0)
                break
        for (x2, y2, w2, h2) in mouths:
            if(x2>x and x2<x+w and y2>y+h/2 and y2+h2<y+5*h/4 and x2+w2/2>x+h/3 and x2+w2/2<x+2*h/3):
                joint=cv2.resize(joint,(w2,h2))
                for c in range(0,3):
                    frame[y2+h2/4:y2+5*h2/4, x2+w2/2:x2+3*w2/2, c] =  joint[:,:,c] * (joint[:,:,3]/255.0) + frame[y2+h2/4:y2+5*h2/4, x2+w2/2:x2+3*w2/2, c] * (1.0 - joint[:,:,3]/255.0)
                break

    cv2.imwrite(filename,frame)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def makeVideo(frame,w,h):
    fps=25
    capSize = (int(w),int(h))
    fourcc=cv2.cv.CV_FOURCC('m','p','4','v')
    out = cv2.VideoWriter() 
    success = out.open(basedir+'/output.mov',fourcc,fps,capSize,True) 
    frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    for i in range(162):
        temp=cv2.resize(frame,(int(w)+2*i,int(h)+2*i))
        tempFrame = temp[i/2:int(h)+i/2,i/2:int(w)+i/2]
        out.write(tempFrame)
    out.release() 
    out=None

#realpython.com
def capVideo():
    faceCascade = cv2.CascadeClassifier(basedir+"/haarcascade_frontalface_default.xml")
    mouthCascade = cv2.CascadeClassifier(basedir+"/Mouth.xml")
    eyesCascade = cv2.CascadeClassifier(basedir+"/frontalEyes35x16.xml")
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        ret, orig = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        mouths = mouthCascade.detectMultiScale(
            gray,
            scaleFactor=1.7,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        eyes = eyesCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        for (x, y, w, h) in mouths:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 1)
        
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        
        # Display the resulting frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('p'):
            #orig=cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
            w,h=video_capture.get(3),video_capture.get(4)
            video_capture.release()
            cv2.destroyAllWindows()
            finalImage=addItems(orig,faces,mouths,eyes)
            makeVideo(finalImage,w,h)
            
            
            cmd = 'pwd'
            subprocess.call(cmd, shell=True)  
            print(basedir)
            cmd = 'ffmpeg -y -i "%s"/Final.mp4 -r 30 -i "%s"/output.mov -filter:a aresample=async=1 -c:a flac -c:v copy -shortest "%s"/result.mkv' % (basedir,basedir,basedir)
            subprocess.call(cmd, shell=True)                                     # "Muxing Done
            print('Muxing Done')
            cmd = '~/../../Applications/VLC.app/Contents/MacOS/VLC "%s/result.mkv" -f --play-and-stop' % (basedir)
            subprocess.call(cmd, shell=True) 
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()

capVideo()


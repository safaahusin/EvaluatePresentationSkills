# import the necessary packages
from imutils.video import VideoStream
from imutils import face_utils
import datetime
import argparse
import imutils
import time
import dlib
import cv2
import index
import math
import FaceProcess
import processing
import Evaluate
#import recongation
import Detect
import threading
start_time = time.time()

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# initialize the video stream and allow the cammera sensor to warmup
print("[INFO] camera sensor warming up...")
# Open the first webcame device
vs = cv2.VideoCapture(0)
# loop over the frames from the video stream


#Create two opencv named windows
#cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)


#Position the windows next to eachother
cv2.moveWindow("base-image",0,100)
cv2.moveWindow("result-image",200,40)


# Start the window thread for the two windows we are using
cv2.startWindowThread()

#The deisred output width and height
# size For output windows
OUTPUT_SIZE_WIDTH = 775
OUTPUT_SIZE_HEIGHT = 600





# Create the tracker we will use
tracker = dlib.correlation_tracker()

# The variable we use to keep track of the fact whether we are
# currently using the dlib tracker
trackingFace = 0

#to calculate number of frame
frameCount=0

#coordinate of faical land mark for pervise face
ListOfIndexOld = []

#coordinate of faical land mark for current face
ListOfIndexNew = []
rectang=[]
dicSave={}
move=0
start=False

while True:


    # grab the frame from the threaded video stream, resize it to
    # have a maximum width of 400 pixels, and convert it to
    # grayscale
    rc, baseImage = vs.read()



    #cv2.imshow("base-image",  baseImage)



    # Result image is the image we will show the user, which is a
    # combination of the original image from the webcam and the
    # overlayed rectangle for the largest face
    frame = baseImage.copy()





    frameCount+=1

    if frameCount>10:
        if frameCount%10==0:
            d = processing.AllState()
            d.saveChange(dicSave)
            dicSave={}




    frame = imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



    if not trackingFace:

        print ("start")
        # detect faces in the grayscale frame
        rects = detector(gray, 1)
        print ("end")

        #check if detect faces or not
        if len(rects)>=1:

            if len(rects)==1:
                #use function crop face to return coordinate to face (x,y,w,h)
                (x, y, w, h) = FaceProcess.FaceProcess.cropFace(rects[0])

            else:
                # if i detect many face at first determine which face
                # i need to track it throw recongation  after that
                # track it
                #(x, y, w, h) = recongation.DoRecognation(rects, frame)

                #if not recongnaize any face
                #all face return false
                if x == None:
                    continue

                cv2.putText(frame, "loza", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 2)

            # Initialize the tracker
            tracker.start_track(frame,
                                dlib.rectangle(x ,
                                               y ,
                                               x + w ,
                                               y + h ))

            # Set the indicator variable such that we know the
            # tracker is tracking a region in the image
            trackingFace = 1

    # Check if the tracker is actively tracking a region in the image
    if trackingFace:

        # Update the tracker and request information about the
        # quality of the tracking update
        trackingQuality = tracker.update(frame)

        # If the tracking quality is good enough, determine the
        # updated position of the tracked region and draw the
        # rectangle
        #

        tracked_position = tracker.get_position()

        if tracked_position.is_empty() == False and trackingQuality >= 8.75:


            tracked_position = tracker.get_position()

            t_x = int(tracked_position.left())
            t_y = int(tracked_position.top())
            t_w = int(tracked_position.width())
            t_h = int(tracked_position.height())



            rect = dlib.rectangle(t_x, t_y, t_x + t_w, t_y + t_h)

            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array

            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            Count=0

            ListOfIndexNew = []

            for (x, y) in shape:
                Count += 1

                indexObj = index.Index(x, y)
                ListOfIndexNew.append(indexObj)

                if Count == 1 or Count == 17:

                    cv2.circle(frame, (x, y), 1, (0, 255, 255), 2)
                elif Count == 37 or Count == 46:
                    cv2.circle(frame, (x, y), 1, (57, 189, 37), 2)
                else:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), 2)

            if len(ListOfIndexNew)!=0:

                direction = Detect.Detect.detectDirection(ListOfIndexNew)

                if (direction[0]!="F" or (direction[0]=="F" and len(direction)!=1) )and start==False:

                    cv2.putText(baseImage,"""you must look forward direction""", (0, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2)

                    cv2.putText(baseImage, """for camera """, (0, 90),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2)



                else:

                    cv2.putText(baseImage, "Start Evaluation ...", (0, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2)


                    start=True

                    position = Detect.Detect.detectPosition(ListOfIndexNew[0].x)

                    dicSave[frameCount] = [direction, position]
                    print(dicSave)

                    cv2.putText(frame, str(' '.join(direction)), (100, 50),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2)

                    cv2.putText(frame, str(' '.join(position)), (100, 90),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 0, 255), 2)

                    if len(ListOfIndexNew) != 0 and len(ListOfIndexOld) == 0:
                        rectang = Detect.Detect.locate_of_face_esraa(ListOfIndexNew)
                        cv2.rectangle(frame, (rectang[0], rectang[1]), (rectang[3], rectang[2]), (0, 0, 255), 2)

                    if len(ListOfIndexNew) != 0 and len(ListOfIndexOld) != 0:
                        if len(rectang) != 0:
                            p, rectang = Detect.Detect.compare(rectang, ListOfIndexNew)
                            if p=="Left" or p=="Right":
                                move+=1

                            cv2.rectangle(frame, (rectang[0], rectang[1]), (rectang[3], rectang[2]), (0, 0, 255), 2)
                        cv2.putText(frame, p, (100, 110),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (255, 255, 255), 2)


                    # just copy all element to old
                    ListOfIndexOld = []
                    for x in ListOfIndexNew:
                        ListOfIndexOld.append(x)

        else:
            # If the quality of the tracking update is not
            # sufficient (e.g. the tracked region moved out of the
            # screen) we stop the tracking of the face and in the
            # next loop we will find the largest face in the image
            # again
            trackingFace = 0
            # Since we want to show something larger on the screen than the
            # original 320x240, we resize the image again
            #


    # Resize the image to 775*600
    frame = cv2.resize(frame, (OUTPUT_SIZE_WIDTH, OUTPUT_SIZE_HEIGHT))
    baseImage= cv2.resize(baseImage, (800, OUTPUT_SIZE_HEIGHT))

    # show the frame
    cv2.imshow("result-image", frame)
    cv2.imshow("user Image", baseImage)
    key = cv2.waitKey(1) & 0xFF

    # if the `qqa` key was pressed, break from the loop
    if key == ord("b"):
        tim=Detect.Detect.timer(start_time, time.time())
        print(move)
        Obj=Evaluate.evaluate(processing.AllState.dictonary,move,tim)
        res=Obj.result()
        Count=0
        for note in res:
            print (Count,' :- ',note)
            Count+=1
        break

# do a bit of cleanup
cv2.destroyAllWindows()
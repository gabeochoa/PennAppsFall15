#! /usr/bin/python
import numpy as np
import cv2
import cv


def openVideoFile(fileToOpen):
    try:
        vidFile = cv2.VideoCapture(fileToOpen)
    except:
        print "problem opening input stream"
        sys.exit(1)
    if not vidFile.isOpened():
        print "capture stream not open"
        sys.exit(1)
    nFrames = int(vidFile.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)) # one good way of namespacing legacy openCV: cv2.cv.*
    print "frame number: %s" %nFrames
    fps = vidFile.get(cv2.cv.CV_CAP_PROP_FPS)
    print "FPS value: %s" %fps

    ret, frame = vidFile.read() # read first frame, and the return code of the function.
    frame=  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    oldframe = frame

    while ret:  # note that we don't have to use frame number here, we could read from a live written file.
        cv2.imshow("frameWindow", frame)
        cv2.waitKey(int(1/fps*1000)) # time to wait between frames, in mSec
        ret, frame = vidFile.read() # read next frame, get next return code
        frame=  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        stereo = cv2.StereoBM(1, 16, 15)
        
        window_size = 3
        min_disp = 16
        num_disp = 112-min_disp
        stereo = cv2.StereoSGBM(minDisparity = min_disp,
            numDisparities = num_disp,
            SADWindowSize = 16,
            P1 = 8*3*window_size**2,
            P2 = 32*3*window_size**2,
            disp12MaxDiff = 1,
            uniquenessRatio = 10,
            speckleWindowSize = 100,
            speckleRange = 32
        )
        disp = stereo.compute(oldframe, frame).astype(np.float32) / 16.0
        cv2.imshow("aa", (disp-min_disp)/num_disp)
        oldframe = frame

    



def main():
    openVideoFile("can.MOV")
    return



main()

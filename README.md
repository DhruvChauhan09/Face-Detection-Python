# Head Tilt Tracker 
A real-time head direction tracker using **MediaPipe Face Mesh** and **OpenCV**.  
This project detects facial landmarks and determines whether the user is looking **left**, **right**, **up**, **down**, or **center** using key face points like nose, eyes, chin, and forehead.

## Features
- Real-time face mesh detection using webcam
- Calculates horizontal (left/right) and vertical (up/down) head movement
- Displays direction overlay on video
- Draws bounding box and key facial landmarks
- Handles absence of face with warning text

## How It Works
- Uses MediaPipe’s FaceMesh to extract 468 facial landmarks.
- Tracks key landmark indices:
    Nose tip (1)
    Chin (152)
    Left eye (33), Right eye (263)
    Forehead (10)
- Compares x/y positions to infer head tilt direction.
- Displays result as an overlay on the webcam frame.

## Technologies Used
- [Python 3]
- [OpenCV]
- [MediaPipe]

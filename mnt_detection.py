import cv2
import mediapipe as mp

mpFace = mp.solutions.face_mesh
face_mesh = mpFace.FaceMesh()
mpDraw = mp.solutions.drawing_utils

NOSE_TIP = 1
CHIN = 152
LEFT_EYE = 33
RIGHT_EYE = 263
FOREHEAD = 10

cap = cv2.VideoCapture(0)

while True:
    success,frame=cap.read()
    frame = cv2.flip(frame,1)
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    h,w,_ = frame.shape

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        def getpoint(index):
            return int(landmarks[index].x*w),int(landmarks[index].y*h)
        
        

        nose_x = landmarks[1].x  
        leye_x = landmarks[33].x
        reye_x = landmarks[263].x
        nose_y = landmarks[1].y 
        forehead_y = landmarks[10].y
        chin_y = landmarks[152].y 

        # horizontal
        left_score = nose_x-leye_x
        right_score = reye_x-nose_x
        if left_score > right_score + 0.05:
            h_direction = "Right"
        elif left_score + 0.05 < right_score:
            h_direction = "Left"
        else:
            h_direction = "--"

        # vertical
        up_score = nose_y-forehead_y
        down_score = chin_y-nose_y

        if up_score > down_score + 0.05:
            v_direction = "Down"
        elif down_score > up_score + 0.05:
            v_direction = "Up"   
        else:
            v_direction = "--"  
            

        for face_landmarks in results.multi_face_landmarks:
            # Collect all landmark coordinates
            x_list = []
            y_list = []

            for lm in face_landmarks.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                x_list.append(x)
                y_list.append(y)

            # Get bounding box
            x_min, x_max = min(x_list), max(x_list)
            y_min, y_max = min(y_list), max(y_list)

            # Draw rectangle
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  

        for bp in [NOSE_TIP,CHIN,LEFT_EYE,RIGHT_EYE,FOREHEAD]:
            x, y = getpoint(bp)
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)        


        if (v_direction=="Down" or v_direction=="Up")and(h_direction=="Left" or h_direction=="Right"):
            cv2.putText(frame, f"Direction: {v_direction}-{h_direction}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        elif (v_direction=="Down" or v_direction=="Up")and(h_direction=="--"): 
            cv2.putText(frame, f"Direction: {v_direction}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        elif (v_direction=="--")and(h_direction=="Left" or h_direction=="Right"):       
            cv2.putText(frame, f"Direction: {h_direction}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
        else:
            cv2.putText(frame, f"Direction: Facing Center", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)   


    else:
        cv2.putText(frame, "Face Not Detected", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)         
        



    cv2.imshow("Head Tilt Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

   



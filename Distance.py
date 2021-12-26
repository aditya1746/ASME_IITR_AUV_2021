import cv2
import numpy as np

##frame=cv2.imread("gate3.png")
cap = cv2.VideoCapture('GateTest.mp4')
font = cv2.FONT_HERSHEY_COMPLEX

def nothing(x):
	pass

cv2.namedWindow('track',cv2.WINDOW_NORMAL)
cv2.namedWindow('tracker',cv2.WINDOW_NORMAL)
cv2.createTrackbar('bt','track',0,255,nothing)
cv2.createTrackbar('gt','track',0,255,nothing)
cv2.createTrackbar('rt','track',0,255,nothing)
cv2.createTrackbar('x','tracker',0,7000,nothing)



while(True):
    ret, frame = cap.read()

    bt = cv2.getTrackbarPos('bt', 'track')
    gt = cv2.getTrackbarPos('gt', 'track')
    rt = cv2.getTrackbarPos('rt', 'track')
    x = cv2.getTrackbarPos('x', 'tracker')

    b, g, r = cv2.split(frame)
    b1 = b+152
    g1 = g-126
    r1 = r-204

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equc_b = clahe.apply(b1)
    equc_g = clahe.apply(g1)
    equc_r = clahe.apply(r1)
    img = cv2.merge((equc_b, equc_g, equc_r))

   # cv2.imshow("img",img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(image=blur, threshold1=100, threshold2=200)
   # cv2.imshow("blur",blur)

    _, thresh = cv2.threshold(edges, 10, 255, cv2.THRESH_BINARY)
   # cv2.imshow("thresh",thresh)
    dilated = cv2.dilate(thresh, None, iterations=3)
   # cv2.imshow("dilated",dilated)
    contours,_ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    x=3048
    for contour in contours :
        if cv2.contourArea(contour) < 7000-x :
            continue
        else:
            if len(contours) > 0:
                areas = [cv2.contourArea(c) for c in contours]
                max_index = np.argmax(areas)
                cnt = contours[max_index]
            area = cv2.contourArea(cnt)
            ##epsilon = 0.00005 * cv2.arcLength(cnt, True)
            ##approx = cv2.approxPolyDP(cnt, epsilon, True)
            # finding centre
            M = cv2.moments(cnt)
            Cx = int(M['m10'] / M['m00'])
            Cy = int(M['m01'] / M['m00'])
            a = Cx
            b = Cy
            cv2.circle(frame, (a, b), 3, (0, 0, 0), -1)

            # finding distance
            distance = 2 * (10 ** (-7)) * (area ** 2) - (0.0067 * area) + 83.487
            S = 'Distance Of Object: ' + str(distance)
            cv2.putText(frame,S, (5, 50), font, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

            # drawing rectangles
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)


    cv2.imshow('frame', frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cv2.waitKey(0)
cv2.destroyAllWindows()
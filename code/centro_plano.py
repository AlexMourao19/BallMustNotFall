import cv2
from picamera2 import Picamera2 as PiCamera,Preview
import numpy as np

camera = PiCamera()
#camera.zoom =(0,0,0,0)
config = camera.create_still_configuration()
#config = camera.create_still_configuration(main={"size":(1280,720)},lores={"size":(640,480)})
#camera.resolution = (1280,720)
#camera.preview_configuration.main.format = "RGB888"
camera.preview_configuration.main.size=(1280,720)
camera.preview_configuration.main.align()
camera.configure(config)
#camera.configure("preview")
camera.start()

frame = camera.capture_array()
#image = np.empty((1280,720*3),dtype = np.uint8)
#camera.start_and_capture_file('/home/ballmustnotfall/Desktop/test.jpg')
#image = camera.capture_image()
#frame = image
while True:
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("PiCam",frame_rgb)
    
    if cv2.waitKey(1)==ord('q'):
        break
cv2.destroyAllWindows()
print("frame size: ",frame.size)

gray = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2GRAY)
while True:
    cv2.imshow("PiCam",gray)
    if cv2.waitKey(1)==ord('e'):
        break

ret,thresh = cv2.threshold(gray,200,255,cv2.THRESH_BINARY_INV)
while True:
    cv2.imshow("PiCam",thresh)
    if cv2.waitKey(1)==ord('w'):
        break

contours, hierarchy = cv2.findContours(thresh,
  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for c in contours:
    if (cv2.contourArea(c) > 1000000):
         area = cv2.contourArea(c)
         epsilon = 0.02*cv2.arcLength(c,True)
         polygon = cv2.approxPolyDP(c,epsilon,True)
         test = frame.copy()
         cv2.drawContours(test,[polygon],-1,(0,255,0),10)
         
         M = cv2.moments(polygon)
         
         Cx = int(M["m10"]/M["m00"])
         Cy = int(M["m01"]/M["m00"])
         
         cv2.circle(test, (Cx, Cy), 5, (0, 255, 255), 0)
         cv2.putText(test, f'({Cx},{Cy})', (Cx-25, Cy-25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
         
         print("area: ",area)
         while True:
            cv2.imshow("PiCam",test)
            if cv2.waitKey(1)==ord('q'):
                break
         

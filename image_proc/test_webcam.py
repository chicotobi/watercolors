import cv2
import image_processing

def line_x(x1,x2,y1,y2):
  def f(x):
    return (y2-y1)/(x2-x1)*(x-x1)+y1
  return f

def line_y(x1,x2,y1,y2):
  def f(y):
    return (x2-x1)/(y2-y1)*(y-y1)+x1
  return f

def mideval(x1,x2,y1,y2,x0=-1,y0=-1):
  if x0 == -1:
    return line_y(x1,x2,y1,y2)(y0)
  else:
    return line_x(x1,x2,y1,y2)(x0)
  
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

while rval:      
      
    img = frame
    
    try:
      img = image_processing.process(img)
    except:
      print("An exception occurred")
  
    cv2.imshow("preview", img)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")

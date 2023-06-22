import image_processing
import cv2
      
import pickle as pkl
img = pkl.load(open('frame.pkl','rb'))

img = image_processing.process(img)

# Show result
cv2.imshow("Result Image", img)

if cv2.waitKey(0) & 0xff == 27:  
    cv2.destroyAllWindows()  
import cv2
import numpy as np
import math
import plot_graph

MAX_HEIGHT = 4

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

def line_intersection(line1, line2):
  line1 = ((line1[0],line1[1]),(line1[2],line1[3]))
  line2 = ((line2[0],line2[1]),(line2[2],line2[3]))
  
  xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
  ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

  def det(a, b):
    return a[0] * b[1] - a[1] * b[0]

  div = det(xdiff, ydiff)
  if div == 0:
    raise Exception('lines do not intersect')

  d = (det(*line1), det(*line2))
  x = det(d, xdiff) / div
  y = det(d, ydiff) / div
  return x, y

def fill_grid(grid,nflask):
  nx = 2 * nflask # Vertical lines
  ny = MAX_HEIGHT + 2 # Horizontal lines (best case)

def process(img):
  
  ymax, xmax, _ = img.shape
  
  MIN_WIDTH_CELL = 60
  MIN_WIDTH_SPACE = 35
  MIN_HEIGHT_CELL = 50
  MIN_HEIGHT_SPACE = 20
  
  # Convert the image to gray-scale
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  # Find the edges in the image using canny detector
  edges = cv2.Canny(gray, 20, 60)
  # Detect points that form a line
  lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)
  # Draw lines on the image
  vlines = []
  hlines = []
  for line in lines:
      x1, y1, x2, y2 = line[0]
          
      # Get angle of the lines
      angle = math.atan2(y2-y1, x2-x1)
      if abs(angle) < math.pi/2 * 0.05:
        # Horizontal line
        #cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        x0 = xmax//2
        y0 = mideval(x1,x2,y1,y2,x0=x0)
        #cv2.circle(img, (x0,int(y0)), 5, (0,0,255), -1)
        hlines += [(x1,y1,x2,y2,y0)]
      elif abs(angle) > math.pi/2 * 0.95:
        # Vertical line
        #cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        y0 = ymax//2
        x0 = mideval(x1,x2,y1,y2,y0=y0)
        #cv2.circle(img, (int(x0),y0), 5, (0,0,255), -1)
        vlines += [(x1,y1,x2,y2,x0)]
  
  # Sort lines
  hlines = sorted(hlines,key=lambda x: x[4])
  vlines = sorted(vlines,key=lambda x: x[4])
  
  # Find first hline 
  dists = [hlines[i+1][4]-hlines[i][4] for i in range(len(hlines)-1)]
  dists2 = [i for i in dists if i>MIN_HEIGHT_CELL]
  
  # Drop hlines if distance is too small
  new_hlines = [hlines[0]]
  last_value = hlines[0][4]
  for i in range(1,len(hlines)):
    if hlines[i][4] - last_value > MIN_HEIGHT_SPACE:
      new_hlines += [hlines[i]]
      last_value = hlines[i][4]
      
  # Drop hlines if distance is too small
  new_vlines = [vlines[0]]
  last_value = vlines[0][4]
  for i in range(1,len(vlines)):
    if vlines[i][4] - last_value > MIN_WIDTH_SPACE:
      new_vlines += [vlines[i]]
      last_value = vlines[i][4]
      
      
  for line in new_hlines:
      x1, y1, x2, y2, _ = line
      cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
      
  for line in new_vlines:
      x1, y1, x2, y2, _ = line
      cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
      
  # get intersection points
  for h in new_hlines:
    for v in new_vlines:
      x, y = line_intersection(h,v) 
      x = round(x)
      y = round(y)
      cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
  
  
  return img
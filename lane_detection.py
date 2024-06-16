import cv2
import numpy as np

class LaneDetection:
    def __init__(self):
        pass
    def region_of_interest(self,img,vertices):
        mask=np.zeros_like(img)
        cv2.fillPoly(mask,vertices,255)
        masked_image=cv2.bitwise_and(img,mask)
        return masked_image
    def detect_edges(self,frame):
        gray=cv2.cvtColor(frame,cv2.COLOR_BAYER_BG2GRAY)
        blur=cv2.GaussianBlur(gray,(5,5),0)
        edges=cv2.Canny(blur,50,150)
        return edges
    def detect_lines(self, edges):
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, maxLineGap=50)
        return lines

    def draw_lines(self, frame, lines):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
        combined = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
 
    def process_frame(self, frame):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # Detect edges using Canny
        edges = cv2.Canny(blur, 50, 150)
        return edges
